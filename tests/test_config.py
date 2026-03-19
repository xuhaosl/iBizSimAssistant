import pytest
from unittest.mock import Mock, patch
from src.config.settings import Settings
from src.utils.validators import Validators


class TestSettings:
    
    @pytest.fixture
    def config_file(self, tmp_path):
        import yaml
        config_data = {
            'website': {
                'base_url': 'https://example.com',
                'login_url': '/login',
                'target_pages': ['/page1', '/page2']
            },
            'login': {
                'username_selector': '#username',
                'password_selector': '#password',
                'submit_selector': '#submit',
                'success_indicator': '.success'
            },
            'excel': {
                'input_file': './data/input.xlsx',
                'output_file': './data/output.xlsx',
                'sheet_name': 'Sheet1'
            },
            'extraction': [
                {
                    'name': 'field1',
                    'selector': '.field1',
                    'type': 'text',
                    'target_cell': 'A1'
                }
            ],
            'submission': [
                {
                    'excel_cell': 'A1',
                    'selector': '#input1',
                    'type': 'text'
                }
            ],
            'browser': {
                'headless': False,
                'timeout': 30000,
                'screenshot_on_error': True
            }
        }
        
        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        return str(config_file)
    
    @pytest.fixture
    def settings(self, config_file):
        return Settings(config_file)
    
    def test_init(self, settings):
        assert settings.config is not None
        assert isinstance(settings.config, dict)
    
    def test_website_property(self, settings):
        website = settings.website
        assert website['base_url'] == 'https://example.com'
        assert website['login_url'] == '/login'
        assert len(website['target_pages']) == 2
    
    def test_login_property(self, settings):
        login = settings.login
        assert login['username_selector'] == '#username'
        assert login['password_selector'] == '#password'
        assert login['submit_selector'] == '#submit'
    
    def test_excel_property(self, settings):
        excel = settings.excel
        assert excel['input_file'] == './data/input.xlsx'
        assert excel['output_file'] == './data/output.xlsx'
        assert excel['sheet_name'] == 'Sheet1'
    
    def test_extraction_property(self, settings):
        extraction = settings.extraction
        assert len(extraction) == 1
        assert extraction[0]['name'] == 'field1'
    
    def test_submission_property(self, settings):
        submission = settings.submission
        assert len(submission) == 1
        assert submission[0]['excel_cell'] == 'A1'
    
    def test_browser_property(self, settings):
        browser = settings.browser
        assert browser['headless'] == False
        assert browser['timeout'] == 30000
        assert browser['screenshot_on_error'] == True
    
    def test_get_full_url(self, settings):
        url = settings.get_full_url('/test')
        assert url == 'https://example.com/test'
    
    def test_get_input_file_path(self, settings):
        path = settings.get_input_file_path()
        assert str(path).endswith('data/input.xlsx')
    
    def test_get_output_file_path(self, settings):
        path = settings.get_output_file_path()
        assert str(path).endswith('data/output.xlsx')
    
    def test_get_sheet_name(self, settings):
        sheet_name = settings.get_sheet_name()
        assert sheet_name == 'Sheet1'


class TestValidators:
    
    def test_is_valid_email_valid(self):
        assert Validators.is_valid_email('test@example.com') == True
        assert Validators.is_valid_email('user.name+tag@domain.co.uk') == True
    
    def test_is_valid_email_invalid(self):
        assert Validators.is_valid_email('invalid') == False
        assert Validators.is_valid_email('invalid@') == False
        assert Validators.is_valid_email('@example.com') == False
    
    def test_is_valid_url_valid(self):
        assert Validators.is_valid_url('https://example.com') == True
        assert Validators.is_valid_url('http://test.org') == True
    
    def test_is_valid_url_invalid(self):
        assert Validators.is_valid_url('not-a-url') == False
        assert Validators.is_valid_url('ftp://example.com') == False
    
    def test_is_valid_cell_reference_valid(self):
        assert Validators.is_valid_cell_reference('A1') == True
        assert Validators.is_valid_cell_reference('Z999') == True
        assert Validators.is_valid_cell_reference('AA100') == True
    
    def test_is_valid_cell_reference_invalid(self):
        assert Validators.is_valid_cell_reference('1A') == False
        assert Validators.is_valid_cell_reference('A') == False
        assert Validators.is_valid_cell_reference('') == False
    
    def test_is_valid_selector_valid(self):
        assert Validators.is_valid_selector('#id') == True
        assert Validators.is_valid_selector('.class') == True
        assert Validators.is_valid_selector('div > p') == True
    
    def test_is_valid_selector_invalid(self):
        assert Validators.is_valid_selector('') == False
    
    def test_is_not_empty_valid(self):
        assert Validators.is_not_empty('test') == True
        assert Validators.is_not_empty(['item']) == True
        assert Validators.is_not_empty({'key': 'value'}) == True
        assert Validators.is_not_empty(123) == True
    
    def test_is_not_empty_invalid(self):
        assert Validators.is_not_empty(None) == False
        assert Validators.is_not_empty('') == False
        assert Validators.is_not_empty([]) == False
        assert Validators.is_not_empty({}) == False
    
    def test_is_positive_number_valid(self):
        assert Validators.is_positive_number(1) == True
        assert Validators.is_positive_number(0.5) == True
        assert Validators.is_positive_number('100') == True
    
    def test_is_positive_number_invalid(self):
        assert Validators.is_positive_number(0) == False
        assert Validators.is_positive_number(-1) == False
        assert Validators.is_positive_number('abc') == False
        assert Validators.is_positive_number(None) == False
    
    def test_validate_config_valid(self):
        config = {
            'website': {
                'base_url': 'https://example.com',
                'login_url': '/login',
                'target_pages': []
            },
            'login': {
                'username_selector': '#username',
                'password_selector': '#password',
                'submit_selector': '#submit',
                'success_indicator': '.success'
            },
            'excel': {
                'input_file': './input.xlsx',
                'output_file': './output.xlsx',
                'sheet_name': 'Sheet1'
            }
        }
        
        is_valid, error = Validators.validate_config(config)
        assert is_valid == True
        assert error is None
    
    def test_validate_config_missing_keys(self):
        config = {
            'website': {'base_url': 'https://example.com'}
        }
        
        is_valid, error = Validators.validate_config(config)
        assert is_valid == False
        assert 'Missing required key' in error
    
    def test_validate_config_invalid_url(self):
        config = {
            'website': {
                'base_url': 'not-a-url',
                'login_url': '/login',
                'target_pages': []
            },
            'login': {
                'username_selector': '#username',
                'password_selector': '#password',
                'submit_selector': '#submit',
                'success_indicator': '.success'
            },
            'excel': {
                'input_file': './input.xlsx',
                'output_file': './output.xlsx',
                'sheet_name': 'Sheet1'
            }
        }
        
        is_valid, error = Validators.validate_config(config)
        assert is_valid == False
        assert 'Invalid base_url' in error
    
    def test_validate_config_invalid_selectors(self):
        config = {
            'website': {
                'base_url': 'https://example.com',
                'login_url': '/login',
                'target_pages': []
            },
            'login': {
                'username_selector': '',
                'password_selector': '#password',
                'submit_selector': '#submit',
                'success_indicator': '.success'
            },
            'excel': {
                'input_file': './input.xlsx',
                'output_file': './output.xlsx',
                'sheet_name': 'Sheet1'
            }
        }
        
        is_valid, error = Validators.validate_config(config)
        assert is_valid == False
        assert 'Invalid login selectors' in error
