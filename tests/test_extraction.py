import pytest
from unittest.mock import Mock, MagicMock
from src.data.extractor import DataExtractor
from src.config.settings import Settings


@pytest.fixture
def mock_page_handler():
    handler = Mock()
    handler.page = Mock()
    return handler


@pytest.fixture
def mock_settings():
    settings = Mock(spec=Settings)
    settings.extraction = [
        {
            'name': 'title',
            'selector': 'h1',
            'type': 'text',
            'target_cell': 'A1'
        },
        {
            'name': 'description',
            'selector': '.description',
            'type': 'text',
            'target_cell': 'B1'
        }
    ]
    return settings


@pytest.fixture
def extractor(mock_page_handler, mock_settings):
    return DataExtractor(mock_page_handler, mock_settings)


class TestDataExtractor:
    
    def test_init(self, extractor, mock_page_handler, mock_settings):
        assert extractor.page_handler == mock_page_handler
        assert extractor.settings == mock_settings
    
    def test_extract_text(self, extractor, mock_page_handler):
        mock_page_handler.get_text.return_value = 'Test Title'
        
        result = extractor._extract_text('h1')
        
        assert result == 'Test Title'
        mock_page_handler.get_text.assert_called_once_with('h1')
    
    def test_extract_text_with_whitespace(self, extractor, mock_page_handler):
        mock_page_handler.get_text.return_value = '  Test Title  '
        
        result = extractor._extract_text('h1')
        
        assert result == 'Test Title'
    
    def test_extract_attribute(self, extractor, mock_page_handler):
        mock_page_handler.get_attribute.return_value = 'test-value'
        
        result = extractor._extract_attribute('.link', 'href')
        
        assert result == 'test-value'
        mock_page_handler.get_attribute.assert_called_once_with('.link', 'href')
    
    def test_extract_table(self, extractor, mock_page_handler):
        mock_row1 = Mock()
        mock_row1.locator.return_value.all.return_value = [
            Mock(inner_text=Mock(return_value='Cell1')),
            Mock(inner_text=Mock(return_value='Cell2'))
        ]
        
        mock_row2 = Mock()
        mock_row2.locator.return_value.all.return_value = [
            Mock(inner_text=Mock(return_value='Cell3')),
            Mock(inner_text=Mock(return_value='Cell4'))
        ]
        
        mock_page_handler.page.locator.return_value.all.return_value = [mock_row1, mock_row2]
        
        result = extractor._extract_table('table')
        
        assert len(result) == 2
        assert result[0] == ['Cell1', 'Cell2']
        assert result[1] == ['Cell3', 'Cell4']
    
    def test_extract_list(self, extractor, mock_page_handler):
        mock_page_handler.page.locator.return_value.all.return_value = [
            Mock(inner_text=Mock(return_value='Item1')),
            Mock(inner_text=Mock(return_value='Item2')),
            Mock(inner_text=Mock(return_value='Item3'))
        ]
        
        result = extractor._extract_list('.items')
        
        assert result == ['Item1', 'Item2', 'Item3']
    
    def test_extract_all(self, extractor, mock_page_handler):
        mock_page_handler.get_text.side_effect = ['Test Title', 'Test Description']
        
        result = extractor.extract_all()
        
        assert 'title' in result
        assert 'description' in result
        assert result['title'] == 'Test Title'
        assert result['description'] == 'Test Description'
    
    def test_extract_all_empty_config(self, mock_page_handler, mock_settings):
        mock_settings.extraction = []
        extractor = DataExtractor(mock_page_handler, mock_settings)
        
        result = extractor.extract_all()
        
        assert result == {}
    
    def test_extract_all_invalid_field_config(self, mock_page_handler, mock_settings):
        mock_settings.extraction = [
            {'name': 'test', 'selector': '.test', 'type': 'text'}
        ]
        extractor = DataExtractor(mock_page_handler, mock_settings)
        
        result = extractor.extract_all()
        
        assert result == {}
    
    def test_extract_by_selector_text(self, extractor, mock_page_handler):
        mock_page_handler.get_text.return_value = 'Sample Text'
        
        result = extractor.extract_by_selector('.sample', 'text')
        
        assert result == 'Sample Text'
    
    def test_extract_by_selector_attribute(self, extractor, mock_page_handler):
        mock_page_handler.get_attribute.return_value = 'sample-attr'
        
        result = extractor.extract_by_selector('.sample', 'attribute', 'data-id')
        
        assert result == 'sample-attr'
    
    def test_extract_by_selector_table(self, extractor, mock_page_handler):
        mock_row = Mock()
        mock_row.locator.return_value.all.return_value = [
            Mock(inner_text=Mock(return_value='Data'))
        ]
        mock_page_handler.page.locator.return_value.all.return_value = [mock_row]
        
        result = extractor.extract_by_selector('table', 'table')
        
        assert isinstance(result, list)
    
    def test_extract_by_selector_list(self, extractor, mock_page_handler):
        mock_page_handler.page.locator.return_value.all.return_value = [
            Mock(inner_text=Mock(return_value='Item'))
        ]
        
        result = extractor.extract_by_selector('.items', 'list')
        
        assert result == ['Item']
    
    def test_extract_by_selector_unknown_type(self, extractor, mock_page_handler):
        result = extractor.extract_by_selector('.test', 'unknown')
        
        assert result is None
    
    def test_wait_and_extract_success(self, extractor, mock_page_handler):
        mock_page_handler.wait_for_element.return_value = True
        mock_page_handler.get_text.return_value = 'Test'
        
        result = extractor.wait_and_extract('.test', 'text', 5000)
        
        assert result == 'Test'
        mock_page_handler.wait_for_element.assert_called_once_with('.test', timeout=5000)
    
    def test_wait_and_extract_timeout(self, extractor, mock_page_handler):
        mock_page_handler.wait_for_element.return_value = False
        
        result = extractor.wait_and_extract('.test', 'text', 5000)
        
        assert result is None
