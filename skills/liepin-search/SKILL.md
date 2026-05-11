---
name: liepin-search
description: 当 agent 需要完成猎聘登录、cookie 校验、人才搜索时使用。优先使用此 skill 进行稳定的命令式搜索工作流。
---

# 猎聘搜索 Skill

## 功能概览

| 功能 | 命令入口 | 说明 |
| --- | --- | --- |
| 登录 | `has liepin login --account <name>` | 生成或刷新指定账号的 cookie |
| Cookie 校验 | `has liepin check --account <name>` | 检查指定账号 cookie 是否有效 |
| 人才搜索 | `has liepin search ...` | 搜索候选人并导出数据 |
| 详情采集 | 直接调用 MCP Chrome 工具 | 采集候选人详情页 |

## 支持动作

### 1. 登录猎聘

```bash
has liepin login --account my_account
```

### 2. 检查 Cookie 状态

```bash
has liepin check --account my_account
```

### 3. 人才搜索

```bash
has liepin search --account my_account --keyword "Python 开发"
```

## MCP Chrome 工具调用规范

### 登录流程

```python
# 1. 导航到登录页
mcp_chrome_chrome_navigate(url="https://www.liepin.com/")

# 2. 点击登录按钮（通常在右上角）
mcp_chrome_chrome_click_element(selector="div[data-selector='login']")

# 3. 选择二维码登录
mcp_chrome_chrome_click_element(selector="div.qrcode-login-tab")

# 4. 截图展示二维码给用户
mcp_chrome_chrome_screenshot(storeBase64=True, savePng=False)

# 5. 等待用户扫码完成
```

### 搜索流程

```python
# 1. 导航到搜索页
mcp_chrome_chrome_navigate(url="https://www.liepin.com/zhaopin/")

# 2. 填写搜索关键词
mcp_chrome_chrome_fill_or_select(
    selector="input[placeholder*='搜索职位']",
    value="Python 开发"
)

# 3. 点击搜索按钮
mcp_chrome_chrome_click_element(selector="button.search-btn")

# 4. 解析搜索结果列表
mcp_chrome_chrome_read_page()
```

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 元素选择器：`references/selectors.md`
- 故障排查：`references/troubleshooting.md`

*开发中 - 更多细节待补充*
