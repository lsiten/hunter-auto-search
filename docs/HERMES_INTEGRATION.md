# Hermes Agent 集成使用指南

## ✅ Skills 已安装

以下 Skills 已成功安装到 Hermes Agent：

| Skill | 平台 | 状态 |
|-------|------|------|
| `boss-search` | BOSS 直聘 | ✅ 已安装 |
| `liepin-search` | 猎聘 | ✅ 已安装 |
| `linkedin-search` | 领英 | ✅ 已安装 |
| `maimai-search` | 脉脉 | ✅ 已安装 |

---

## 🚀 快速开始

### 步骤 1: 加载 Skill

在 Hermes Agent 中输入：

```python
# 加载 BOSS 直聘 Skill
skill_view('boss-search')
```

### 步骤 2: 按照 Skill 指引执行

Skill 会自动显示：
- 功能概述
- 支持的命令
- MCP 工具调用流程
- 详细的步骤说明

---

## 📋 使用流程示例

### 示例 1: BOSS 直聘搜索人才

#### **阶段 1: 登录**

```python
# 1. 加载 Skill
skill_view('boss-search')

# 2. 按照 Skill 指引执行登录流程
# - 使用 mcp_chrome_navigate 打开登录页
# - 等待用户扫码
# - 保存 Cookie
```

#### **阶段 2: 搜索人才**

```python
# 3. 导航到搜索页面
# 4. 输入搜索关键词
# 5. 设置筛选条件
# 6. 开始搜索
```

#### **阶段 3: 数据采集**

```python
# 7. 解析搜索结果列表
# 8. 进入详情页采集完整信息
# 9. 导出为 JSON/CSV
```

---

## 🔧 MCP 工具调用流程

### 登录流程

```python
# 1. 打开登录页面
mcp_chrome_navigate(url="https://www.zhipin.com/web/user/?ka=header-login")

# 2. 等待扫码
mcp_chrome_screenshot()  # 显示二维码给用户

# 3. 等待登录完成
# (等待页面跳转)

# 4. 保存 Cookie
# (使用 cookie_manager 保存)
```

### 搜索流程

```python
# 1. 打开搜索页面
mcp_chrome_navigate(url="https://www.zhipin.com/web/geek/job")

# 2. 输入关键词
mcp_chrome_fill_or_select(selector="#searchInput", value="Python 开发")

# 3. 点击搜索
mcp_chrome_click_element(selector=".search-btn")

# 4. 等待结果加载
# 5. 解析页面内容
mcp_chrome_get_web_content()
```

---

## 📊 数据输出

所有搜索结果会保存到：

```
output/
├── boss_search_result_20260511.json
├── boss_search_result_20260511.csv
└── ...
```

### 数据结构

每个候选人包含：
- 基础信息（姓名、头像、位置、年龄）
- 职业信息（当前职位、公司、薪资）
- 工作经历
- 教育经历
- 联系方式
- 技能标签

---

## 💡 常用命令

### CLI 命令

```bash
# 查看帮助
python has_cli.py --help

# BOSS 直聘
python has_cli.py boss --help
python has_cli.py boss check
python has_cli.py boss search --keyword "Python"

# 猎聘
python has_cli.py liepin --help

# 领英
python has_cli.py linkedin --help

# 脉脉
python has_cli.py maimai --help
```

### 数据验证

```python
# 在项目目录运行
python examples/boss_search_demo.py
```

---

## ⚠️ 注意事项

1. **反爬虫机制**: 招聘网站有反爬虫机制，请合理控制请求频率
2. **登录有效期**: Cookie 会过期，需要定期重新登录
3. **数据隐私**: 采集的候选人信息请妥善保管
4. **使用合规**: 请遵守各平台的使用条款和相关法律法规

---

## 📚 相关文档

- [快速开始指南](QUICKSTART.md)
- [MCP 工具调用完整流程](MCP_WORKFLOW_GUIDE.md)
- [BOSS 直聘 Skill 文档](../skills/boss-search/SKILL.md)
- [项目 README](../README.md)

---

## 🎉 开始使用

现在你可以在 Hermes Agent 中直接使用：

```python
# 加载 BOSS 直聘 Skill
skill_view('boss-search')
```

按照 Skill 文档的指引，即可开始自动化搜索人才！
