"""
配置验证和修复脚本
用于检查并修复配置文件中的问题
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import yaml

def verify_and_fix_config():
    """
    验证并修复配置文件
    """
    config_path = Path(__file__).parent / "src" / "config" / "config.yaml"
    
    print("=" * 60)
    print("配置验证和修复工具")
    print("=" * 60)
    
    try:
        print("\n读取配置文件...")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✓ 配置文件读取成功")
        
        print("\n检查配置内容...")
        
        issues_found = False
        
        if 'website' not in config:
            print("✗ 错误: 缺少 website 配置")
            issues_found = True
        elif 'base_url' not in config.get('website', {}):
            print("✗ 错误: 缺少 base_url")
            issues_found = True
        elif config.get('website', {}).get('base_url', '').strip() == '':
            print("✗ 错误: base_url 为空")
            issues_found = True
        elif 'login_url' not in config.get('website', {}):
            print("✗ 错误: 缺少 login_url")
            issues_found = True
        elif config.get('website', {}).get('login_url', '').strip() == '':
            print("✗ 错误: login_url 为空")
            issues_found = True
        
        if not issues_found:
            print("✓ website 配置正确")
            print(f"  - base_url: {config.get('website', {}).get('base_url', '')}")
            print(f"  - login_url: {config.get('website', {}).get('login_url', '')}")
        
        if 'login' not in config:
            print("✗ 错误: 缺少 login 配置")
            issues_found = True
        elif 'username_selector' not in config.get('login', {}):
            print("✗ 错误: 缺少 username_selector")
            issues_found = True
        elif config.get('login', {}).get('username_selector', '').strip() == '':
            print("✗ 错误: username_selector 为空")
            issues_found = True
        
        if 'password_selector' not in config.get('login', {}):
            print("✗ 错误: 缺少 password_selector")
            issues_found = True
        elif config.get('login', {}).get('password_selector', '').strip() == '':
            print("✗ 错误: password_selector 为空")
            issues_found = True
        
        if 'submit_selector' not in config.get('login', {}):
            print("✗ 错误: 缺少 submit_selector")
            issues_found = True
        elif config.get('login', {}).get('submit_selector', '').strip() == '':
            print("✗ 错误: submit_selector 为空")
            issues_found = True
        
        if not issues_found:
            print("✓ login 配置正确")
            print(f"  - username_selector: {config.get('login', {}).get('username_selector', '')}")
            print(f"  - password_selector: {config.get('login', {}).get('password_selector', '')}")
            print(f"  - submit_selector: {config.get('login', {}).get('submit_selector', '')}")
        
        if 'excel' not in config:
            print("✗ 错误: 缺少 excel 配置")
            issues_found = True
        elif config.get('excel', {}).get('input_file', '').strip() == '':
            print("✗ 错误: input_file 为空")
            issues_found = True
        elif config.get('excel', {}).get('output_file', '').strip() == '':
            print("✗ 错误: output_file 为空")
            issues_found = True
        elif config.get('excel', {}).get('sheet_name', '').strip() == '':
            print("✗ 错误: sheet_name 为空")
            issues_found = True
        
        if not issues_found:
            print("✓ excel 配置正确")
            print(f"  - input_file: {config.get('excel', {}).get('input_file', '')}")
            print(f"  - output_file: {config.get('excel', {}).get('output_file', '')}")
            print(f"  - sheet_name: {config.get('excel', {}).get('sheet_name', '')}")
        
        if 'extraction' not in config:
            print("✗ 错误: 缺少 extraction 配置")
            issues_found = True
        elif not isinstance(config.get('extraction', []), list):
            print("✗ 错误: extraction 不是列表")
            issues_found = True
        
        if 'submission' not in config:
            print("✗ 错误: 缺少 submission 配置")
            issues_found = True
        elif not isinstance(config.get('submission', []), list):
            print("✗ 错误: submission 不是列表")
            issues_found = True
        
        if 'browser' not in config:
            print("✗ 错误: 缺少 browser 配置")
            issues_found = True
        elif config.get('browser', {}).get('headless', '') == '':
            print("✗ 错误: headless 为空")
            issues_found = True
        elif config.get('browser', {}).get('timeout', '') == '':
            print("✗ 错误: timeout 为空")
            issues_found = True
        
        if not issues_found:
            print("\n✓ 配置文件验证通过！")
            print("\n当前配置:")
            print(yaml.dump(config, allow_unicode=True, default_flow_style=False))
            return True
        else:
            print("\n✗ 发现配置问题，请检查上述错误")
            return False
    
    except Exception as e:
        print(f"\n✗ 验证过程中发生异常: {e}")
        return False


if __name__ == '__main__':
    success = verify_and_fix_config()
    
    print("\n" + "=" * 60)
    if success:
        print("配置文件验证完成！")
        print("可以运行 login_gui.py 了")
    else:
        print("配置文件存在错误，请修复后重试")
    
    print("=" * 60)
    
    sys.exit(0 if success else 1)
