"""
完整流程测试脚本
测试从登录到数据提取的完整工作流程
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Settings
from src.browser.browser_manager import BrowserManager
from src.browser.page_handler import PageHandler
from src.auth.login_handler import LoginHandler
from src.data.extractor import DataExtractor
from src.data.processor import DataProcessor
from src.utils.logger import get_logger


def test_full_workflow():
    """
    测试完整工作流程
    
    步骤：
    1. 初始化配置
    2. 启动浏览器
    3. 登录
    4. 导航到目标页面
    5. 提取数据
    6. 关闭浏览器
    """
    logger = get_logger()
    logger.info("=" * 60)
    logger.info("完整工作流程测试")
    logger.info("=" * 60)
    
    try:
        logger.info("步骤 1: 初始化配置...")
        settings = Settings()
        logger.info(f"✓ 配置加载成功")
        logger.info(f"  - 网站: {settings.website.get('base_url')}")
        logger.info(f"  - 登录页面: {settings.website.get('login_url')}")
        
        logger.info("\n步骤 2: 启动浏览器...")
        browser_config = settings.browser
        headless = browser_config.get('headless', False)
        timeout = browser_config.get('timeout', 30000)
        screenshot_on_error = browser_config.get('screenshot_on_error', True)
        
        with BrowserManager(headless=headless, timeout=timeout, 
                        screenshot_on_error=screenshot_on_error) as browser_manager:
            logger.info("✓ 浏览器启动成功")
            
            page = browser_manager.get_page()
            if not page:
                logger.error("✗ 错误: 无法获取页面对象")
                return False
            
            logger.info("\n步骤 3: 执行登录...")
            page_handler = PageHandler(page)
            login_handler = LoginHandler(page_handler, settings)
            
            login_success = login_handler.login()
            
            if login_success:
                logger.info("✓ 登录成功")
                logger.info(f"  - 已登录: {login_handler.is_authenticated()}")
                
                logger.info("\n步骤 4: 导航到目标页面...")
                target_pages = settings.website.get('target_pages', [])
                
                if target_pages:
                    first_page = target_pages[0]
                    full_url = settings.get_full_url(first_page)
                    
                    if page_handler.navigate(full_url):
                        logger.info(f"✓ 导航到 {first_page}")
                        
                        logger.info("\n步骤 5: 提取数据...")
                        extractor = DataExtractor(page_handler, settings)
                        data = extractor.extract_all()
                        
                        logger.info(f"✓ 提取到 {len(data)} 个数据字段")
                        
                        for key, value in data.items():
                            logger.info(f"  - {key}: {value}")
                        
                        logger.info("\n步骤 6: 关闭浏览器...")
                        return True
                    else:
                        logger.warning("没有配置目标页面，跳过数据提取")
                        logger.info("\n步骤 6: 关闭浏览器...")
                        return True
            else:
                logger.error("✗ 登录失败")
                return False
                
    except Exception as e:
        logger.exception(f"测试过程中发生异常: {e}")
        return False


def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("iBizSimAssistant - 完整工作流程测试")
    print("=" * 60)
    print("\n此脚本将测试完整的工作流程：")
    print("  1. 初始化配置")
    print("  2. 启动浏览器")
    print("  3. 登录")
    print("  4. 导航到目标页面")
    print("  5. 提取数据")
    print("  6. 关闭浏览器")
    print("\n注意:")
    print("  - 需要正确的登录凭据")
    print("  - 需要正确的网站选择器配置")
    print("  - 浏览器会自动关闭")
    print("\n按 Enter 键开始测试...")
    input()
    
    success = test_full_workflow()
    
    print("\n" + "=" * 60)
    if success:
        print("测试结果: 成功 ✓")
    else:
        print("测试结果: 失败 ✗")
    print("=" * 60)
    
    print("\n日志文件位置: logs/")
    print("请查看日志文件了解详细信息\n")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
