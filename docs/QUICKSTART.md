# Hunter Auto Search 快速开始指南

## 环境准备

### 1. 安装依赖
```bash
cd hunter-auto-search
pip install -e .
```

### 2. 验证安装
```bash
python has_cli.py --help
```

应该看到输出：
```
Usage: has_cli.py [OPTIONS] COMMAND [ARGS]...

  Hunter Auto Search CLI - 多平台招聘人才搜索工具

Options:
  --help  Show this message and exit.

Commands:
  boss      BOSS 直聘搜索
  liepin    猎聘搜索
  linkedin  领英搜索
  maimai    脉脉搜索
```

## 第一个搜索任务 (BOSS 直聘)

### 步骤 1: 准备好 Hermes Agent
确保你的 Hermes Agent 已加载 MCP Chrome 工具。

### 步骤 2: 加载 BOSS 直聘 Skill
在 Hermes Agent 中执行：
```python
skill_view("boss-search")
```

### 步骤 3: 执行登录流程

让 Hermes Agent 按照 Skill 中的说明执行登录：

1. 导航到 https://www.zhipin.com/web/user/?ka=header-login
2. 等待二维码加载
3. 使用手机 BOSS 直聘 APP 扫码
4. 等待登录完成

### 步骤 4: 执行搜索

搜索 "Python 开发"，采集 2 页，导出到 JSON：

```bash
python has_cli.py boss search --account my_account --keyword "Python 开发" --city 北京 --pages 2 --format json --output output/python_dev.json
```

### 步骤 5: 查看结果

```bash
cat output/python_dev.json
```

## CLI 命令详解

### 登录账号
```bash
# BOSS 直聘登录
python has_cli.py boss login --account my_account

# 猎聘登录
python has_cli.py liepin login --account my_account

# 领英登录
python has_cli.py linkedin login --account my_account

# 脉脉登录
python has_cli.py maimai login --account my_account
```

### 检查 Cookie 有效性
```bash
python has_cli.py boss check --account my_account
```

### 搜索候选人
```bash
# 基本搜索
python has_cli.py boss search --account my_account --keyword "产品经理"

# 带筛选条件
python has_cli.py boss search --account my_account \
    --keyword "Java 开发" \
    --city "上海" \
    --salary "20-50K" \
    --experience "3-5年" \
    --pages 3 \
    --format csv \
    --output output/java_shanghai.csv

# 采集详情页
python has_cli.py boss search --account my_account \
    --keyword "人工智能" \
    --fetch-details \
    --pages 1
```

## 作为 Python 库使用

```python
from searcher import BossSearcher, LiepinSearcher
from utils import DataExporter

# 创建搜索器
boss = BossSearcher(account="my_account")

# 检查登录状态
cookie_valid = boss.check_login()
if not cookie_valid:
    print("需要重新登录，请让 Hermes Agent 执行登录流程")

# 准备搜索参数
params = boss.prepare_search_params(
    keyword="Python 开发",
    city="北京",
    salary="20-40K",
)

# 此时需要 Hermes Agent 执行浏览器操作:
# 1. mcp_chrome_navigate(url=BOSS_SEARCH_URL)
# 2. mcp_chrome_fill_or_select(...)
# 3. mcp_chrome_read_page()

# 解析搜索结果
# raw_data = 从 chrome_read_page 返回的数据
# candidates = boss.parse_search_list(raw_data)

# 导出数据
# exporter = DataExporter("output/result.json")
# exporter.export_json(candidates)
```

## Cookie 管理

### Cookie 存储位置
```
cookies/
├── boss_my_account.json
├── liepin_my_account.json
├── linkedin_my_account.json
└── maimai_my_account.json
```

### 手动导入 Cookie
如果你已经在浏览器中登录，可以手动导出 Cookie 到 JSON 文件：

```json
{
  "cookies": [
    {
      "name": "cookie_name",
      "value": "cookie_value",
      "domain": ".zhipin.com",
      "path": "/"
    }
  ],
  "account": "my_account",
  "platform": "boss",
  "created_at": "2024-01-15T10:30:00"
}
```

## 常见问题

### Q: 扫码登录超时怎么办？
A: 确保在 60 秒内完成扫码，或者增加超时时间配置。

### Q: 搜索结果为空？
A: 1. 检查是否已登录 2. 检查搜索关键词是否正确 3. 检查是否有验证码拦截

### Q: 遇到验证码？
A: BOSS 直聘和猎聘都有反爬机制，遇到验证码时：
1. 暂停操作
2. 手动在浏览器中完成验证
3. 继续执行

### Q: 采集频率如何设置？
A: 建议设置：
- 页面跳转间隔: 2-3 秒
- 点击操作间隔: 1-2 秒
- 详情页采集间隔: 3-5 秒

### Q: Cookie 失效很快？
A: 这是平台的反爬策略，建议每次搜索前都检查登录状态。

## Skill 加载方式

### Hermes Agent 中加载 Skill
```python
# BOSS 直聘
skill_view("boss-search")

# 猎聘
skill_view("liepin-search")

# 领英
skill_view("linkedin-search")

# 脉脉
skill_view("maimai-search")
```

### 查看 Skill 参考文档
每个 Skill 都有完整的参考文档：
- `runtime-requirements.md` - 运行环境要求
- `cli-contract.md` - CLI 命令契约
- `selectors.md` - 页面元素选择器
- `troubleshooting.md` - 故障排查

## 下一步

1. ✅ 项目框架已完成
2. ✅ BOSS 直聘 Skill 已完成
3. 🚧 实现 BOSS 直聘解析逻辑 (进行中)
4. 📋 实现猎聘解析逻辑
5. 📋 实现领英解析逻辑
6. 📋 实现脉脉解析逻辑
7. 📋 端到端测试与优化

## 获取帮助

- 查看 `docs/MCP_WORKFLOW_GUIDE.md` 了解 MCP 工具调用流程
- 查看各平台 Skill 文档了解平台特定操作
- 查看 `PROGRESS.md` 了解项目实现进度
