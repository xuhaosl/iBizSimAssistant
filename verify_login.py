"""
登录功能验证脚本
用于测试和验证网站登录功能是否正常工作
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Settings
from src.browser.browser_manager import BrowserManager
from src.browser.page_handler import PageHandler
from src.auth.login_handler import LoginHandler
from src.utils.logger import get_logger


def test_login(username=None, password=None):
    """
    测试登录功能
    
    步骤：
    1. 加载配置
    2. 启动浏览器
    3. 执行登录
    4. 验证登录状态
    5. 关闭浏览器
    
    Args:
        username: 用户名（如果为None则从环境变量读取）
        password: 密码（如果为None则从环境变量读取）
    """
    logger = get_logger()
    logger.info("=" * 60)
    logger.info("开始登录功能验证测试")
    logger.info("=" * 60)
    
    try:
        logger.info("步骤 1: 加载配置文件...")
        settings = Settings()
        
        logger.info("✓ 配置加载成功")
        logger.info(f"  - 网站: {settings.website.get('base_url')}")
        logger.info(f"  - 登录页面: {settings.website.get('login_url')}")
        
        logger.info("\n步骤 2: 获取登录凭据...")
        
        if username is None:
            username = settings.username
            if username:
                logger.info(f"  - 使用环境变量中的用户名: {username[:3]}***")
            else:
                logger.info("  - 环境变量中未设置用户名")
        
        if password is None:
            password = settings.password
            if password:
                logger.info("  - 使用环境变量中的密码: ***")
            else:
                logger.info("  - 环境变量中未设置密码")
        
        if not username or not password:
            logger.warning("⚠ 用户名或密码未设置")
            logger.info("  - 将使用命令行输入的凭据")
        
        logger.info("✓ 登录凭据获取完成")
        
        logger.info("\n步骤 3: 启动浏览器...")
        browser_config = settings.browser
        headless = browser_config.get('headless', False)
        timeout = browser_config.get('timeout', 30000)
        screenshot_on_error = browser_config.get('screenshot_on_error', True)
        
        logger.info(f"  - 无头模式: {headless}")
        logger.info(f"  - 超时时间: {timeout}ms")
        logger.info(f"  - 错误截图: {screenshot_on_error}")
        
        with BrowserManager(headless=headless, timeout=timeout, 
                        screenshot_on_error=screenshot_on_error) as browser_manager:
            logger.info("✓ 浏览器启动成功")
            
            page = browser_manager.get_page()
            if not page:
                logger.error("✗ 错误: 无法获取页面对象")
                return False
            
            logger.info("\n步骤 4: 初始化登录处理器...")
            
            if username and password:
                logger.info("  - 使用提供的登录凭据")
                settings.username = username
                settings.password = password
            
            login_handler = LoginHandler(PageHandler(page), settings)
            logger.info("✓ 登录处理器初始化成功")
            
            logger.info("\n步骤 5: 执行登录操作...")
            logger.info("  - 导航到登录页面...")
            logger.info("  - 填写用户名...")
            logger.info("  - 填写密码...")
            logger.info("  - 点击登录按钮...")
            
            login_success = login_handler.login()
            
            if login_success:
                logger.info("\n" + "=" * 60)
                logger.info("✓✓✓ 登录验证成功！✓✓✓")
                logger.info("=" * 60)
                logger.info("\n登录状态:")
                logger.info(f"  - 已登录: {login_handler.is_authenticated()}")
                logger.info(f"  - 当前页面: {page.url}")
                
                logger.info("\n提示:")
                logger.info("  1. 浏览器窗口将在 5 秒后关闭")
                logger.info("  2. 你可以在这段时间内手动验证登录状态")
                logger.info("  3. 查看浏览器窗口确认是否成功登录")
                
                logger.info("\n等待 5 秒...")
                page.wait_for_timeout(5000)
                
                logger.info("✓ 测试完成")
                return True
            else:
                logger.error("\n" + "=" * 60)
                logger.error("✗✗✗ 登录验证失败！✗✗✗")
                logger.error("=" * 60)
                logger.error("\n可能的原因:")
                logger.error("  1. 用户名或密码错误")
                logger.error("  2. 网站选择器配置错误")
                logger.error("  3. 网络连接问题")
                logger.error("  4. 网站登录页面已更改")
                logger.error("  5. 需要验证码")
                
                logger.error("\n建议:")
                logger.error("  1. 检查输入的用户名和密码是否正确")
                logger.error("  2. 检查 config.yaml 中的选择器配置")
                logger.error("  3. 查看日志文件了解详细错误信息")
                logger.error("  4. 尝试将 headless 设置为 false 以观察浏览器")
                
                return False
                
    except Exception as e:
        logger.exception(f"\n✗ 测试过程中发生异常: {e}")
        logger.error("\n请检查:")
        logger.error("  1. 配置文件是否正确")
        logger.error("  2. 依赖包是否已安装")
        logger.error("  3. Playwright 浏览器是否已安装")
        logger.error("  4. 日志文件中的详细错误信息")
        return False


def main():
    """
    主函数
    """
    print("\n" + "=" * 60)
    print("iBizSimAssistant - 登录功能验证工具")
    print("=" * 60)
    print("\n此工具将测试网站的登录功能")
    print("\n目标网站: https://www.ibizsim.cn")
    print("登录页面: /main/login")
    print("\n请选择登录方式:")
    print("  1. 使用命令行输入账号密码")
    print("  2. 使用 .env 文件中的账号密码（如果已配置）")
    print("\n推荐: 使用命令行输入，更安全方便")
    
    print("\n" + "-" * 60)
    
    username_input = input("请输入用户名: ").strip()
    password_input = input("请输入密码: ").strip()
    
    if not username_input or not password_input:
        print("\n⚠ 警告: 用户名或密码为空")
        print("将使用 .env 文件中的配置（如果存在）\n")
        username = None
        password = None
    else:
        username = username_input
        password = password_input
        print("\n✓ 已获取登录凭据")
    
    print("\n按 Enter 键开始测试...")
    input()
    
    success = test_login(username, password)
    
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
