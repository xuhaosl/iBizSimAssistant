"""
简单配置检查脚本
直接读取配置文件，不依赖Settings类
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import yaml

def check_config():
    """
    直接读取并检查配置文件
    """
    config_path = Path(__file__).parent / "src" / "config" / "config.yaml"
    
    print("=" * 60)
    print("配置文件直接检查")
    print("=" * 60)
    
    try:
        print("\n读取配置文件...")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✓ 配置文件读取成功")
        
        print("\n检查关键配置...")
        
        website = config.get('website', {})
        if website:
            base_url = website.get('base_url', '')
            login_url = website.get('login_url', '')
            print(f"✓ base_url: '{base_url}'")
            print(f"✓ login_url: '{login_url}'")
            
            full_url = f"{base_url}{login_url}"
            print(f"✓ 完整URL: '{full_url}'")
            
            if 'none' in full_url.lower():
                print("✗ 警告: URL中包含 'none'")
            else:
                print("✓ URL格式正确")
        else:
            print("✗ 错误: 缺少 website 配置")
        
        login = config.get('login', {})
        if login:
            username_selector = login.get('username_selector', '')
            password_selector = login.get('password_selector', '')
            print(f"✓ username_selector: '{username_selector}'")
            print(f"✓ password_selector: '{password_selector}'")
        else:
            print("✗ 错误: 缺少 login 配置")
        
        print("\n" + "-" * 60)
        print("请检查上述输出")
        print("如果URL包含 'none'，说明配置文件有问题")
        print("=" * 60)
        
        return 'none' not in full_url.lower()
    
    except Exception as e:
        print(f"\n✗ 检查过程中发生异常: {e}")
        return False


if __name__ == '__main__':
    result = check_config()
    
    print("\n" + "=" * 60)
    if result:
        print("配置文件检查通过！")
        print("建议：")
        print("1. 如果URL包含 'none'，请手动编辑配置文件")
        print("2. 退出虚拟环境并重新激活")
        print("3. 清理Python缓存: 删除 __pycache__ 目录")
    else:
        print("配置文件存在问题")
    
    print("=" * 60)
    
    sys.exit(0 if result else 1)
