import re
from typing import Any, Optional


class Validators:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def is_valid_cell_reference(cell_ref: str) -> bool:
        pattern = r'^[A-Z]+[0-9]+$'
        return re.match(pattern, cell_ref) is not None
    
    @staticmethod
    def is_valid_selector(selector: str) -> bool:
        return len(selector) > 0
    
    @staticmethod
    def is_not_empty(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return True
    
    @staticmethod
    def is_positive_number(value: Any) -> bool:
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_config(config: dict) -> tuple[bool, Optional[str]]:
        if not config:
            return False, "Configuration is empty"
        
        required_keys = ['website', 'login', 'excel']
        for key in required_keys:
            if key not in config:
                return False, f"Missing required key: {key}"
        
        website = config.get('website', {})
        if not Validators.is_valid_url(website.get('base_url', '')):
            return False, "Invalid base_url in website configuration"
        
        login = config.get('login', {})
        if not all([
            Validators.is_valid_selector(login.get('username_selector', '')),
            Validators.is_valid_selector(login.get('password_selector', '')),
            Validators.is_valid_selector(login.get('submit_selector', ''))
        ]):
            return False, "Invalid login selectors"
        
        return True, None
