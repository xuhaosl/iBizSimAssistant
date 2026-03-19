# iBizSimAssistant

一个功能强大的网页自动化助手，用于网页数据提取和Excel集成。

## 功能特性

- **自动登录**: 使用账号密码自动登录指定网页
- **数据提取**: 从网页提取文本、属性、表格等多种类型的数据
- **Excel集成**: 将提取的数据写入本地Excel表格
- **数据提交**: 从本地Excel读取数据并提交到网页表单
- **灵活配置**: 通过YAML配置文件自定义所有操作
- **日志记录**: 详细的日志记录便于调试和监控

## 技术栈

- **Python 3.8+**
- **Playwright**: 网页自动化框架
- **openpyxl**: Excel文件操作
- **PyYAML**: 配置文件解析
- **python-dotenv**: 环境变量管理

## 安装

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆仓库:
```bash
git clone https://github.com/yourusername/iBizSimAssistant.git
cd iBizSimAssistant
```

2. 创建虚拟环境（推荐）:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖:
```bash
pip install -r requirements.txt
```

4. 安装Playwright浏览器:
```bash
playwright install chromium
```

## 配置

### 1. 环境变量配置

复制 `.env.example` 文件为 `.env`:
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的登录凭据:
```env
USERNAME=your_username
PASSWORD=your_password
```

### 2. 应用配置

编辑 `src/config/config.yaml` 文件，根据您的需求配置:

```yaml
website:
  base_url: "https://example.com"
  login_url: "/login"
  target_pages:
    - "/data-page"
    - "/form-page"

login:
  username_selector: "#username"
  password_selector: "#password"
  submit_selector: "#login-btn"
  success_indicator: ".user-profile"

excel:
  input_file: "./data/input.xlsx"
  output_file: "./data/output.xlsx"
  sheet_name: "Sheet1"

extraction:
  - name: "data_field1"
    selector: ".data-field1"
    type: "text"
    target_cell: "A1"
  - name: "data_field2"
    selector: ".data-field2"
    type: "text"
    target_cell: "B1"

submission:
  - excel_cell: "A2"
    selector: "#form-field1"
    type: "text"
  - excel_cell: "B2"
    selector: "#form-field2"
    type: "text"
  submit_selector: "#submit-btn"

browser:
  headless: false
  timeout: 30000
  screenshot_on_error: true
```

## 使用方法

### 命令行参数

```bash
python src/main.py [选项]
```

#### 选项说明

- `--config, -c`: 指定配置文件路径（默认: src/config/config.yaml）
- `--mode, -m`: 操作模式
  - `full`: 完整工作流程（登录、提取数据、写入Excel）
  - `extract`: 仅提取数据并写入Excel
  - `submit`: 仅从Excel读取数据并提交到网页
- `--page, -p`: 目标页面URL路径

### 使用示例

#### 1. 完整工作流程

执行所有步骤: 登录、提取数据、写入Excel:
```bash
python src/main.py --mode full
```

#### 2. 仅提取数据

登录并从指定页面提取数据，然后写入Excel:
```bash
python src/main.py --mode extract --page "/data-page"
```

#### 3. 仅提交数据

登录并从Excel读取数据，然后提交到指定页面:
```bash
python src/main.py --mode submit --page "/form-page"
```

#### 4. 使用自定义配置文件

```bash
python src/main.py --config /path/to/custom_config.yaml --mode full
```

## 项目结构

```
iBizSimAssistant/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 程序入口
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # 配置加载
│   │   └── config.yaml         # 配置文件
│   ├── browser/
│   │   ├── __init__.py
│   │   ├── browser_manager.py  # 浏览器管理
│   │   └── page_handler.py     # 页面操作
│   ├── auth/
│   │   ├── __init__.py
│   │   └── login_handler.py    # 登录处理
│   ├── data/
│   │   ├── __init__.py
│   │   ├── extractor.py        # 数据提取
│   │   └── processor.py        # 数据处理
│   ├── excel/
│   │   ├── __init__.py
│   │   ├── reader.py           # Excel读取
│   │   └── writer.py           # Excel写入
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # 日志工具
│       └── validators.py       # 数据验证
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_extraction.py
│   └── test_excel.py
├── logs/                      # 日志文件目录
├── data/                      # 数据文件目录
├── .env                       # 环境变量（敏感信息）
├── .gitignore
├── requirements.txt            # Python依赖
├── setup.py                   # 安装脚本
└── README.md
```

## 配置说明

### 网站配置 (website)

- `base_url`: 网站基础URL
- `login_url`: 登录页面路径
- `target_pages`: 需要处理的目标页面列表

### 登录配置 (login)

- `username_selector`: 用户名输入框的CSS选择器
- `password_selector`: 密码输入框的CSS选择器
- `submit_selector`: 登录按钮的CSS选择器
- `success_indicator`: 登录成功后的页面元素选择器

### Excel配置 (excel)

- `input_file`: 输入Excel文件路径
- `output_file`: 输出Excel文件路径
- `sheet_name`: 工作表名称

### 数据提取配置 (extraction)

每个提取字段包含:
- `name`: 字段名称
- `selector`: 元素CSS选择器
- `type`: 数据类型（text、attribute、table、list）
- `target_cell`: 目标Excel单元格

### 数据提交配置 (submission)

每个提交字段包含:
- `excel_cell`: Excel单元格引用
- `selector`: 网页表单元素选择器
- `type`: 数据类型
- `submit_selector`: 提交按钮选择器

### 浏览器配置 (browser)

- `headless`: 是否使用无头模式（true/false）
- `timeout`: 默认超时时间（毫秒）
- `screenshot_on_error`: 错误时是否截图（true/false）

## 日志

日志文件保存在 `logs/` 目录下，文件名格式为 `ibizsim_YYYYMMDD_HHMMSS.log`。

日志级别:
- DEBUG: 详细的调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误

## 常见问题

### 1. 登录失败

**问题**: 无法登录到网站

**解决方案**:
- 检查 `.env` 文件中的用户名和密码是否正确
- 确认 `config.yaml` 中的选择器是否正确
- 查看日志文件了解详细错误信息
- 尝试将 `browser.headless` 设置为 `false` 以观察浏览器行为

### 2. 数据提取失败

**问题**: 无法提取网页数据

**解决方案**:
- 确认页面已完全加载
- 检查元素选择器是否正确
- 使用浏览器开发者工具验证选择器
- 增加超时时间

### 3. Excel读写错误

**问题**: 无法读写Excel文件

**解决方案**:
- 确认Excel文件路径正确
- 检查文件是否被其他程序占用
- 确保有文件读写权限
- 确认工作表名称正确

### 4. Playwright浏览器未安装

**问题**: 运行时提示浏览器未安装

**解决方案**:
```bash
playwright install chromium
```

## 开发

### 运行测试

```bash
pytest tests/
```

### 代码风格

本项目遵循PEP 8代码风格指南。

## 安全建议

1. **不要提交敏感信息**: 确保 `.env` 文件已添加到 `.gitignore`
2. **使用强密码**: 在 `.env` 中使用强密码
3. **定期更新依赖**: 保持依赖包为最新版本
4. **限制文件权限**: 确保配置文件和日志文件有适当的访问权限

## 贡献

欢迎贡献！请遵循以下步骤:

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请通过以下方式联系:

- 提交 Issue
- 发送邮件至: your.email@example.com

## 致谢

感谢所有为本项目做出贡献的开发者。

## 更新日志

### 0.1.0 (2024-03-19)
- 初始版本发布
- 实现基本登录功能
- 实现数据提取功能
- 实现Excel读写功能
- 实现数据提交功能
