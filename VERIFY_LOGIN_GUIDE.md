# iBizSim 登录功能验证指南

## 概述

`verify_login.py` 是一个独立的验证脚本，用于测试和验证 iBizSim 网站的登录功能是否正常工作。

## 目标网站信息

- **网站地址**: https://www.ibizsim.cn
- **登录页面**: /main/login
- **主要功能**: 企业竞争模拟系统

## 使用前准备

### 1. 配置环境变量

在项目根目录下创建 `.env` 文件（如果还没有的话），并填入你的登录凭据：

```env
USERNAME=your_username
PASSWORD=your_password
```

**重要**: 确保 `.env` 文件不会被提交到版本控制系统（已在 .gitignore 中配置）。

### 2. 配置网站信息

编辑 `src/config/config.yaml` 文件，设置正确的网站信息：

```yaml
website:
  base_url: "https://www.ibizsim.cn"
  login_url: "/main/login"
  target_pages:
    - "/main/index"
    - "/main/decision"

login:
  username_selector: "#username"      # 用户名输入框的选择器
  password_selector: "#password"      # 密码输入框的选择器
  submit_selector: "#login-btn"        # 登录按钮的选择器
  success_indicator: ".user-profile"   # 登录成功后的元素选择器

browser:
  headless: false                  # 建议先设为 false，方便观察
  timeout: 30000
  screenshot_on_error: true
```

**注意**: 上述选择器是示例配置，你需要根据实际的 iBizSim 网站登录页面结构进行调整。

### 如何获取 iBizSim 网站的正确选择器

1. **访问登录页面**
   - 在浏览器中打开 https://www.ibizsim.cn/main/login
   - 使用开发者工具（F12）查看页面结构

2. **查找登录表单元素**
   - 找到用户名输入框
   - 找到密码输入框
   - 找到登录按钮
   - 找到登录成功后的页面元素

3. **获取元素选择器**
   - 右键点击元素
   - 选择"检查"或"检查元素"
   - 在开发者工具中找到元素
   - 右键点击元素，选择"Copy" → "Copy selector"
   - 将选择器更新到 config.yaml 中

4. **常见的选择器模式**
   ```yaml
   # ID 选择器（最推荐）
   username_selector: "#username"
   password_selector: "#password"
   
   # Class 选择器
   username_selector: ".username-input"
   password_selector: ".password-input"
   
   # Name 属性选择器
   username_selector: "[name='username']"
   password_selector: "[name='password']"
   
   # Type 属性选择器
   username_selector: "input[type='text']"
   password_selector: "input[type='password']"
   ```

### 3. 安装依赖

确保已安装所有必要的依赖：

```bash
pip install -r requirements.txt
```

### 4. 安装 Playwright 浏览器

```bash
playwright install chromium
```

## 运行验证脚本

### 方式一：直接运行

```bash
python verify_login.py
```

### 方式二：使用 Python 运行

```bash
python -m verify_login
```

## 验证流程

脚本将按以下步骤执行验证：

### 步骤 1: 加载配置
- ✓ 检查 config.yaml 文件是否存在
- ✓ 解析配置文件
- ✓ 显示网站URL和登录页面路径

### 步骤 2: 检查环境变量
- ✓ 验证 USERNAME 是否设置
- ✓ 验证 PASSWORD 是否设置
- ✓ 如果未设置，提示用户配置

### 步骤 3: 启动浏览器
- ✓ 初始化 Playwright 浏览器
- ✓ 根据配置设置无头/有头模式
- ✓ 配置超时时间和错误截图

### 步骤 4: 初始化登录处理器
- ✓ 创建 PageHandler 实例
- ✓ 创建 LoginHandler 实例
- ✓ 准备执行登录操作

### 步骤 5: 执行登录操作
- ✓ 导航到登录页面
- ✓ 等待用户名字段出现
- ✓ 填写用户名
- ✓ 填写密码
- ✓ 点击登录按钮
- ✓ 等待登录成功指示器

### 步骤 6: 验证登录状态
- ✓ 检查登录处理器状态
- ✓ 显示当前页面URL
- ✓ 等待5秒供用户手动验证

## 验证结果

### 成功情况

如果登录成功，你将看到：

