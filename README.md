# Hunter Auto Search

面向 Hermes Agent 的多平台招聘人才搜索自动化工具集。

## 项目概述

Hunter Auto Search 是一个基于 Skill-Driven Architecture 的人才搜索自动化工具，专为 Hermes Agent 设计。通过 MCP Chrome 工具协议，实现 BOSS 直聘、猎聘、领英、脉脉四大招聘平台的自动化搜索和数据采集。

## ✨ 特性

- 🎯 **Skill-Driven**：每个平台一个独立 Skill，Hermes Agent 通过 `skill_view()` 加载执行
- 🌐 **MCP Chrome Native**：不依赖 Playwright，直接使用 Hermes 内置的 MCP Chrome 工具
- 📊 **统一数据模型**：所有平台输出统一的候选人数据结构，便于后续 AI 处理
- 🔐 **多账号支持**：通过 `--account` 参数支持多账号 Cookie 隔离
- 📦 **多种导出格式**：支持 JSON、CSV 格式导出
- 🛠️ **CLI 工具**：统一的命令行入口，方便集成和自动化

## 🏗️ 支持平台

| 平台 | 状态 | Skill 名称 | 备注 |
|------|------|------------|------|
| BOSS 直聘 | ✅ 框架完成 | `boss-search` | 选择器已定义 |
| 猎聘 | ✅ 框架完成 | `liepin-search` | 选择器已定义 |
| 领英 | ✅ 框架完成 | `linkedin-search` | 选择器已定义 |
| 脉脉 | ✅ 框架完成 | `maimai-search` | 选择器已定义 |

## 📁 项目结构

```
hunter-auto-search/
├── pyproject.toml          # 项目配置与依赖
├── has_cli.py              # CLI 入口 (has = hunter-auto-search)
├── conf.py                 # 全局配置
├── cookies/                # Cookie 存储 (git 忽略)
├── output/                 # 数据输出 (git 忽略)
├── docs/                   # 文档
│   ├── QUICKSTART.md       # 快速开始指南
│   └── MCP_WORKFLOW_GUIDE.md  # MCP 工具调用流程指南
├── utils/                  # 工具模块
│   ├── log.py              # Loguru 日志配置
│   ├── cookie_manager.py   # 多账号 Cookie 管理
│   └── data_exporter.py    # JSON/CSV 数据导出
├── searcher/               # 搜索器核心
│   ├── base_searcher.py    # 搜索基类 (所有平台继承)
│   ├── models.py           # Pydantic 统一数据模型
│   ├── boss_searcher/      # BOSS 直聘搜索器
│   ├── liepin_searcher/    # 猎聘搜索器
│   ├── linkedin_searcher/  # 领英搜索器
│   └── maimai_searcher/    # 脉脉搜索器
└── skills/                 # Hermes Agent Skills
    ├── boss-search/        # BOSS 直聘完整 Skill
    ├── liepin-search/      # 猎聘 Skill
    ├── linkedin-search/    # 领英 Skill
    └── maimai-search/      # 脉脉 Skill
```

## 🚀 快速开始

### 1. 安装

```bash
cd hunter-auto-search
pip install -e .
```

### 2. 验证安装

```bash
python has_cli.py --help
```

### 3. 使用 Hermes Agent 执行

1. 在 Hermes Agent 中加载对应平台的 Skill
2. 按照 Skill 说明执行登录流程
3. 执行搜索和数据采集

详细使用说明请查看 [快速开始指南](docs/QUICKSTART.md)。

## 📖 文档

- [快速开始指南](docs/QUICKSTART.md) - 快速上手教程
- [MCP 工具调用流程指南](docs/MCP_WORKFLOW_GUIDE.md) - 浏览器自动化详细流程
- 各平台 Skill 文档 - 平台特定的操作说明

## 🔧 CLI 使用

```bash
# 查看所有命令
python has_cli.py --help

# 平台命令
python has_cli.py boss --help      # BOSS 直聘
python has_cli.py liepin --help    # 猎聘
python has_cli.py linkedin --help  # 领英
python has_cli.py maimai --help    # 脉脉

# 登录
python has_cli.py boss login --account my_account

# 检查登录状态
python has_cli.py boss check --account my_account

# 搜索
python has_cli.py boss search --account my_account \
    --keyword "Python 开发" \
    --city "北京" \
    --pages 2 \
    --output output/result.json
```

## 📊 统一数据模型

所有平台输出统一的 Candidate 数据结构：

```python
{
  "platform": "boss",
  "candidate_id": "xxx",
  "name": "张三",
  "title": "高级 Python 工程师",
  "current_company": "某科技有限公司",
  "current_salary": "30-50K",
  "expected_salary": "40-60K",
  "location": "北京",
  "work_years": "5年",
  "age": 30,
  "gender": "男",
  "avatar_url": "https://...",
  "experiences": [
    {
      "company": "某科技有限公司",
      "position": "高级 Python 工程师",
      "duration": "2020.03 - 至今",
      "description": "负责后端开发..."
    }
  ],
  "educations": [
    {
      "school": "北京大学",
      "degree": "本科",
      "major": "计算机科学",
      "duration": "2013.09 - 2017.07"
    }
  ],
  "skills": ["Python", "Django", "MySQL", "Redis"],
  "contact": {
    "phone": "138****8888",
    "email": "zhangsan@example.com",
    "wechat": None
  },
  "profile_url": "https://...",
  "last_active": "3小时前",
  "collected_at": "2024-01-15T10:30:00"
}
```

## 🎯 设计理念

### Skill-Driven Architecture
每个平台一个独立的 Skill，包含：
- 功能说明和使用场景
- CLI 命令契约
- MCP 工具调用流程
- 页面元素选择器
- 故障排查指南

Hermes Agent 通过 `skill_view()` 加载 Skill，按照 Skill 的指导执行自动化流程。

### 分离关注点
- **Python 代码**：数据模型、Cookie 管理、数据导出、搜索参数准备
- **Hermes Agent**：通过 MCP Chrome 执行浏览器操作
- **Skill 文档**：定义执行流程和规范

## 📋 开发进度

详细进度请查看 [PROGRESS.md](PROGRESS.md)。

### 已完成
- ✅ 项目基础框架
- ✅ Pydantic 统一数据模型
- ✅ 多账号 Cookie 管理
- ✅ BaseSearcher 基类
- ✅ 4 个平台搜索器框架
- ✅ 4 个平台页面选择器定义
- ✅ CLI 命令行工具
- ✅ BOSS 直聘完整 Skill
- ✅ 其他平台 Skill 框架
- ✅ 文档（快速开始、MCP 流程指南）

### 进行中
- 🚧 BOSS 直聘页面解析逻辑完善
- 🚧 端到端流程测试

## ⚠️ 注意事项

1. **合规使用**：请遵守各平台的使用条款和 robots.txt
2. **数据隐私**：采集的个人信息请合规使用和存储
3. **反爬限制**：合理设置采集频率，避免账号被封
4. **账号安全**：妥善保管 Cookie 文件，不要提交到版本控制

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
