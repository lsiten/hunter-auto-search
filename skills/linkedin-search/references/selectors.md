# 领英页面元素选择器参考

> 本文档列出领英平台所有页面的元素选择器，供 Hermes Agent 的 MCP Chrome 工具使用。

---

## 目录

1. [登录相关](#登录相关)
2. [搜索相关](#搜索相关)
3. [搜索结果列表](#搜索结果列表)
4. [个人详情页](#个人详情页)
5. [分页与无限加载](#分页与无限加载)
6. [反爬/验证元素](#反爬验证元素)
7. [URL 模式](#url-模式)

---

## 登录相关

### 登录页面 URL
- **登录页**: `https://www.linkedin.com/login`
- **首页**: `https://www.linkedin.com`

### 登录元素

| 元素名称 | CSS 选择器 | XPath | 说明 |
|---------|-----------|-------|------|
| 用户名输入 | `#username, input[name="session_key"]` | `//input[@id='username']` | 邮箱/手机号输入框 |
| 密码输入 | `#password, input[name="session_password"]` | `//input[@id='password']` | 密码输入框 |
| 登录按钮 | `button[type="submit"], .btn__primary--large` | `//button[@type='submit']` | 提交登录 |

### 登录状态检查

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 用户头像 | `.global-nav__me-photo, .profile-photo` | 登录成功后右上角显示 |
| 用户名称 | `.profile-name, .nav-item__name` | 显示登录用户名 |

---

## 搜索相关

### 搜索页面 URL
- **人员搜索**: `https://www.linkedin.com/search/results/people/`

### 搜索元素

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 全局搜索框 | `.search-global-typeahead__input, #global-nav-typeahead input` | 顶部搜索栏 |
| 搜索按钮 | `.search-global-typeahead__submit, .search-btn` | 搜索提交按钮 |

### 高级筛选条件

| 筛选条件 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 地区筛选 | `.location-filter, .geo-filter` | 按城市/地区筛选 |
| 当前公司 | `.current-company-filter` | 按当前任职公司筛选 |
| 过往公司 | `.past-company-filter` | 按过往任职公司筛选 |
| 行业筛选 | `.industry-filter` | 按行业领域筛选 |
| 学校筛选 | `.school-filter` | 按毕业院校筛选 |
| 语言筛选 | `.language-filter` | 按档案语言筛选 |

### 人脉连接度筛选

| 连接度 | CSS 选择器 | 说明 |
|-------|-----------|------|
| 人脉筛选 | `.network-filter` | 人脉关系筛选器 |
| 1 度人脉 | `.first-degree` | 直接联系人 |
| 2 度人脉 | `.second-degree` | 朋友的朋友 |
| 3 度人脉 | `.third-degree` | 3 度及以上 |

---

## 搜索结果列表

### 列表容器

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 结果列表容器 | `.search-results__list, .reusable-search__entity-result-list` | 搜索结果外层容器 |

### 候选人卡片元素

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 卡片元素 | `.entity-result, .search-result__item, .reusable-search__result-container` | 单个候选人卡片 |
| 头像 | `.entity-result__universal-image img, .presence-entity__image` | 候选人头像 |
| 姓名 | `.entity-result__title-text, .actor-name` | 候选人姓名 |
| 当前职位 | `.entity-result__primary-subtitle, .search-result__snippets` | 最新职位名称 |
| 所在地 | `.entity-result__secondary-subtitle, .search-result__location` | 所在城市 |
| 当前公司 | `.entity-result__summary, .search-result__job-title` | 最新工作单位 |
| 连接按钮 | `.entity-result__actions button, .search-result__actions button` | 发送连接请求 |
| 发消息按钮 | `.message-anywhere-button` | 发送站内信 |

---

## 个人详情页

### 基本信息

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 姓名 | `h1.text-heading-xlarge, .pv-top-card--list li:first-child` | 候选人姓名 |
| 当前职位 | `.text-body-medium.break-words, .pv-top-card--list li:nth-child(2)` | 最新职位 |
| 所在地 | `.text-body-small.inline.t-black--light.break-words, .pv-top-card--list-bullet li:first-child` | 所在城市 |
| 头像 | `.pv-top-card__photo img, .presence-entity__image` | 候选人头像 |

### 联系方式

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 联系方式区域 | `.pv-contact-info` | 联系方式板块 |
| 查看联系方式 | `#top-card-text-details-contact-info, .pv-top-card--contact-see-more` | 展开联系方式按钮 |
| 邮箱 | `.pv-contact-info__contact-type.ci-email a` | 电子邮箱 |
| 电话 | `.pv-contact-info__contact-type.ci-phone span` | 手机号码 |
| 网站 | `.pv-contact-info__contact-type.ci-websites a` | 个人网站 |
| 微信 | `.pv-contact-info__contact-type.ci-wechat` | 微信号 |

### 关于部分

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 关于区域 | `.pv-about-section, .summary` | 自我介绍板块 |
| 关于内容 | `.pv-about__summary-text, .summary__text` | 个人简介内容 |

### 工作经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 工作经历区域 | `.experience-section, #experience-section` | 工作经历板块 |
| 单条经历 | `.pv-entity__position-group-pager, .experience-item` | 单条工作经历 |
| 公司名称 | `.pv-entity__secondary-title, .company-name` | 任职公司 |
| 职位名称 | `.t-16.t-black.t-bold, .position-title` | 担任职位 |
| 任职时间 | `.pv-entity__date-range span:nth-child(2), .date-range` | 工作时间段 |
| 工作地点 | `.pv-entity__location span:nth-child(2), .location` | 工作城市 |
| 工作描述 | `.pv-entity__description, .description` | 工作内容描述 |

### 教育经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 教育经历区域 | `.education-section, #education-section` | 教育经历板块 |
| 单条教育 | `.pv-education-entity, .education-item` | 单条教育经历 |
| 学校名称 | `.pv-entity__school-name, .school-name` | 毕业院校 |
| 学历 | `.pv-entity__degree-name span:nth-child(2), .degree` | 学位/学历 |
| 专业 | `.pv-entity__fos span:nth-child(2), .field-of-study` | 所学专业 |
| 就读时间 | `.pv-entity__dates span:nth-child(2), .date-range` | 在校时间段 |

### 技能与其他

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 技能区域 | `.pv-skill-categories-section, .skills-section` | 技能标签板块 |
| 技能标签 | `.pv-skill-category-entity__name-text, .skill-item` | 单个技能标签 |
| 证书区域 | `.certifications-section` | 资格证书板块 |
| 项目区域 | `.projects-section` | 项目经历板块 |

---

## 分页与无限加载

### 分页控件

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 分页容器 | `.artdeco-pagination, .search-results__pagination` | 分页导航容器 |
| 下一页按钮 | `.artdeco-pagination__button--next, .next` | 翻到下一页 |
| 页码列表 | `.artdeco-pagination__indicator` | 所有页码按钮 |
| 当前页码 | `.artdeco-pagination__indicator--active` | 当前所在页码 |

### 无限加载

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 滚动触发点 | `.infinite-scroll__trigger` | 触发加载更多的位置 |

**无限加载操作示例:**
```python
# 滚动到页面底部触发加载
mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
time.sleep(3)  # 等待加载完成
```

---

## 消息相关

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 消息弹窗 | `.msg-overlay-conversation-bubble` | 消息对话窗口 |
| 消息输入框 | `.msg-form__contenteditable` | 消息内容编辑区 |
| 发送按钮 | `.msg-form__send-button` | 发送消息按钮 |

---

## 反爬/验证元素

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 验证页面 | `.challenge-form, .login-challenge` | 风控验证页面 |
| 验证码图片 | `.captcha-image, #captcha-internal` | 图形验证码 |
| 验证码输入 | `input[name="captcha"]` | 验证码输入框 |
| 邮箱验证输入 | `input[name="pin"]` | 邮箱验证码输入 |

---

## URL 模式

| 页面类型 | 正则表达式 | 示例 |
|---------|-----------|------|
| 登录页 | `linkedin\.com/login` | `https://www.linkedin.com/login` |
| 搜索页 | `linkedin\.com/search/results/people` | `https://www.linkedin.com/search/results/people/?keywords=Python` |
| 个人档案 | `linkedin\.com/in/[^/]+` | `https://www.linkedin.com/in/john-smith-123456` |
| 消息页 | `linkedin\.com/messaging` | `https://www.linkedin.com/messaging/` |

---

## API 端点 (谨慎使用)

| 接口名称 | 路径 | 说明 |
|---------|------|------|
| 搜索接口 | `/voyager/api/search/cluster` | 搜索结果 API |
| 档案接口 | `/voyager/api/identity/profiles` | 个人档案 API |
| 消息接口 | `/voyager/api/messaging/conversations` | 消息对话 API |

---

## 使用示例

### MCP Chrome 工具调用

```python
# 1. 打开登录页面
mcp_chrome_navigate(url="https://www.linkedin.com/login")
time.sleep(3)

# 2. 输入账号密码
mcp_chrome_fill_or_select(selector="#username", value="your@email.com")
mcp_chrome_fill_or_select(selector="#password", value="your_password")

# 3. 点击登录
mcp_chrome_click_element(selector='button[type="submit"]')
time.sleep(5)

# 4. 搜索关键词
mcp_chrome_fill_or_select(
    selector=".search-global-typeahead__input",
    value="软件工程师 北京"
)
time.sleep(1)
mcp_chrome_click_element(selector=".search-global-typeahead__submit")
time.sleep(3)

# 5. 滚动加载更多
for i in range(3):
    mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)

# 6. 获取页面内容
page_data = mcp_chrome_get_web_content(htmlContent=True)

# 7. 解析数据
candidates = searcher.parse_candidate_list(page_data)
```

---

## 选择器更新检查清单

当领英页面结构变更时，请检查：

- [ ] 登录表单输入框 ID 是否变化
- [ ] 搜索结果卡片类名是否更新
- [ ] 个人详情页信息区块类名是否变化
- [ ] 分页控件是否仍存在或改为无限加载
- [ ] Cookie 关键字段是否有新增或变更
- [ ] 测试页面语言是否为英语（影响文本匹配）

---

## 注意事项

1. **领英 A/B 测试**: 领英经常进行 A/B 测试，不同用户可能看到不同页面结构
2. **动态加载**: 大量内容使用 JavaScript 动态加载，需要等待加载完成
3. **无限滚动**: 搜索结果使用无限滚动，不使用传统分页
4. **选择器优先级**: 优先使用 ID 选择器，其次是语义化类名
5. **语言敏感**: 文本匹配受界面语言影响，建议使用英文界面
6. **XPath 回退**: CSS 选择器失效时，可尝试 XPath 作为备选方案
