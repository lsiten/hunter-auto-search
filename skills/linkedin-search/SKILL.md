---
name: linkedin-search
description: 当 agent 需要完成领英登录、cookie 校验、人才搜索时使用。优先使用此 skill 进行稳定的命令式搜索工作流。
---

# 领英搜索 Skill

## 功能概览

| 功能 | 命令入口 | 说明 |
| --- | --- | --- |
| 登录 | `has linkedin login --account <name>` | 生成或刷新指定账号的 cookie |
| Cookie 校验 | `has linkedin check --account <name>` | 检查指定账号 cookie 是否有效 |
| 人才搜索 | `has linkedin search ...` | 搜索候选人并导出数据 |
| 详情采集 | 直接调用 MCP Chrome 工具 | 采集候选人详情页 |

## 支持动作

### 1. 登录领英

```bash
has linkedin login --account my_account
```

### 2. 检查 Cookie 状态

```bash
has linkedin check --account my_account
```

### 3. 人才搜索

```bash
has linkedin search --account my_account --keyword "Software Engineer"
```

## MCP Chrome 工具调用规范

### 登录流程

```python
# 1. 导航到登录页
mcp_chrome_chrome_navigate(url="https://www.linkedin.com/login")

# 2. 输入账号密码（需要用户提供）或扫码登录
mcp_chrome_chrome_fill_or_select(selector="#username", value="xxx@xxx.com")
mcp_chrome_chrome_fill_or_select(selector="#password", value="******")
mcp_chrome_chrome_click_element(selector="button[type='submit']")
```

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 元素选择器：`references/selectors.md`
- 故障排查：`references/troubleshooting.md`

*开发中 - 更多细节待补充*
