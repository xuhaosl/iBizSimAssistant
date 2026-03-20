# iBizSimAssistant

iBizSim 助手 - 一个功能完整的图形界面工具，用于 iBizSim 网站的登录、赛事管理和参数提取。

## 功能特性

- **图形界面**: 友好的 Tkinter 图形用户界面
- **自动登录**: 支持账号密码自动登录 iBizSim 网站
- **赛事管理**: 自动加载和管理用户的赛事列表
- **参数提取**: 从规则页面自动提取32个比赛参数
- **Excel集成**: 支持读取和显示Excel文件内容
- **灵活配置**: 通过YAML配置文件自定义网站选择器
- **日志记录**: 详细的日志记录便于调试和监控
- **双向滚动**: 赛事列表支持水平和垂直滚动

## 技术栈

- **Python 3.8+**
- **Playwright**: 网页自动化框架
- **Tkinter**: 图形用户界面
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
git clone https://github.com/xuhaosl/iBizSimAssistant.git
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

## 使用方法

### 启动图形界面

```bash
python -m src.main
```

或者在 Windows 上双击 `启动验证工具.bat` 文件。

### 主要功能

#### 1. 登录功能

- 输入用户名和密码
- 支持密码显示/隐藏切换
- 自动启动浏览器进行登录
- 实时状态显示

#### 2. 赛事管理

- 自动加载用户参加的赛事列表
- 显示赛事ID、名称、日期、状态等信息
- 支持进入比赛页面
- 支持跳转到规则页面

#### 3. 参数提取

从规则页面自动提取以下32个参数：

**基础参数**:
- 当期可运输比例
- 公司总数
- 公司序号

**成本参数**:
- 原材料库存费用
- 购机费用
- 原材料固定运费
- 原材料变动运费
- 原材料可用比例
- 维修费

**人力资源参数**:
- 新员工培训费
- 安置费
- 基本工资
- 一加特殊工资
- 二班正班工资
- 二加特殊工资

**财务参数**:
- 废品系数
- 最高工资系数
- 最低资金额度
- 贷款利息
- 国债利息
- 债券利息
- 税收比例
- 减税比例
- 资金有效性

**评分权重参数**:
- 本期利润
- 市场份额
- 累计分红
- 累计缴税
- 净资产
- 人均利润率
- 资本利润率

#### 4. 文件读取

- 支持 Excel 文件（.xlsx, .xls）
- 支持文本文件（.txt）
- 自动识别文件类型
- 表格内容格式化显示

## 配置

### 环境变量配置

复制 `.env.example` 文件为 `.env`:
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的登录凭据:
```env
USERNAME=your_username
PASSWORD=your_password
```

### 应用配置

编辑 `src/config/config.yaml` 文件，根据您的需求配置:

```yaml
website:
  base_url: "https://www.ibizsim.cn/main"
  login_url: "/login"
  target_pages:
    - "/index"
    - "/decision"

login:
  username_selector: 'input[name="name"]'
  password_selector: 'input[name="password"]'
  submit_selector: 'input[type="submit"]'
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

browser:
  headless: false
  timeout: 30000
  screenshot_on_error: true
```

## 项目结构

```
iBizSimAssistant/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 图形界面主程序
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
│   │   ├── game_extractor.py   # 赛事数据提取
│   │   └── processor.py        # 数据处理
│   ├── excel/
│   │   ├── __init__.py
│   │   ├── reader.py           # Excel读取
│   │   └── writer.py           # Excel写入
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # 日志工具
│       ├── performance.py       # 性能优化
│       ├── retry.py           # 重试机制
│       └── validators.py       # 数据验证
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_extraction.py
│   ├── test_excel.py
│   └── test_config.py
├── logs/                      # 日志文件目录
├── data/                      # 数据文件目录
├── .env                       # 环境变量（敏感信息）
├── .gitignore
├── requirements.txt            # Python依赖
├── setup.py                   # 安装脚本
├── 启动验证工具.bat            # Windows快速启动脚本
└── README.md
```

## 界面布局

### 三栏布局

**第一栏** (1:1:1):
- 登录信息（用户名、密码、显示密码复选框）
- 登录/停止/清空按钮
- 状态显示
- 赛事列表（支持水平和垂直滚动）
- 进入比赛/复制规则按钮
- 查看日志/退出按钮

**第二栏** (1:1:1):
- 文件选择（文件地址、打开按钮）
- 规则详情（参数表格 + 显示框）
  - 参数表格：32行×2列（参数、值）
  - 显示框：显示规则页面内容

**第三栏** (1:1:1):
- 待用区域

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

### 2. 参数提取失败

**问题**: 无法从规则页面提取参数

**解决方案**:
- 确认已成功跳转到规则页面
- 检查规则页面是否完全加载
- 查看日志文件了解具体哪个参数提取失败
- 某些参数可能需要手动填写

### 3. Excel文件读取失败

**问题**: 无法读取Excel文件

**解决方案**:
- 确认Excel文件路径正确
- 检查文件是否被其他程序占用
- 确保有文件读写权限
- 确认文件格式为.xlsx或.xls

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
5. **注意日志安全**: 不要在日志中记录敏感信息

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

### 1.0.0 (2025-03-20)
- 实现完整的图形界面
- 实现iBizSim网站登录功能
- 实现赛事列表加载和管理
- 实现32个参数的自动提取
- 实现Excel文件读取支持
- 实现双向滚动赛事列表
- 实现规则详情表格显示
- 优化用户界面布局和交互
- 添加详细的日志记录系统