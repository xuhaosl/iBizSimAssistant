@echo off
REM iBizSim 登录验证 GUI 工具启动脚本
REM 用于快速启动 login_gui.py，无需手动输入命令

echo ========================================
echo iBizSim 登录验证工具
echo ========================================
echo.
echo 正在启动图形界面...
echo.
echo 提示：
echo - 请在弹出的窗口中输入您的 iBizSim 账号和密码
echo - 点击"开始验证"按钮进行登录测试
echo - 可以在日志区域查看实时操作状态
echo.
echo ========================================
echo.

python login_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 程序已退出
    echo.
)

pause
