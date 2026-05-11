# 猎聘页面元素选择器参考

> 本文档列出猎聘平台所有页面的元素选择器，供 Hermes Agent 的 MCP Chrome 工具使用。

---

## 目录

1. [登录相关](#登录相关)
2. [搜索相关](#搜索相关)
3. [搜索结果列表](#搜索结果列表)
4. [详情页元素](#详情页元素)
5. [分页相关](#分页相关)
6. [错误/提示元素](#错误提示元素)
7. [URL 模式](#url-模式)

---

## 登录相关

### 登录页面 URL
- **登录页**: `https://www.liepin.com/`
- **招聘方后台**: `https://hunter.liepin.com/`

### 登录元素

| 元素名称 | CSS 选择器 | XPath | 说明 |
|---------|-----------|-------|------|
| 登录链接 | `.login-btn, [data-selector='login']` | `//*[contains(@class,'login-btn')]` | 首页登录按钮 |
| 二维码图片 | `.qrcode-img, .qr-code img` | `//img[contains(@class,'qrcode')]` | 登录二维码 |
| 刷新二维码 | `.refresh-qrcode` | `//*[contains(@class,'refresh-qrcode')]` | 二维码失效时刷新 |
| 账号密码 Tab | `.tab-account` | `//*[contains(@class,'tab-account')]` | 切换到账号密码登录 |
| 用户名输入 | `input[name="username"], #login` | `//input[@name='username']` | 手机号/邮箱输入框 |
| 密码输入 | `input[name="password"], #password` | `//input[@name='password']` | 密码输入框 |
| 登录按钮 | `.submit-btn, .btn-login` | `//*[contains(@class,'submit-btn')]` | 提交登录 |

### 登录状态检查

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 用户头像 | `.user-avatar, .avatar img` | 登录成功后显示 |
| 用户名称 | `.user-name, .username` | 显示登录用户名 |

---

## 搜索相关

### 搜索页面 URL
- **简历搜索**: `https://hunter.liepin.com/resume/search`

### 搜索元素

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 关键词输入 | `.search-input, [data-selector="keyword"]` | 职位/技能关键词 |
| 搜索按钮 | `.search-btn, .btn-search` | 执行搜索 |

### 高级筛选

| 筛选条件 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 城市筛选 | `.city-filter, .area-selector` | 选择工作城市 |
| 薪资筛选 | `.salary-filter, .expectSalary-selector` | 期望薪资范围 |
| 经验筛选 | `.experience-filter, .workYears-selector` | 工作经验要求 |
| 学历筛选 | `.education-filter, .eduLevel-selector` | 学历要求 |
| 职位筛选 | `.position-filter` | 职位类别 |
| 公司筛选 | `.company-filter` | 公司行业/规模 |

---

## 搜索结果列表

### 列表容器

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 结果列表容器 | `.resume-list, .search-result-list` | 搜索结果的外层容器 |

### 候选人卡片元素

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 卡片元素 | `.resume-card, .search-item` | 单个候选人卡片 |
| 头像 | `.avatar img, .head-img` | 候选人头像 |
| 姓名 | `.name, .user-name, .resume-name` | 候选人姓名 |
| 当前职位 | `.title, .job-title, .position` | 最新职位名称 |
| 当前公司 | `.current-company, .latest-company` | 最新工作单位 |
| 期望薪资 | `.expected-salary, .salary-expect` | 期望薪资范围 |
| 所在地 | `.location, .work-city` | 工作城市 |
| 工作年限 | `.work-years, .experience` | 总工作经验 |
| 学历 | `.degree, .edu-level` | 最高学历 |
| 年龄 | `.age` | 年龄 |
| 最后活跃 | `.last-active, .active-time` | 最后在线时间 |
| 查看联系方式 | `.view-contact-btn, .get-contact` | 获取联系方式按钮 |

---

## 详情页元素

### 基本信息

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 姓名 | `.name, .resume-name` | 候选人姓名 |
| 头像 | `.avatar img` | 候选人头像 |
| 当前职位 | `.current-position, .job-title` | 最新职位 |
| 当前公司 | `.current-company` | 最新工作单位 |
| 期望薪资 | `.expected-salary, .salary` | 薪资要求 |
| 所在地 | `.location, .city` | 所在城市 |
| 年龄 | `.age` | 年龄 |
| 性别 | `.gender` | 性别 |

### 联系方式

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 手机 | `.phone, .mobile` | 手机号码 |
| 邮箱 | `.email` | 邮箱地址 |
| 微信 | `.wechat` | 微信号 |

### 工作经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 工作经历区域 | `.work-experience, .work-list, .experience-section` | 工作经历板块 |
| 单个经历 | `.work-item, .exp-item` | 单条工作经历 |
| 公司名称 | `.company-name, .corp-name` | 任职公司 |
| 职位名称 | `.position, .title` | 担任职位 |
| 任职时间 | `.duration, .date-range, .time` | 工作时间段 |
| 工作描述 | `.description, .job-content, .desc` | 工作内容描述 |

### 教育经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 教育经历区域 | `.education-experience, .edu-list, .education-section` | 教育经历板块 |
| 单条教育 | `.edu-item, .education-item` | 单条教育经历 |
| 学校名称 | `.school-name, .school` | 毕业院校 |
| 学历 | `.degree, .education` | 学历等级 |
| 专业 | `.major, .specialty` | 所学专业 |
| 就读时间 | `.duration, .date-range` | 在校时间段 |

### 技能与项目

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 技能标签 | `.skill-tags .tag, .skills .skill-item, .ability-item` | 技能标签列表 |
| 项目经历区域 | `.project-experience, .project-list` | 项目经历板块 |
| 项目条目 | `.project-item` | 单个项目经历 |

---

## 分页相关

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 分页容器 | `.pagination, .pager` | 分页导航容器 |
| 下一页按钮 | `.next-page, .next, .pagination .next` | 翻到下一页 |
| 上一页按钮 | `.prev-page, .prev` | 翻到上一页 |
| 页码列表 | `.pagination .page-item, .pager .num` | 所有页码 |
| 当前页码 | `.pagination .active, .current` | 当前所在页码 |

---

## 错误/提示元素

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 错误提示 | `.error-message, .error-tip, .message` | 错误信息提示 |
| 滑块验证 | `.slider-btn, .slide-verify` | 滑块验证码 |
| 图片验证码 | `.geetest_item_img, .captcha-img` | 图形验证码 |

---

## URL 模式

| 页面类型 | 正则表达式 | 示例 |
|---------|-----------|------|
| 登录页 | `liepin\.com/?$` | `https://www.liepin.com/` |
| 招聘方后台 | `hunter\.liepin\.com` | `https://hunter.liepin.com/` |
| 搜索页 | `hunter\.liepin\.com/resume/search` | `https://hunter.liepin.com/resume/search` |
| 候选人详情 | `hunter\.liepin\.com/resume/detail` | `https://hunter.liepin.com/resume/detail/123456` |
| 简历查看 | `hunter\.liepin\.com/resume/view` | `https://hunter.liepin.com/resume/view/123456` |

---

## API 端点

| 接口名称 | 路径 | 说明 |
|---------|------|------|
| 搜索接口 | `/hunter/resume/api/search` | 简历搜索 API |
| 详情接口 | `/hunter/resume/api/detail` | 简历详情 API |
| 联系方式 | `/hunter/resume/api/contact` | 获取联系方式 API |

---

## 使用示例

### MCP Chrome 工具调用

```python
# 1. 打开搜索页面
mcp_chrome_navigate(url="https://hunter.liepin.com/resume/search")

# 2. 输入关键词
mcp_chrome_fill_or_select(selector=".search-input", value="Python 开发")

# 3. 点击搜索
mcp_chrome_click_element(selector=".search-btn")

# 4. 等待结果加载
time.sleep(3)

# 5. 获取页面内容
page_data = mcp_chrome_get_web_content(htmlContent=True)

# 6. 解析数据
candidates = searcher.parse_candidate_list(page_data)
```

---

## 注意事项

1. **选择器优先级**: 优先使用 `data-*` 属性选择器，其次是 class 选择器
2. **动态加载**: 猎聘大量使用 AJAX 加载，需要等待数据加载完成
3. **反爬虫**: 频繁请求可能触发验证码，建议添加随机延迟
4. **页面变更**: 选择器可能随网站更新而失效，需要定期维护
5. **元素加载**: 使用 `wait_for` 等待关键元素出现后再操作
