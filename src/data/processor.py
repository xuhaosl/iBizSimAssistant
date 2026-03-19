from typing import Dict, Any, List, Optional
import re
from datetime import datetime
from src.config.settings import Settings
from src.utils.logger import get_logger
from src.excel.writer import ExcelWriter


class DataProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = get_logger()
        self.excel_writer = None
    
    def clean_data(self, data: Any) -> Any:
        if isinstance(data, str):
            return data.strip()
        return data
    
    def convert_to_number(self, value: Any) -> Optional[float]:
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                cleaned = re.sub(r'[^\d.-]', '', value)
                if cleaned:
                    return float(cleaned)
            return None
        except (ValueError, TypeError):
            return None
    
    def convert_to_date(self, value: Any, date_format: str = '%Y-%m-%d') -> Optional[str]:
        try:
            if isinstance(value, str):
                date_obj = datetime.strptime(value, date_format)
                return date_obj.strftime(date_format)
            return None
        except (ValueError, TypeError):
            return None
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict):
            self.logger.error("Data must be a dictionary")
            return False
        
        for key, value in data.items():
            if value is None:
                self.logger.warning(f"Field {key} has None value")
        
        return True
    
    def transform_data(self, data: Dict[str, Any], 
                      transformations: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if transformations is None:
            return data
        
        transformed_data = {}
        
        for field_name, value in data.items():
            if field_name in transformations:
                transform_type = transformations[field_name]
                
                if transform_type == 'number':
                    transformed_data[field_name] = self.convert_to_number(value)
                elif transform_type == 'date':
                    transformed_data[field_name] = self.convert_to_date(value)
                elif transform_type == 'clean':
                    transformed_data[field_name] = self.clean_data(value)
                else:
                    transformed_data[field_name] = value
            else:
                transformed_data[field_name] = value
        
        return transformed_data
    
    def structure_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        structured_data = []
        
        for field_name, value in data.items():
            if value is not None:
                structured_data.append({
                    'field': field_name,
                    'value': value
                })
        
        return structured_data
    
    def write_to_excel(self, data: Dict[str, Any], 
                      output_file: Optional[str] = None,
                      sheet_name: Optional[str] = None) -> bool:
        try:
            if output_file is None:
                output_file = str(self.settings.get_output_file_path())
            
            if sheet_name is None:
                sheet_name = self.settings.get_sheet_name()
            
            if self.excel_writer is None:
                self.excel_writer = ExcelWriter(output_file)
            
            extraction_config = self.settings.extraction
            
            for field_config in extraction_config:
                field_name = field_config.get('name')
                target_cell = field_config.get('target_cell')
                
                if field_name in data and target_cell:
                    value = data[field_name]
                    self.excel_writer.write_cell(target_cell, value, sheet_name)
                    self.logger.info(f"Written {field_name} to {target_cell}: {value}")
            
            self.excel_writer.save()
            self.logger.info(f"Data successfully written to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write data to Excel: {e}")
            return False
    
    def process(self, data: Dict[str, Any], 
               transformations: Optional[Dict[str, str]] = None,
               write_to_excel: bool = True) -> Dict[str, Any]:
        try:
            if not self.validate_data(data):
                self.logger.error("Data validation failed")
                return data
            
            cleaned_data = {k: self.clean_data(v) for k, v in data.items()}
            
            if transformations:
                processed_data = self.transform_data(cleaned_data, transformations)
            else:
                processed_data = cleaned_data
            
            if write_to_excel:
                self.write_to_excel(processed_data)
            
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            return data
