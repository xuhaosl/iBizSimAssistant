# iBizSimAssistant 项目实现计划

## 项目概述
iBizSimAssistant 是一个网页自动化助手项目，主要功能包括：
1. 使用账号密码登录指定网页
2. 从网页提取数据
3. 将数据按照要求填入本地Excel表格
4. 从本地Excel表格读取数据并提交到网页

## 技术栈选择

### 核心技术
- **编程语言**: Python 3.8+
- **网页自动化**: Playwright（推荐，相比Selenium更稳定、更快）
- **Excel处理**: openpyxl（读写Excel文件）
- **配置管理**: YAML/JSON（存储配置信息）
- **日志记录**: logging模块

### 依赖库
- playwright: 网页自动化
- openpyxl: Excel文件操作
- pyyaml: 配置文件解析
- python-dotenv: 环境变量管理

## 项目结构设计

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
├── logs/
├── .env                        # 环境变量（敏感信息）
├── .gitignore
├── requirements.txt            # Python依赖
├── README.md
└── setup.py                    # 安装脚本
```

## 实现步骤

### 第一阶段：项目基础搭建

#### 步骤1：创建项目目录结构
- 创建所有必要的目录
- 初始化Python包（__init__.py文件）
- 设置.gitignore文件

#### 步骤2：配置依赖管理
- 创建requirements.txt文件
- 列出所有必要的依赖包
- 创建setup.py用于项目安装

#### 步骤3：配置管理模块
- 创建config.yaml配置文件模板
  - 网站URL配置
  - 登录信息配置（使用占位符）
  - Excel文件路径配置
  - 数据映射规则配置
- 实现settings.py配置加载类
- 创建.env.example模板文件

#### 步骤4：日志系统
- 实现logger.py日志工具
- 配置日志格式和级别
- 设置日志文件存储路径

### 第二阶段：浏览器自动化模块

#### 步骤5：浏览器管理
- 实现browser_manager.py
  - 初始化Playwright浏览器
  - 管理浏览器生命周期
  - 处理浏览器异常
  - 支持无头模式和有头模式切换

#### 步骤6：页面操作基础
- 实现page_handler.py
  - 页面导航方法
  - 元素定位和操作方法
  - 等待元素加载
  - 截图功能（调试用）

### 第三阶段：登录功能

#### 步骤7：登录处理器
- 实现login_handler.py
  - 读取登录配置
  - 自动填写用户名和密码
  - 处理验证码（预留接口）
  - 处理登录失败情况
  - 验证登录成功状态
  - 保存登录状态（cookies）

#### 步骤8：登录测试
- 创建test_login.py测试文件
- 编写登录功能单元测试
- 测试各种登录场景

### 第四阶段：数据提取功能

#### 步骤9：数据提取器
- 实现extractor.py
  - 根据配置定位数据元素
  - 提取文本、属性、表格等数据
  - 处理动态加载内容
  - 支持多种选择器（CSS、XPath）

#### 步骤10：数据处理器
- 实现processor.py
  - 数据清洗和格式化
  - 数据转换（字符串转数字、日期等）
  - 数据验证
  - 数据结构化（转换为字典、列表等）

#### 步骤11：提取功能测试
- 创建test_extraction.py测试文件
- 测试各种数据提取场景

### 第五阶段：Excel操作模块

#### 步骤12：Excel读取器
- 实现reader.py
  - 读取Excel文件
  - 按工作表读取数据
  - 按行/列读取数据
  - 读取指定单元格数据
  - 处理合并单元格

#### 步骤13：Excel写入器
- 实现writer.py
  - 创建/打开Excel文件
  - 写入数据到指定单元格
  - 写入数据到指定行/列
  - 创建新工作表
  - 保存Excel文件

#### 步骤14：Excel功能测试
- 创建test_excel.py测试文件
- 测试读写功能

### 第六阶段：数据写入Excel功能

#### 步骤15：数据映射配置
- 在config.yaml中添加数据映射规则
  - 网页数据字段到Excel单元格的映射
  - 数据格式转换规则
  - 写入位置配置

#### 步骤16：实现数据写入流程
- 在processor.py中添加写入逻辑
  - 读取映射配置
  - 格式化提取的数据
  - 调用Excel写入器
  - 处理写入错误

### 第七阶段：Excel数据提交到网页功能

#### 步骤17：Excel数据读取配置
- 在config.yaml中添加Excel数据读取规则
  - Excel单元格/区域到网页字段的映射
  - 数据读取范围配置

#### 步骤18：实现数据提交流程
- 在page_handler.py中添加表单填写方法
  - 读取Excel数据
  - 定位网页表单元素
  - 填写数据到表单
  - 提交表单
  - 处理提交结果

### 第八阶段：主程序集成

#### 步骤19：主程序入口
- 实现main.py
  - 命令行参数解析
  - 工作流程编排
  - 错误处理和恢复
  - 进度显示

#### 步骤20：工作流程实现
- 实现完整的工作流程
  1. 初始化配置
  2. 启动浏览器
  3. 登录网站
  4. 提取网页数据
  5. 写入数据到Excel（可选）
  6. 从Excel读取数据（可选）
  7. 提交数据到网页（可选）
  8. 关闭浏览器

### 第九阶段：完善和优化

#### 步骤21：错误处理增强
- 添加详细的异常处理
- 实现重试机制
- 添加错误日志记录
- 提供友好的错误提示

#### 步骤22：性能优化
- 优化浏览器启动速度
- 减少不必要的等待
- 批量操作优化

#### 步骤23：文档完善
- 编写README.md
  - 项目介绍
  - 安装说明
  - 使用指南
  - 配置说明
  - 常见问题
- 添加代码注释

#### 步骤24：测试完善
- 完善单元测试
- 添加集成测试
- 测试覆盖率检查

## 配置文件示例

### config.yaml
```yaml
# 网站配置
website:
  base_url: "https://example.com"
  login_url: "/login"
  target_pages:
    - "/data-page"
    - "/form-page"

