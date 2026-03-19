import pytest
from unittest.mock import Mock, patch, MagicMock
from src.auth.login_handler import LoginHandler
from src.config.settings import Settings


@pytest.fixture
def mock_page_handler():
    return Mock()


@pytest.fixture
def mock_settings():
    settings = Mock(spec=Settings)
    settings.login = {
        'username_selector': '#username',
        'password_selector': '#password',
        'submit_selector': '#login-btn',
        'success_indicator': '.user-profile'
    }
    settings.username = 'test_user'
    settings.password = 'test_pass'
    settings.get_full_url = Mock(return_value='https://example.com/login')
    return settings


@pytest.fixture
def login_handler(mock_page_handler, mock_settings):
    return LoginHandler(mock_page_handler, mock_settings)


class TestLoginHandler:
    
    def test_init(self, login_handler, mock_page_handler, mock_settings):
        assert login_handler.page_handler == mock_page_handler
        assert login_handler.settings == mock_settings
        assert login_handler.is_logged_in == False
    
    def test_login_success(self, login_handler, mock_page_handler, mock_settings):
        mock_page_handler.navigate.return_value = True
        mock_page_handler.wait_for_element.return_value = True
        mock_page_handler.fill.return_value = True
        mock_page_handler.click.return_value = True
        
        result = login_handler.login()
        
        assert result == True
        assert login_handler.is_logged_in == True
        mock_page_handler.navigate.assert_called_once_with('https://example.com/login')
        mock_page_handler.fill.assert_any_call('#username', 'test_user')
        mock_page_handler.fill.assert_any_call('#password', 'test_pass')
        mock_page_handler.click.assert_called_once_with('#login-btn')
    
    def test_login_missing_credentials(self, login_handler, mock_settings):
        mock_settings.username = ''
        mock_settings.password = ''
        
        result = login_handler.login()
        
        assert result == False
        assert login_handler.is_logged_in == False
    
    def test_login_navigation_failure(self, login_handler, mock_page_handler):
        mock_page_handler.navigate.return_value = False
        
        result = login_handler.login()
        
        assert result == False
        assert login_handler.is_logged_in == False
    
    def test_login_element_not_found(self, login_handler, mock_page_handler):
        mock_page_handler.navigate.return_value = True
        mock_page_handler.wait_for_element.return_value = False
        
        result = login_handler.login()
        
        assert result == False
        assert login_handler.is_logged_in == False
    
    def test_login_no_success_indicator(self, login_handler, mock_page_handler, mock_settings):
        mock_settings.login['success_indicator'] = None
        mock_page_handler.navigate.return_value = True
        mock_page_handler.wait_for_element.return_value = True
        mock_page_handler.fill.return_value = True
        mock_page_handler.click.return_value = True
        
        result = login_handler.login()
        
        assert result == True
        assert login_handler.is_logged_in == True
    
    def test_logout(self, login_handler):
        login_handler.is_logged_in = True
        
        result = login_handler.logout()
        
        assert result == True
        assert login_handler.is_logged_in == False
    
    def test_is_authenticated(self, login_handler):
        assert login_handler.is_authenticated() == False
        
        login_handler.is_logged_in = True
        assert login_handler.is_authenticated() == True
    
    def test_handle_captcha(self, login_handler, capsys):
        with patch('builtins.input', return_value=''):
            result = login_handler.handle_captcha()
            
            assert result == True
            captured = capsys.readouterr()
            assert 'manual intervention' in captured.out.lower()
