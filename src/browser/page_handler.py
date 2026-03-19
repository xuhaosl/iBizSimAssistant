from playwright.sync_api import Page, Locator
from typing import Optional, List, Dict, Any
from src.utils.logger import get_logger


class PageHandler:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger()
    
    def navigate(self, url: str, wait_until: str = "networkidle") -> bool:
        try:
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until=wait_until)
            self.logger.info("Navigation completed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    def click(self, selector: str, timeout: Optional[int] = None) -> bool:
        try:
            self.logger.debug(f"Clicking element: {selector}")
            self.page.click(selector, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Failed to click element {selector}: {e}")
            return False
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> bool:
        try:
            self.logger.debug(f"Filling element {selector} with value: {value}")
            self.page.fill(selector, value, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Failed to fill element {selector}: {e}")
            return False
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> Optional[str]:
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            text = element.inner_text()
            self.logger.debug(f"Retrieved text from {selector}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from {selector}: {e}")
            return None
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            attr_value = element.get_attribute(attribute)
            self.logger.debug(f"Retrieved attribute {attribute} from {selector}: {attr_value}")
            return attr_value
        except Exception as e:
            self.logger.error(f"Failed to get attribute {attribute} from {selector}: {e}")
            return None
    
    def wait_for_element(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> bool:
        try:
            self.logger.debug(f"Waiting for element {selector} to be {state}")
            self.page.wait_for_selector(selector, state=state, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Element {selector} not found: {e}")
            return False
    
    def is_visible(self, selector: str) -> bool:
        try:
            element = self.page.locator(selector)
            return element.is_visible()
        except Exception:
            return False
    
    def is_enabled(self, selector: str) -> bool:
        try:
            element = self.page.locator(selector)
            return element.is_enabled()
        except Exception:
            return False
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None) -> bool:
        try:
            self.logger.debug(f"Selecting option {value} in {selector}")
            self.page.select_option(selector, value=value, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Failed to select option in {selector}: {e}")
            return False
    
    def check(self, selector: str, timeout: Optional[int] = None) -> bool:
        try:
            self.logger.debug(f"Checking checkbox {selector}")
            self.page.check(selector, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Failed to check {selector}: {e}")
            return False
    
    def uncheck(self, selector: str, timeout: Optional[int] = None) -> bool:
        try:
            self.logger.debug(f"Unchecking checkbox {selector}")
            self.page.uncheck(selector, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Failed to uncheck {selector}: {e}")
            return False
    
    def get_all_text(self, selector: str) -> List[str]:
        try:
            elements = self.page.locator(selector).all()
            texts = [element.inner_text() for element in elements]
            self.logger.debug(f"Retrieved {len(texts)} elements from {selector}")
            return texts
        except Exception as e:
            self.logger.error(f"Failed to get all text from {selector}: {e}")
            return []
    
    def evaluate(self, script: str) -> Any:
        try:
            result = self.page.evaluate(script)
            self.logger.debug(f"Evaluated script: {script[:50]}...")
            return result
        except Exception as e:
            self.logger.error(f"Failed to evaluate script: {e}")
            return None
    
    def get_page_title(self) -> str:
        try:
            title = self.page.title()
            self.logger.debug(f"Page title: {title}")
            return title
        except Exception as e:
            self.logger.error(f"Failed to get page title: {e}")
            return ""
    
    def get_current_url(self) -> str:
        try:
            url = self.page.url
            self.logger.debug(f"Current URL: {url}")
            return url
        except Exception as e:
            self.logger.error(f"Failed to get current URL: {e}")
            return ""
    
    def reload(self, wait_until: str = "networkidle") -> bool:
        try:
            self.logger.info("Reloading page")
            self.page.reload(wait_until=wait_until)
            return True
        except Exception as e:
            self.logger.error(f"Failed to reload page: {e}")
            return False
    
    def go_back(self) -> bool:
        try:
            self.logger.info("Going back")
            self.page.go_back()
            return True
        except Exception as e:
            self.logger.error(f"Failed to go back: {e}")
            return False
    
    def go_forward(self) -> bool:
        try:
            self.logger.info("Going forward")
            self.page.go_forward()
            return True
        except Exception as e:
            self.logger.error(f"Failed to go forward: {e}")
            return False
    
    def wait_for_timeout(self, timeout: int):
        self.logger.debug(f"Waiting for {timeout}ms")
        self.page.wait_for_timeout(timeout)
    
    def submit_form(self, form_data: Dict[str, Any], submit_selector: str) -> bool:
        try:
            self.logger.info("Submitting form...")
            
            for field_selector, value in form_data.items():
                if value is None:
                    self.logger.warning(f"Skipping field {field_selector} with None value")
                    continue
                
                if not self.fill(field_selector, str(value)):
                    self.logger.error(f"Failed to fill field {field_selector}")
                    return False
            
            if not self.click(submit_selector):
                self.logger.error("Failed to click submit button")
                return False
            
            self.logger.info("Form submitted successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to submit form: {e}")
            return False
