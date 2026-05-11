---
name: boss-search
description: 当 agent 需要完成 BOSS 直聘登录、cookie 校验、人才搜索时使用。优先使用此 skill 进行稳定的命令式搜索工作流。
---

# BOSS 直聘搜索 Skill

## 功能概览

| 功能 | 命令入口 | 说明 |
| --- | --- | --- |
| 登录 | `has boss login --account <name>` | 生成或刷新指定账号的 cookie |
| Cookie 校验 | `has boss check --account <name>` | 检查指定账号 cookie 是否有效 |
| 人才搜索 | `has boss search ...` | 搜索候选人并导出数据 |
| 详情采集 | 直接调用 MCP Chrome 工具 | 采集候选人详情页 |

## 支持动作

### 1. 登录 BOSS 直聘

```bash
# 登录（默认无头模式）
has boss login --account my_account

# 有头模式（显示浏览器窗口）
has boss login --account my_account --headed
```

**流程说明：**
1. 导航到 https://www.zhipin.com/web/user/?ka=header-login
2. 等待二维码加载完成
3. 使用 chrome_screenshot 获取二维码图片展示给用户
4. 等待用户扫码完成
5. 验证登录成功后保存 Cookie

### 2. 检查 Cookie 状态

```bash
has boss check --account my_account
```

### 3. 人才搜索

```bash
# 基本搜索
has boss search --account my_account --keyword "Python 开发"

# 带筛选条件
has boss search --account my_account --keyword "算法工程师" --city "北京" --salary "30-50K" --pages 3

# 导出为 CSV
has boss search --account my_account --keyword "产品经理" --output csv
```

**搜索参数：**
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --keyword | -k | 搜索关键词（必填） | - |
| --city | -c | 城市筛选 | 不限制 |
| --salary | -s | 薪资范围 | 不限制 |
| --pages | -p | 采集页数 | 1 |
| --output | -o | 导出格式 (json/csv) | json |
| --headed | - | 显示浏览器窗口 | False |

## MCP Chrome 工具调用规范

**重要：当 CLI 不可用时，直接调用 MCP Chrome 工具执行自动化操作。**

### 登录流程

```python
# 1. 导航到登录页
mcp_chrome_chrome_navigate(url="https://www.zhipin.com/web/user/?ka=header-login")

# 2. 等待二维码加载
sleep(3)

# 3. 截图展示二维码给用户
mcp_chrome_chrome_screenshot(storeBase64=True, savePng=False)

# 4. 等待用户扫码（轮询检查登录状态）
# 检测到页面跳转或出现用户头像即表示登录成功

# 5. 保存 Cookie
# 使用 chrome_javascript 获取 cookies 并通过 CookieManager 保存
```

### 搜索流程

```python
# 1. 导航到搜索页
mcp_chrome_chrome_navigate(url="https://www.zhipin.com/web/geek/job")

# 2. 填写搜索关键词
mcp_chrome_chrome_fill_or_select(
    selector="div.search-job-wrapper input[type='text']",
    value="Python 开发"
)

# 3. 点击搜索按钮
mcp_chrome_chrome_click_element(
    selector="button.search-btn",
    waitForNavigation=True
)

# 4. 解析搜索结果列表
mcp_chrome_chrome_read_page()
# -> 解析页面内容，提取候选人列表

# 5. 分页采集
# 点击下一页，重复步骤 4

# 6. 采集详情（可选）
# 对每个候选人点击进入详情页
mcp_chrome_chrome_click_element(selector="a.job-card-left-box")
mcp_chrome_chrome_read_page()
# -> 解析详情页，获取联系方式、完整经历等
```

## CSS/XPath 选择器参考

| 元素 | CSS 选择器 | 说明 |
|------|------------|------|
| 搜索输入框 | `input[placeholder*='搜索']` | 搜索关键词输入 |
| 搜索按钮 | `button.search-btn` | 提交搜索 |
| 职位卡片 | `div.job-card-wrapper` | 搜索结果项 |
| 职位名称 | `span.job-name` | 候选人当前职位 |
| 薪资 | `span.salary` | 薪资范围 |
| 公司名称 | `h3.company-name a` | 当前公司 |
| 下一页按钮 | `a[class*='next']` | 分页按钮 |
| 二维码区域 | `div.login-qrcode img` | 登录二维码 |

*注意：BOSS 直聘页面结构可能会变化，请使用 chrome_read_page 动态验证选择器有效性。*

## 搜索结果数据结构

每个候选人包含以下字段：

```json
{
  "platform": "boss",
  "candidate_id": "xxx123",
  "name": "张三",
  "current_title": "高级 Python 开发工程师",
  "current_company": "某知名互联网公司",
  "current_salary": "30-50K",
  "location": "北京",
  "work_years": "5-10年",
  "skills": ["Python", "Django", "MySQL", "Redis"],
  "contact": {
    "phone": "138xxxxxxx",
    "email": "xxx@xxx.com",
    "wechat": null
  },
  "experiences": [...],
  "educations": [...],
  "profile_url": "https://www.zhipin.com/...",
  "collected_at": "2026-05-11T22:30:00"
}
```

## 参考文档

- 运行前提：`references/runtime-requirements.md`
- CLI 契约：`references/cli-contract.md`
- 元素选择器：`references/selectors.md`
- 故障排查：`references/troubleshooting.md`

## 常见问题

**Q: 登录后很快就退出了？**
A: BOSS 直聘有较严格的反爬机制，建议：
1. 不要频繁登录登出
2. 使用有头模式降低被识别概率
3. 操作间隔设置合理的延迟

**Q: 搜索结果为空？**
A: 可能原因：
1. Cookie 已失效，需要重新登录
2. 关键词太具体，没有匹配结果
3. 被反爬拦截，需要等待一段时间重试
