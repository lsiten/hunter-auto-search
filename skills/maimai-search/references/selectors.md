# 脉脉页面元素选择器参考

> 本文档列出脉脉平台所有页面的元素选择器，供 Hermes Agent 的 MCP Chrome 工具使用。

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
- **登录页**: `https://maimai.cn/login`
- **首页**: `https://maimai.cn`

### 登录元素 - 二维码方式

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 二维码标签 | `.qr-login-tab, .tab-qrcode` | 切换到二维码登录 |
| 二维码图片 | `.qrcode-img, .qr-code img` | 登录二维码 |
| 刷新二维码 | `.refresh-qrcode, .btn-refresh` | 刷新过期的二维码 |

### 登录元素 - 手机号验证码方式

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 账号密码标签 | `.password-tab, .tab-account` | 切换到账号登录 |
| 手机号输入 | `input[name="phone"], #phone` | 手机号码输入框 |
| 验证码输入 | `input[name="code"], #code` | 短信验证码输入框 |
| 获取验证码 | `.get-code-btn, .btn-send-code` | 发送验证码按钮 |
| 登录按钮 | `.submit-btn, .btn-login` | 提交登录按钮 |

### 登录状态检查

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 用户头像 | `.user-avatar, .avatar img, .header-avatar` | 登录成功后右上角显示 |
| 用户名称 | `.user-name, .username, .header-name` | 显示登录用户名 |

---

## 搜索相关

### 搜索页面 URL
- **搜索页**: `https://maimai.cn/search`

### 搜索元素

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 搜索框 | `.search-input, #searchInput, .header-search input` | 顶部搜索栏 |
| 搜索按钮 | `.search-btn, .btn-search, .header-search button` | 搜索提交按钮 |

### 高级筛选条件

| 筛选条件 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 城市筛选 | `.city-filter, .area-selector, .location-filter` | 按城市/地区筛选 |
| 公司筛选 | `.company-filter, .corp-selector` | 按当前公司筛选 |
| 职位筛选 | `.position-filter, .title-selector` | 按职位名称筛选 |
| 行业筛选 | `.industry-filter` | 按行业领域筛选 |
| 学校筛选 | `.school-filter` | 按毕业院校筛选 |

### 人脉度数筛选

| 人脉度数 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 人脉筛选器 | `.degree-filter` | 人脉关系筛选器 |
| 1 度人脉 | `.degree-1, .first-degree` | 直接联系人 |
| 2 度人脉 | `.degree-2, .second-degree` | 朋友的朋友（数量最多） |
| 3 度人脉 | `.degree-3, .third-degree` | 3 度及以上 |

---

## 搜索结果列表

### 列表容器

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 结果列表容器 | `.search-result-list, .user-list, .contact-list` | 搜索结果外层容器 |

### 候选人卡片元素

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 卡片元素 | `.user-card, .search-item, .contact-item` | 单个候选人卡片 |
| 头像 | `.avatar img, .head-img, .user-avatar` | 候选人头像 |
| 姓名 | `.name, .user-name, .contact-name` | 候选人姓名 |
| 职位 | `.title, .job-title, .position` | 当前职位名称 |
| 公司 | `.company, .corp-name, .current-company` | 当前工作单位 |
| 所在地 | `.location, .city, .area` | 所在城市 |
| 人脉度数 | `.degree, .connection-degree` | 人脉关系层级 |
| 共同联系人 | `.mutual-contacts, .common-friends` | 共同好友数量 |
| 添加联系人 | `.add-contact-btn, .btn-add, .connect-btn` | 发送连接请求 |
| 发消息按钮 | `.send-message-btn, .btn-message` | 发送站内信 |
| 查看详情 | `.view-profile, .card-click-area` | 点击进入个人主页 |

---

## 个人详情页

### 基本信息

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 姓名 | `.profile-name, .name, .user-name` | 候选人姓名 |
| 头像 | `.profile-avatar img, .avatar` | 候选人头像 |
| 职位 | `.profile-title, .job-title, .position` | 当前职位 |
| 公司 | `.profile-company, .current-company` | 当前工作单位 |
| 所在地 | `.profile-location, .city, .location` | 所在城市 |
| 行业 | `.profile-industry, .industry` | 所属行业 |

### 详细信息区

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 信息区块 | `.profile-info, .info-section` | 详细信息区域 |
| 信息项 | `.info-item, .detail-item` | 单个信息条目 |

### 标签

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 用户标签 | `.profile-tags .tag, .user-tags .tag-item` | 个人标签（如：海归、大厂、创业） |

### 工作经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 工作经历区域 | `.work-experience, .experience-list, .work-list` | 工作经历板块 |
| 单条经历 | `.work-item, .experience-item` | 单条工作经历 |
| 公司名称 | `.company-name, .corp-name, .employer` | 任职公司 |
| 职位名称 | `.position, .title, .job-title` | 担任职位 |
| 任职时间 | `.duration, .date-range, .time-period` | 工作时间段 |
| 工作描述 | `.description, .job-content, .desc` | 工作内容描述 |

### 教育经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 教育经历区域 | `.education-experience, .edu-list, .education-list` | 教育经历板块 |
| 单条教育 | `.edu-item, .education-item` | 单条教育经历 |
| 学校名称 | `.school-name, .school` | 毕业院校 |
| 学历 | `.degree, .education` | 学位/学历 |
| 专业 | `.major, .specialty, .field` | 所学专业 |
| 就读时间 | `.duration, .date-range` | 在校时间段 |

### 项目经历

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 项目经历区域 | `.project-experience, .project-list` | 项目经历板块 |
| 单条项目 | `.project-item` | 单条项目经历 |

