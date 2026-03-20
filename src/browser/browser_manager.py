from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional
from src.utils.logger import get_logger


class BrowserManager:
    def __init__(self, headless: bool = False, timeout: int = 30000, 
                 screenshot_on_error: bool = True):
        self.headless = headless
        self.timeout = timeout
        self.screenshot_on_error = screenshot_on_error
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.logger = get_logger()
    
    def start(self):
        try:
            self.logger.info("Starting browser...")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=['--start-minimized', '--no-first-run', '--no-default-browser-check', '--disable-blink-features=AutomationControlled']
            )
            self.context = self.browser.new_context()
            self.context.set_default_timeout(self.timeout)
            self.page = self.context.new_page()
            self.logger.info("Browser started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            self.stop()
            return False
    
    def stop(self):
        try:
            if self.page:
                self.page.close()
                self.logger.info("Page closed")
            if self.context:
                self.context.close()
                self.logger.info("Browser context closed")
            if self.browser:
                self.browser.close()
                self.logger.info("Browser closed")
            if self.playwright:
                self.playwright.stop()
                self.logger.info("Playwright stopped")
        except Exception as e:
            self.logger.error(f"Error while stopping browser: {e}")
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None
    
    def get_page(self) -> Optional[Page]:
        return self.page
    
    def get_context(self) -> Optional[BrowserContext]:
        return self.context
    
    def get_browser(self) -> Optional[Browser]:
        return self.browser
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        if self.page and self.screenshot_on_error:
            try:
                self.page.screenshot(path=filename)
                self.logger.info(f"Screenshot saved to {filename}")
            except Exception as e:
                self.logger.error(f"Failed to take screenshot: {e}")
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self.screenshot_on_error:
            self.take_screenshot()
        self.stop()
