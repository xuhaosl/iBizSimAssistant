import argparse
import sys
from pathlib import Path
from src.config.settings import Settings
from src.browser.browser_manager import BrowserManager
from src.browser.page_handler import PageHandler
from src.auth.login_handler import LoginHandler
from src.data.extractor import DataExtractor
from src.data.processor import DataProcessor
from src.excel.reader import ExcelReader
from src.utils.logger import get_logger


class iBizSimAssistant:
    def __init__(self, config_path: str = None):
        self.logger = get_logger()
        self.settings = Settings(config_path)
        self.browser_manager = None
        self.page_handler = None
        self.login_handler = None
        self.data_extractor = None
        self.data_processor = None
        self.excel_reader = None
    
    def initialize(self) -> bool:
        try:
            self.logger.info("Initializing iBizSimAssistant...")
            
            browser_config = self.settings.browser
            headless = browser_config.get('headless', False)
            timeout = browser_config.get('timeout', 30000)
            screenshot_on_error = browser_config.get('screenshot_on_error', True)
            
            self.browser_manager = BrowserManager(
                headless=headless,
                timeout=timeout,
                screenshot_on_error=screenshot_on_error
            )
            
            if not self.browser_manager.start():
                self.logger.error("Failed to start browser")
                return False
            
            page = self.browser_manager.get_page()
            if not page:
                self.logger.error("Failed to get page")
                return False
            
            self.page_handler = PageHandler(page)
            self.login_handler = LoginHandler(self.page_handler, self.settings)
            self.data_extractor = DataExtractor(self.page_handler, self.settings)
            self.data_processor = DataProcessor(self.settings)
            
            self.logger.info("Initialization completed successfully")
            return True
            
        except Exception as e:
            self.logger.exception(f"Initialization failed: {e}")
            return False
    
    def login(self) -> bool:
        try:
            self.logger.info("Starting login process...")
            return self.login_handler.login()
        except Exception as e:
            self.logger.exception(f"Login failed: {e}")
            return False
    
    def extract_data(self, page_url: str = None) -> dict:
        try:
            if page_url:
                full_url = self.settings.get_full_url(page_url)
                if not self.page_handler.navigate(full_url):
                    self.logger.error(f"Failed to navigate to {full_url}")
                    return {}
            
            data = self.data_extractor.extract_all()
            self.logger.info(f"Extracted {len(data)} data fields")
            return data
        except Exception as e:
            self.logger.exception(f"Data extraction failed: {e}")
            return {}
    
    def write_to_excel(self, data: dict) -> bool:
        try:
            self.logger.info("Writing data to Excel...")
            return self.data_processor.write_to_excel(data)
        except Exception as e:
            self.logger.exception(f"Failed to write to Excel: {e}")
            return False
    
    def read_from_excel(self) -> dict:
        try:
            self.logger.info("Reading data from Excel...")
            input_file = str(self.settings.get_input_file_path())
            sheet_name = self.settings.get_sheet_name()
            
            self.excel_reader = ExcelReader(input_file)
            
            with self.excel_reader:
                submission_config = self.settings.submission
                form_data = {}
                
                for field_config in submission_config:
                    excel_cell = field_config.get('excel_cell')
                    selector = field_config.get('selector')
                    
                    if excel_cell and selector:
                        value = self.excel_reader.read_cell(excel_cell, sheet_name)
                        form_data[selector] = value
                        self.logger.debug(f"Read {excel_cell}: {value}")
                
                self.logger.info(f"Read {len(form_data)} fields from Excel")
                return form_data
                
        except Exception as e:
            self.logger.exception(f"Failed to read from Excel: {e}")
            return {}
    
    def submit_to_web(self, page_url: str = None, form_data: dict = None) -> bool:
        try:
            if form_data is None:
                form_data = self.read_from_excel()
            
            if not form_data:
                self.logger.error("No form data to submit")
                return False
            
            if page_url:
                full_url = self.settings.get_full_url(page_url)
                if not self.page_handler.navigate(full_url):
                    self.logger.error(f"Failed to navigate to {full_url}")
                    return False
            
            submit_selector = self.settings.submission[0].get('submit_selector') if self.settings.submission else None
            
            if not submit_selector:
                self.logger.error("No submit selector configured")
                return False
            
            return self.page_handler.submit_form(form_data, submit_selector)
            
        except Exception as e:
            self.logger.exception(f"Failed to submit to web: {e}")
            return False
    
    def run_full_workflow(self) -> bool:
        try:
            self.logger.info("Starting full workflow...")
            
            if not self.initialize():
                return False
            
            if not self.login():
                self.logger.error("Login failed, aborting workflow")
                return False
            
            target_pages = self.settings.website.get('target_pages', [])
            
            if target_pages:
                for page_url in target_pages:
                    self.logger.info(f"Processing page: {page_url}")
                    
                    data = self.extract_data(page_url)
                    
                    if data:
                        self.write_to_excel(data)
            
            self.logger.info("Full workflow completed successfully")
            return True
            
        except Exception as e:
            self.logger.exception(f"Full workflow failed: {e}")
            return False
        finally:
            self.cleanup()
    
    def cleanup(self):
        try:
            self.logger.info("Cleaning up resources...")
            if self.browser_manager:
                self.browser_manager.stop()
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


def main():
    parser = argparse.ArgumentParser(description='iBizSimAssistant - Web Automation Assistant')
    parser.add_argument('--config', '-c', type=str, default=None,
                       help='Path to configuration file')
    parser.add_argument('--mode', '-m', type=str, default='full',
                       choices=['full', 'extract', 'submit'],
                       help='Operation mode: full, extract, or submit')
    parser.add_argument('--page', '-p', type=str, default=None,
                       help='Target page URL path')
    
    args = parser.parse_args()
    
    assistant = iBizSimAssistant(args.config)
    
    if args.mode == 'full':
        success = assistant.run_full_workflow()
    elif args.mode == 'extract':
        if not assistant.initialize():
            sys.exit(1)
        if not assistant.login():
            sys.exit(1)
        data = assistant.extract_data(args.page)
        if data:
            assistant.write_to_excel(data)
        success = bool(data)
    elif args.mode == 'submit':
        if not assistant.initialize():
            sys.exit(1)
        if not assistant.login():
            sys.exit(1)
        success = assistant.submit_to_web(args.page)
    else:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