# 登录配置
login:
  username_selector: "#username"
  password_selector: "#password"
  submit_selector: "#login-btn"
  success_indicator: ".user-profile"

# Excel配置
excel:
  input_file: "./data/input.xlsx"
  output_file: "./data/output.xlsx"
  sheet_name: "Sheet1"

# 数据提取配置
extraction:
  - name: "data_field1"
    selector: ".data-field1"
    type: "text"
    target_cell: "A1"
  - name: "data_field2"
    selector: ".data-field2"
    type: "text"
    target_cell: "B1"

# 数据提交配置
submission:
  - excel_cell: "A2"
    selector: "#form-field1"
    type: "text"
  - excel_cell: "B2"
    selector: "#form-field2"
    type: "text"
  submit_selector: "#submit-btn"

# 浏览器配置
browser:
  headless: false
  timeout: 30000
  screenshot_on_error: true
```

### .env.example
```env
# 登录凭据
USERNAME=your_username
PASSWORD=your_password

# 可选：代理设置
PROXY_SERVER=
PROXY_USERNAME=
PROXY_PASSWORD=
```

## 关键功能实现要点

### 1. 登录功能
- 使用Playwright的fill()方法填写表单
- 使用wait_for_selector()等待元素加载
- 使用expect()验证登录状态
- 保存cookies以维持会话

### 2. 数据提取
- 使用page.locator()定位元素
- 使用text_content()、inner_text()等提取文本
- 使用get_attribute()提取属性
- 处理表格数据（逐行读取）

### 3. Excel写入
- 使用openpyxl.load_workbook()打开文件
- 使用cell.value赋值
- 使用worksheet.append()添加行
- 使用workbook.save()保存

### 4. 数据提交
- 从Excel读取数据
- 使用fill()填写表单字段
- 使用click()提交表单
- 验证提交结果

## 安全考虑

1. **敏感信息保护**
   - 使用.env文件存储密码
   - 将.env加入.gitignore
   - 不在代码中硬编码凭据

2. **输入验证**
   - 验证Excel数据格式
   - 验证网页元素存在性
   - 防止注入攻击

3. **错误处理**
   - 不暴露敏感信息在错误消息中
   - 记录错误但不记录密码
   - 安全的文件操作

## 扩展性设计

1. **插件化架构**
   - 支持自定义数据提取器
   - 支持自定义数据处理器
   - 支持自定义Excel操作

2. **多网站支持**
   - 通过配置文件支持多个网站
   - 网站特定的处理逻辑

3. **任务调度**
   - 支持定时任务
   - 支持批量处理

## 测试策略

1. **单元测试**
   - 每个模块独立测试
   - 使用mock对象模拟浏览器
   - 测试边界条件

2. **集成测试**
   - 测试完整工作流程
   - 使用测试环境
   - 测试异常情况

3. **端到端测试**
   - 使用真实网站（测试环境）
   - 完整流程测试
   - 性能测试

## 部署考虑

1. **依赖管理**
   - 使用虚拟环境
   - 固定依赖版本
   - 提供安装脚本

2. **跨平台支持**
   - Windows/Linux/Mac兼容
   - 浏览器驱动自动安装

3. **日志和监控**
   - 详细的操作日志
   - 错误告警
   - 性能监控

## 实施时间估算

- 第一阶段：项目基础搭建（1-2天）
- 第二阶段：浏览器自动化模块（2-3天）
- 第三阶段：登录功能（2-3天）
- 第四阶段：数据提取功能（3-4天）
- 第五阶段：Excel操作模块（2-3天）
- 第六阶段：数据写入Excel功能（2-3天）
- 第七阶段：Excel数据提交到网页功能（3-4天）
- 第八阶段：主程序集成（2-3天）
- 第九阶段：完善和优化（3-5天）

总计：约20-30天（根据复杂度和经验）

## 后续优化方向

1. **功能增强**
   - 支持验证码识别（OCR）
   - 支持多账号管理
   - 支持数据可视化
   - 支持邮件通知

2. **性能优化**
   - 并发处理
   - 缓存机制
   - 增量更新

3. **用户体验**
   - 图形界面（GUI）
   - Web界面
   - 进度条显示
   - 实时日志查看

4. **企业级特性**
   - 数据库支持
   - API接口
   - 权限管理
   - 审计日志
