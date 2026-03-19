"""
环境测试脚本
用于验证 Python 环境和依赖是否正确安装
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    print("=" * 60)
    print("环境测试")
    print("=" * 60)
    
    print("\n测试 Python 模块导入...")
    
    errors = []
    
    try:
        import yaml
        print("✓ yaml 模块导入成功")
    except ImportError as e:
        print(f"✗ yaml 模块导入失败: {e}")
        errors.append("yaml")
    
    try:
        from dotenv import load_dotenv
        print("✓ dotenv 模块导入成功")
    except ImportError as e:
        print(f"✗ dotenv 模块导入失败: {e}")
        errors.append("dotenv")
    
    try:
        import playwright
        print("✓ playwright 模块导入成功")
    except ImportError as e:
        print(f"✗ playwright 模块导入失败: {e}")
        errors.append("playwright")
    
    try:
        import openpyxl
        print("✓ openpyxl 模块导入成功")
    except ImportError as e:
        print(f"✗ openpyxl 模块导入失败: {e}")
        errors.append("openpyxl")
    
    print("\n" + "-" * 60)
    
    if errors:
        print(f"\n⚠ 发现 {len(errors)} 个导入错误:")
        for error in errors:
            print(f"  - {error}")
        print("\n建议:")
        print("  1. 确保在虚拟环境中运行")
        print("  2. 检查依赖是否正确安装")
        print("  3. 尝试重新安装缺失的模块")
    else:
        print("\n✓ 所有核心模块导入成功！")
        print("\n测试结果:")
        print("  - Python 版本:", sys.version.split()[0])
        print("  - 环境路径:", sys.executable)
        print("  - 虚拟环境:", hasattr(sys, 'real_prefix'))
        print("\n可以运行 login_gui.py 了！")
    
    print("\n" + "=" * 60)
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(test_imports())
