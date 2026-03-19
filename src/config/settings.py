import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    def __init__(self, config_path=None):
        load_dotenv()
        
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        else:
            config_path = Path(config_path)
        
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path):
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @property
    def website(self):
        return self.config.get('website', {})
    
    @property
    def login(self):
        return self.config.get('login', {})
    
    @property
    def excel(self):
        return self.config.get('excel', {})
    
    @property
    def extraction(self):
        return self.config.get('extraction', [])
    
    @property
    def submission(self):
        return self.config.get('submission', [])
    
    @property
    def browser(self):
        return self.config.get('browser', {})
    
    @property
    def username(self):
        return os.getenv('USERNAME', '')
    
    @username.setter
    def username(self, value):
        os.environ['USERNAME'] = str(value) if value else ''
    
    @property
    def password(self):
        return os.getenv('PASSWORD', '')
    
    @password.setter
    def password(self, value):
        os.environ['PASSWORD'] = str(value) if value else ''
    
    @property
    def proxy_server(self):
        return os.getenv('PROXY_SERVER', '')
    
    @property
    def proxy_username(self):
        return os.getenv('PROXY_USERNAME', '')
    
    @property
    def proxy_password(self):
        return os.getenv('PROXY_PASSWORD', '')
    
    def get_full_url(self, path):
        base_url = self.website.get('base_url', '')
        if not base_url:
            self.logger.error(f"base_url is empty in configuration")
            raise ValueError("base_url is not configured in config.yaml")
        return f"{base_url}{path}"
    
    def get_input_file_path(self):
        return Path(self.excel.get('input_file', './data/input.xlsx'))
    
    def get_output_file_path(self):
        return Path(self.excel.get('output_file', './data/output.xlsx'))
    
    def get_sheet_name(self):
        return self.excel.get('sheet_name', 'Sheet1')