```
============================================================
✓✓✓ 登录验证成功！✓✓✓
============================================================

登录状态:
  - 已登录: True
  - 当前页面: https://your-website.com/dashboard

提示:
  1. 浏览器窗口将在 5 秒后关闭
  2. 你可以在这段时间内手动验证登录状态
  3. 查看浏览器窗口确认是否成功登录

等待 5 秒...
✓ 测试完成

============================================================
测试结果: 成功 ✓
============================================================
```

### 失败情况

如果登录失败，你将看到：

```
============================================================
✗✗✗ 登录验证失败！✗✗✗
============================================================

可能的原因:
  1. 用户名或密码错误
  2. 网站选择器配置错误
  3. 网络连接问题
  4. 网站登录页面已更改
  5. 需要验证码

建议:
  1. 检查 .env 文件中的用户名和密码
  2. 检查 config.yaml 中的选择器配置
  3. 查看日志文件了解详细错误信息
  4. 尝试将 headless 设置为 false 以观察浏览器

============================================================
测试结果: 失败 ✗
============================================================
```

## 常见问题排查

### 问题 1: 找不到配置文件

**错误信息**: `Config file not found`

**解决方案**:
- 确认 `src/config/config.yaml` 文件存在
- 检查文件路径是否正确

### 问题 2: 用户名或密码未设置

**错误信息**: `Username or password not provided in environment variables`

**解决方案**:
- 创建 `.env` 文件
- 填入正确的 USERNAME 和 PASSWORD
- 确保 `.env` 文件在项目根目录

### 问题 3: 元素选择器错误

**错误信息**: `Username field not found` 或 `Failed to click submit button`

**解决方案**:
- 使用浏览器开发者工具检查元素选择器
- 更新 `config.yaml` 中的选择器配置
- 尝试将 `headless` 设为 `false` 观察页面

### 问题 4: 登录超时

**错误信息**: `Element not found within timeout`

**解决方案**:
- 增加 `config.yaml` 中的 `timeout` 值
- 检查网络连接
- 确认页面加载速度

### 问题 5: Playwright 浏览器未安装

**错误信息**: `Executable doesn't exist` 或类似的浏览器错误

**解决方案**:
```bash
playwright install chromium
```

## 如何获取正确的选择器

### 使用浏览器开发者工具

1. 在浏览器中打开登录页面
2. 右键点击用户名输入框
3. 选择"检查"或"检查元素"
4. 在开发者工具中找到元素的 HTML
5. 右键点击元素，选择"Copy" → "Copy selector"
6. 将选择器粘贴到 `config.yaml` 中

### 常见选择器示例

```yaml
# ID 选择器
username_selector: "#username"

# Class 选择器
username_selector: ".username-input"

# 属性选择器
username_selector: "[name='username']"

# 组合选择器
username_selector: "form input[type='text']"
```

## 日志查看

所有日志都保存在 `logs/` 目录下，文件名格式为 `ibizsim_YYYYMMDD_HHMMSS.log`。

查看最新日志：
```bash
# Windows
type logs\ibizsim_*.log | more

# Linux/Mac
tail -f logs/ibizsim_*.log
```

## 下一步

登录验证成功后，你可以：

1. **测试数据提取功能**
   ```bash
   python src/main.py --mode extract --page "/target-page"
   ```

2. **测试完整工作流程**
   ```bash
   python src/main.py --mode full
   ```

3. **测试数据提交功能**
   ```bash
   python src/main.py --mode submit --page "/form-page"
   ```

## 注意事项

1. **安全性**: 不要将 `.env` 文件提交到版本控制系统
2. **隐私**: 日志文件中不会记录密码，但会记录用户名的前3位
3. **性能**: 首次运行时，Playwright 会下载浏览器驱动，可能需要一些时间
4. **网络**: 确保网络连接稳定，能够访问目标网站
5. **兼容性**: 某些网站可能有反爬虫机制，可能需要额外处理

## 获取帮助

如果遇到问题：

1. 查看日志文件了解详细错误信息
2. 检查 `README.md` 中的常见问题部分
3. 确认所有依赖都已正确安装
4. 尝试在浏览器中手动登录，确认网站功能正常

祝你测试顺利！
