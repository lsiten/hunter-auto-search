---
name: maimai-search
description: 当 agent 需要完成脉脉登录、cookie 校验、人才搜索时使用。优先使用此 skill 进行稳定的命令式搜索工作流。
---

# 脉脉搜索 Skill

## 功能概览

| 功能 | 命令入口 | 说明 |
| --- | --- | --- |
| 登录 | `has maimai login --account <name>` | 生成或刷新指定账号的 cookie |
| Cookie 校验 | `has maimai check --account <name>` | 检查指定账号 cookie 是否有效 |
| 人才搜索 | `has maimai search ...` | 搜索候选人并导出数据 |
| 详情采集 | 直接调用 MCP Chrome 工具 | 采集候选人详情页 |

## 支持动作

### 1. 登录脉脉

```bash
has maimai login --account my_account
```

### 2. 检查 Cookie 状态

```bash
has maimai check --account my_account
```

### 3. 人才搜索

```bash
has maimai search --account my_account --keyword "Python 开发"
```

## MCP Chrome 工具调用规范

### 登录流程

```python
# 1. 导航到登录页
mcp_chrome_chrome_navigate(url="https://maimai.cn/")

# 2. 选择手机号登录或扫码登录
# 脉脉需要手机号验证码登录
```

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 元素选择器：`references/selectors.md`
- 故障排查：`references/troubleshooting.md`

*开发中 - 更多细节待补充*
