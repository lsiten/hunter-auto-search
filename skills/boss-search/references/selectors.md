# BOSS 直聘元素选择器参考

*注意：BOSS 直聘页面结构可能会变化，请使用 `chrome_read_page` 动态验证选择器有效性。*

## 登录页面元素

| 元素 | CSS 选择器 | 说明 |
|------|------------|------|
| 二维码图片 | `div.login-qrcode img, img[alt*='扫码']` | 登录二维码 |
| 账号密码登录切换 | `a[class*='password']` | 切换到账号密码登录 |
| 手机号输入框 | `input[type='tel']` | 手机号输入 |
| 验证码输入框 | `input[placeholder*='验证码']` | 验证码输入 |
| 获取验证码按钮 | `button[class*='code-btn']` | 获取验证码 |
| 登录提交按钮 | `button[type='submit']` | 提交登录 |

## 搜索页面元素

| 元素 | CSS 选择器 | 说明 |
|------|------------|------|
| 搜索输入框 | `input[placeholder*='搜索职位']`, `div.search-job-wrapper input` | 关键词输入框 |
| 搜索按钮 | `button.search-btn`, `button[class*='search-submit']` | 提交搜索 |
| 城市筛选下拉 | `div[class*='city-select']` | 城市选择器 |
| 薪资筛选下拉 | `div[class*='salary-select']` | 薪资选择器 |
| 经验筛选下拉 | `div[class*='experience-select']` | 经验选择器 |
| 筛选结果数量 | `span[class*='count']` | 搜索结果总数 |

## 搜索结果列表元素

| 元素 | CSS 选择器 | 说明 |
|------|------------|------|
| 职位卡片容器 | `div.job-card-wrapper`, `li[class*='job-card']` | 单个搜索结果项 |
| 职位名称 | `span.job-name`, `div[class*='job-title']` | 候选人当前职位 |
| 薪资 | `span.salary`, `div[class*='salary']` | 薪资范围 |
| 公司名称 | `h3.company-name a`, `div[class*='company-info'] a` | 当前公司 |
| 工作地点 | `span.job-area`, `p[class*='area']` | 工作城市 |
| 工作经验 | `span[class*='experience']` | 工作年限 |
| 学历要求 | `span[class*='degree']` | 学历要求 |
| 职位标签 | `div[class*='tag-list'] span` | 技能标签列表 |
| 候选人链接 | `a.job-card-left-box` | 进入详情页的链接 |

## 详情页面元素

| 元素 | CSS 选择器 | 说明 |
|------|------------|------|
| 候选人姓名 | `h1[class*='name']`, `div[class*='user-name']` | 姓名 |
| 联系方式按钮 | `button[class*='contact']`, `a[class*='chat']` | 获取联系方式按钮 |
| 手机号 | `div[class*='phone']` | 手机号（需要点击获取） |
| 邮箱 | `div[class*='email']` | 邮箱 |
| 工作经历列表 | `div[class*='experience-list'] div.item` | 工作经历项 |
| 教育经历列表 | `div[class*='education-list'] div.item` | 教育经历项 |
| 技能标签 | `div[class*='skill-tags'] span` | 技能标签 |
| 自我描述 | `div[class*='self-intro']`, `div[class*='resume-summary']` | 自我介绍 |

## 分页元素

| 元素 | CSS 选择器 | 说明 |
|------|------------|------|
| 下一页按钮 | `a[class*='next']`, `li[class*='next'] a`, `button[aria-label*='下一页']` | 下一页 |
| 当前页码 | `span[class*='current']`, `li[class*='active']` | 当前页数 |
| 总页数 | `div[class*='page-count']` | 总页数 |

## 动态验证方法

```python
# 1. 使用 chrome_read_page 获取页面元素
elements = mcp_chrome_chrome_read_page(filter="interactive")

# 2. 检查元素是否存在
for elem in elements:
    if "搜索" in elem.get("text", ""):
        print(f"找到搜索相关元素: {elem}")

# 3. 调试建议
# 使用 chrome_screenshot 结合视觉确认
# 使用 chrome_javascript 在控制台检查元素
```

## 常见变动提示

BOSS 直聘大约每 3-6 个月会进行一次前端重构，主要变动点：
1. 类名前缀变化（如从 `job-card` 变为 `job-item`）
2. 页面布局调整（搜索框位置变化）
3. 登录流程变化（增加新的验证方式）

建议每次使用前先人工确认页面结构是否有变化。
