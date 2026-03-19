from typing import Optional
from src.browser.page_handler import PageHandler
from src.config.settings import Settings
from src.utils.logger import get_logger
from src.utils.retry import retry


class LoginHandler:
    def __init__(self, page_handler: PageHandler, settings: Settings):
        self.page_handler = page_handler
        self.settings = settings
        self.logger = get_logger()
        self.is_logged_in = False
    
    @retry(max_attempts=3, delay=2.0, exceptions=(Exception,))
    def login(self) -> bool:
        try:
            self.logger.info("Starting login process...")
            
            login_url = self.settings.get_full_url(self.settings.website.get('login_url'))
            
            if not self.page_handler.navigate(login_url):
                self.logger.error("Failed to navigate to login page")
                return False
            
            username_selector = self.settings.login.get('username_selector')
            password_selector = self.settings.login.get('password_selector')
            submit_selector = self.settings.login.get('submit_selector')
            
            if not all([username_selector, password_selector, submit_selector]):
                self.logger.error("Missing login selectors in configuration")
                return False
            
            if not self.page_handler.wait_for_element(username_selector):
                self.logger.error(f"Username field not found: {username_selector}")
                return False
            
            username = self.settings.username
            password = self.settings.password
            
            if not username or not password:
                self.logger.error("Username or password not provided in environment variables")
                return False
            
            if not self.page_handler.fill(username_selector, username):
                self.logger.error("Failed to fill username")
                return False
            
            if not self.page_handler.fill(password_selector, password):
                self.logger.error("Failed to fill password")
                return False
            
            if not self.page_handler.click(submit_selector):
                self.logger.error("Failed to click submit button")
                return False
            
            self.logger.info("Login form submitted")
            
            success_indicator = self.settings.login.get('success_indicator')
            if success_indicator:
                if self.page_handler.wait_for_element(success_indicator, timeout=10000):
                    self.logger.info("Login successful - success indicator found")
                    self.is_logged_in = True
                    return True
                else:
                    self.logger.error("Login failed - success indicator not found")
                    return False
            else:
                self.logger.info("No success indicator configured, assuming login successful")
                self.is_logged_in = True
                return True
                
        except Exception as e:
            self.logger.exception(f"Login process failed: {e}")
            return False
    
    def logout(self) -> bool:
        try:
            self.logger.info("Logging out...")
            self.is_logged_in = False
            self.logger.info("Logout completed")
            return True
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            return False
    
    def is_authenticated(self) -> bool:
        return self.is_logged_in
    
    def handle_captcha(self) -> bool:
        self.logger.warning("Captcha detected - manual intervention required")
        self.logger.info("Please solve the captcha manually and press Enter to continue...")
        input()
        return True
