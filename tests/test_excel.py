import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
from src.excel.reader import ExcelReader
from src.excel.writer import ExcelWriter


@pytest.fixture
def temp_excel_file(tmp_path):
    return str(tmp_path / "test.xlsx")


class TestExcelReader:
    
    @pytest.fixture
    def reader(self, temp_excel_file):
        return ExcelReader(temp_excel_file)
    
    def test_init(self, reader, temp_excel_file):
        assert reader.file_path == Path(temp_excel_file)
        assert reader.workbook is None
    
    def test_open_nonexistent_file(self, reader):
        result = reader.open()
        
        assert result == False
    
    def test_read_cell(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_cell = MagicMock()
            mock_cell.value = 'Test Value'
            mock_sheet.__getitem__ = Mock(return_value=mock_cell)
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.read_cell('A1')
            
            assert result == 'Test Value'
    
    def test_read_row(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_row = [MagicMock(value='Val1'), MagicMock(value='Val2')]
            mock_sheet.__getitem__ = Mock(return_value=mock_row)
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.read_row(1)
            
            assert result == ['Val1', 'Val2']
    
    def test_read_column(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_cell1 = MagicMock(value='Val1')
            mock_cell2 = MagicMock(value='Val2')
            mock_sheet.__getitem__ = Mock(return_value=[mock_cell1, mock_cell2])
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.read_column('A')
            
            assert result == ['Val1', 'Val2']
    
    def test_read_range(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_row = [MagicMock(value='Val')]
            mock_sheet.__getitem__ = Mock(return_value=[mock_row])
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.read_range('A1', 'B2')
            
            assert isinstance(result, list)
    
    def test_read_all_data(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_sheet.iter_rows = Mock(return_value=[
                (MagicMock(value='A1'), MagicMock(value='B1')),
                (MagicMock(value='A2'), MagicMock(value='B2'))
            ])
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.read_all_data()
            
            assert len(result) == 2
    
    def test_read_to_dict(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_sheet.iter_rows = Mock(return_value=[
                (MagicMock(value='Name'), MagicMock(value='Age')),
                (MagicMock(value='John'), MagicMock(value=30))
            ])
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.read_to_dict()
            
            assert len(result) == 1
            assert 'Name' in result[0]
            assert 'Age' in result[0]
    
    def test_get_cell_value(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_cell = MagicMock(value='Test')
            mock_sheet.cell = Mock(return_value=mock_cell)
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            reader.open()
            result = reader.get_cell_value(1, 1)
            
            assert result == 'Test'
    
    def test_context_manager(self, reader, temp_excel_file):
        with patch('src.excel.reader.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            with reader:
                assert reader.workbook is not None
            
            assert reader.workbook is None


class TestExcelWriter:
    
    @pytest.fixture
    def writer(self, temp_excel_file):
        return ExcelWriter(temp_excel_file)
    
    def test_init(self, writer, temp_excel_file):
        assert writer.file_path == Path(temp_excel_file)
        assert writer.workbook is None
    
    def test_create_new(self, writer):
        with patch('src.excel.writer.Workbook') as mock_workbook:
            mock_wb = MagicMock()
            mock_workbook.return_value = mock_wb
            
            result = writer.create_new()
            
            assert result == True
            assert writer.workbook == mock_wb
    
    def test_write_cell(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.write_cell('A1', 'Test')
            
            assert result == True
    
    def test_write_row(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.write_row(1, ['A', 'B', 'C'])
            
            assert result == True
    
    def test_write_column(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.write_column('A', ['A', 'B', 'C'])
            
            assert result == True
    
    def test_append_row(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.append_row(['A', 'B', 'C'])
            
            assert result == True
            mock_sheet.append.assert_called_once_with(['A', 'B', 'C'])
    
    def test_write_dict(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.write_dict({'Name': 'John', 'Age': 30})
            
            assert result == True
    
    def test_write_header(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.write_header(['Name', 'Age', 'City'])
            
            assert result == True
    
    def test_clear_sheet(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_sheet.max_row = 5
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.clear_sheet('Sheet1')
            
            assert result == True
            mock_sheet.delete_rows.assert_called_once_with(1, 5)
    
    def test_get_last_row(self, writer):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_sheet = MagicMock()
            mock_sheet.max_row = 10
            mock_workbook.__getitem__ = Mock(return_value=mock_sheet)
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            writer.open_existing()
            result = writer.get_last_row()
            
            assert result == 10
    
    def test_context_manager(self, writer, temp_excel_file):
        with patch('src.excel.writer.load_workbook') as mock_load:
            mock_workbook = MagicMock()
            mock_workbook.sheetnames = ['Sheet1']
            mock_load.return_value = mock_workbook
            
            with writer:
                assert writer.workbook is not None
            
            mock_workbook.save.assert_called_once()
