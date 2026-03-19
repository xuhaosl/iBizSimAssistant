from typing import List, Dict, Any, Optional
from src.browser.page_handler import PageHandler
from src.config.settings import Settings
from src.utils.logger import get_logger
from src.utils.retry import retry


class DataExtractor:
    def __init__(self, page_handler: PageHandler, settings: Settings):
        self.page_handler = page_handler
        self.settings = settings
        self.logger = get_logger()
    
    def extract_all(self) -> Dict[str, Any]:
        extraction_config = self.settings.extraction
        if not extraction_config:
            self.logger.warning("No extraction configuration found")
            return {}
        
        extracted_data = {}
        
        for field_config in extraction_config:
            field_name = field_config.get('name')
            selector = field_config.get('selector')
            data_type = field_config.get('type', 'text')
            
            if not field_name or not selector:
                self.logger.warning(f"Invalid field configuration: {field_config}")
                continue
            
            try:
                if data_type == 'text':
                    value = self._extract_text(selector)
                elif data_type == 'attribute':
                    attribute = field_config.get('attribute', 'value')
                    value = self._extract_attribute(selector, attribute)
                elif data_type == 'table':
                    value = self._extract_table(selector)
                elif data_type == 'list':
                    value = self._extract_list(selector)
                else:
                    self.logger.warning(f"Unknown data type: {data_type}")
                    continue
                
                extracted_data[field_name] = value
                self.logger.info(f"Extracted {field_name}: {value}")
                
            except Exception as e:
                self.logger.error(f"Failed to extract {field_name}: {e}")
                extracted_data[field_name] = None
        
        return extracted_data
    
    def _extract_text(self, selector: str) -> Optional[str]:
        text = self.page_handler.get_text(selector)
        if text is not None:
            return text.strip()
        return None
    
    def _extract_attribute(self, selector: str, attribute: str) -> Optional[str]:
        return self.page_handler.get_attribute(selector, attribute)
    
    def _extract_table(self, selector: str) -> List[List[str]]:
        try:
            rows = self.page_handler.page.locator(f"{selector} tr").all()
            table_data = []
            
            for row in rows:
                cells = row.locator("td, th").all()
                row_data = [cell.inner_text().strip() for cell in cells]
                table_data.append(row_data)
            
            self.logger.info(f"Extracted table with {len(table_data)} rows")
            return table_data
            
        except Exception as e:
            self.logger.error(f"Failed to extract table: {e}")
            return []
    
    def _extract_list(self, selector: str) -> List[str]:
        try:
            elements = self.page_handler.page.locator(selector).all()
            items = [element.inner_text().strip() for element in elements]
            self.logger.info(f"Extracted list with {len(items)} items")
            return items
        except Exception as e:
            self.logger.error(f"Failed to extract list: {e}")
            return []
    
    def extract_by_selector(self, selector: str, data_type: str = 'text', 
                           attribute: Optional[str] = None) -> Any:
        try:
            if data_type == 'text':
                return self._extract_text(selector)
            elif data_type == 'attribute':
                return self._extract_attribute(selector, attribute or 'value')
            elif data_type == 'table':
                return self._extract_table(selector)
            elif data_type == 'list':
                return self._extract_list(selector)
            else:
                self.logger.warning(f"Unknown data type: {data_type}")
                return None
        except Exception as e:
            self.logger.error(f"Failed to extract by selector {selector}: {e}")
            return None
    
    def wait_and_extract(self, selector: str, data_type: str = 'text',
                        timeout: int = 10000) -> Optional[Any]:
        if not self.page_handler.wait_for_element(selector, timeout=timeout):
            self.logger.error(f"Element not found within timeout: {selector}")
            return None
        
        return self.extract_by_selector(selector, data_type)
