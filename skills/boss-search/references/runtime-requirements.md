# 运行前提与环境要求

## 系统要求

- **操作系统**: macOS / Linux / Windows
- **Python 版本**: 3.10+
- **Chrome 浏览器**: 已安装并可正常启动

## 依赖安装

```bash
cd hunter-auto-search
pip install -e .
```

## MCP Chrome Server 配置

本 Skill 依赖 Hermes Agent 内置的 MCP Chrome Server。请确保：

1. MCP Chrome Server 已在 Hermes Agent 中配置并启用
2. Chrome 浏览器可以正常启动
3. 网络可以正常访问 BOSS 直聘网站

## 账号准备

1. 确保有可用的 BOSS 直聘账号
2. 首次使用需要扫码登录
3. 建议使用企业账号以获得更完整的候选人信息

## 网络要求

- 能够正常访问 `https://www.zhipin.com`
- 稳定的网络连接（建议延迟 < 200ms）
- 不需要代理（如有代理请确保配置正确）

## 注意事项

1. **不要频繁登录登出**：频繁操作可能触发反爬机制
2. **合理设置采集速度**：建议每页间隔 5-10 秒
3. **Cookie 有效期**：BOSS 直聘 Cookie 通常有效期为 7-15 天
4. **IP 封禁风险**：短时间内大量采集可能导致 IP 被封，请谨慎使用