### 技能标签

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 技能区域 | `.skill-tags, .skills, .ability-tags` | 技能标签板块 |
| 技能标签 | `.skill-tags .tag, .skills .skill-item` | 单个技能标签 |

### 联系方式 (VIP/人脉可见)

| 字段名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 联系方式区域 | `.contact-info, .contact-section` | 联系方式板块 |
| 手机号 | `.phone, .mobile, .telephone` | 手机号码 |
| 邮箱 | `.email, .mail` | 电子邮箱 |
| 微信 | `.wechat, .wx` | 微信号 |

---

## 消息/聊天相关

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 聊天弹窗 | `.chat-modal, .message-window` | 消息对话窗口 |
| 消息输入框 | `.message-input, .chat-input textarea` | 消息内容编辑区 |
| 发送按钮 | `.send-btn, .btn-send` | 发送消息按钮 |

---

## 人脉关系

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 人脉路径 | `.relation-path, .connection-path` | 显示"你 → A → B"的连接路径 |
| 共同好友列表 | `.mutual-friends-list, .common-contacts` | 共同好友列表 |

---

## 分页与无限加载

### 传统分页

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 分页容器 | `.pagination, .pager` | 分页导航容器 |
| 下一页按钮 | `.next-page, .next, .pagination .next` | 翻到下一页 |
| 页码列表 | `.pagination .page-item, .pager .num` | 所有页码按钮 |
| 当前页码 | `.pagination .active, .current-page` | 当前所在页码 |

### 无限加载

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 加载更多触发 | `.load-more, .infinite-trigger` | 触发加载更多的位置 |
| 加载更多按钮 | `.load-more-btn, .btn-load-more` | 手动点击加载更多 |

**无限加载操作示例:**
```python
# 滚动到页面底部触发加载
mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
time.sleep(3)  # 等待加载完成
```

---

## 反爬/验证元素

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 错误提示 | `.error-message, .error-tip, .message-box` | 错误信息展示 |
| 滑块验证 | `.slider-btn, .slide-verify, .captcha-slider` | 极验滑块验证码 |
| 验证码图片 | `.captcha-img, .verify-img, .geetest_item_img` | 图形验证码 |
| 验证码输入 | `.code-input, input[name="verifyCode"]` | 验证码输入框 |

### 会员/权限提示

| 元素名称 | CSS 选择器 | 说明 |
|---------|-----------|------|
| 会员限制提示 | `.member-limit, .vip-tip` | 需要 VIP 权限的提示 |
| 每日上限提示 | `.daily-limit, .limit-tip` | 达到每日操作上限的提示 |

---

## URL 模式

| 页面类型 | 正则表达式 | 示例 |
|---------|-----------|------|
| 登录页 | `maimai\.cn/login` | `https://maimai.cn/login` |
| 首页 | `maimai\.cn/?$` | `https://maimai.cn` |
| 搜索页 | `maimai\.cn/search` | `https://maimai.cn/search?q=Python` |
| 个人档案 | `maimai\.cn/web/personal` | `https://maimai.cn/web/personal?uid=123456` |
| 消息页 | `maimai\.cn/web/im` | `https://maimai.cn/web/im` |

---

## API 端点 (谨慎使用)

| 接口名称 | 路径 | 说明 |
|---------|------|------|
| 搜索接口 | `/api/search/user` | 搜索结果 API |
| 个人档案 | `/api/user/profile` | 个人档案 API |
| 联系人接口 | `/api/user/contact` | 联系人相关 API |
| 消息接口 | `/api/im/send` | 发送消息 API |

---

## 使用示例

### MCP Chrome 工具调用

```python
# 1. 打开登录页面
mcp_chrome_navigate(url="https://maimai.cn/login")
time.sleep(3)

# 2. 手机号验证码登录
mcp_chrome_fill_or_select(selector='input[name="phone"]', value="13800138000")
time.sleep(1)
mcp_chrome_click_element(selector=".get-code-btn")
time.sleep(2)
# 此时需要手动输入收到的验证码
# mcp_chrome_fill_or_select(selector='input[name="code"]', value="123456")
# mcp_chrome_click_element(selector=".submit-btn")

# 3. 搜索关键词
mcp_chrome_fill_or_select(selector=".search-input", value="产品经理")
time.sleep(1)
mcp_chrome_click_element(selector=".search-btn")
time.sleep(3)

# 4. 滚动加载更多
for i in range(3):
    mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)

# 5. 获取页面内容
page_data = mcp_chrome_get_web_content(htmlContent=True)

# 6. 解析数据
candidates = searcher.parse_candidate_list(page_data)
```

---

## 选择器更新检查清单

当脉脉页面结构变更时，请检查：

- [ ] 登录表单输入框 ID 是否变化
- [ ] 搜索结果卡片类名是否更新
- [ ] 个人详情页信息区块类名是否变化
- [ ] 滑块验证码的 DOM 结构是否变更
- [ ] Cookie 关键字段是否有新增或变更
- [ ] 测试是否需要 VIP 权限才能看到某些字段

---

## 注意事项

1. **极验滑块**: 脉脉使用极验滑块验证码，自动化较难绕过，建议人工处理
2. **高频风控**: 脉脉对高频操作非常敏感，容易触发风控，务必控制频率
3. **VIP 权限**: 很多高级功能和联系方式需要 VIP 才能查看
4. **人脉限制**: 大部分数据只能查看 2 度人脉以内的信息
5. **页面动态**: 脉脉页面大量使用动态加载，需要等待元素出现
6. **选择器频繁变更**: 脉脉更新迭代快，选择器可能经常变化，需要及时更新
7. **中文文本匹配**: 页面文本全部为中文，文本匹配时注意编码问题
8. **数据隐私**: 脉脉用户数据敏感，遵守相关法律法规和平台协议
