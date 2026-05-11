# MCP Chrome 工具调用流程指南

本文档定义了所有平台通用的浏览器自动化流程。
Hermes Agent 应按照此流程执行搜索和数据采集。

## 通用执行流程

### 1. 浏览器初始化与导航

```python
# 导航到目标页面
mcp_chrome_navigate(url=LOGIN_URL)

# 等待页面加载
time.sleep(2)
```

### 2. 登录流程 (扫码登录优先)

```python
# 步骤1: 检查是否已登录
page_content = mcp_chrome_read_page(filter="interactive")
if find_element(page_content, USER_AVATAR):
    logger.info("已登录，跳过登录流程")
    return True

# 步骤2: 尝试切换到二维码登录 (如果有)
qrcode_tab = find_element(page_content, LOGIN_QRCODE_TAB)
if qrcode_tab:
    mcp_chrome_click_element(selector=LOGIN_QRCODE_TAB)
    time.sleep(1)

# 步骤3: 截图展示二维码给用户
screenshot = mcp_chrome_screenshot(full_page=False)
logger.info("请扫描二维码登录")

# 步骤4: 等待用户扫码完成 (最多等待 60 秒)
max_wait = 60
start_time = time.time()
while time.time() - start_time < max_wait:
    page_content = mcp_chrome_read_page(filter="interactive")
    if find_element(page_content, USER_AVATAR):
        logger.success("登录成功！")
        return True
    time.sleep(2)

logger.error("登录超时")
return False
```

### 3. Cookie 保存与恢复

```python
# 登录成功后保存 cookie
cookies = mcp_chrome_get_cookies()
cookie_manager.save(account, cookies)

# 下次启动时恢复
cookies = cookie_manager.load(account)
if cookies:
    mcp_chrome_set_cookies(cookies)
    # 刷新页面验证
    mcp_chrome_navigate(url=HOME_URL)
    time.sleep(2)
```

### 4. 搜索流程

```python
# 步骤1: 导航到搜索页
mcp_chrome_navigate(url=SEARCH_URL)
time.sleep(3)

# 步骤2: 输入搜索关键词
mcp_chrome_fill_or_select(selector=SEARCH_INPUT, value=keyword)
time.sleep(0.5)

# 步骤3: 设置筛选条件 (可选)
if city:
    mcp_chrome_click_element(selector=FILTER_CITY)
    time.sleep(1)
    # 选择城市...

# 步骤4: 点击搜索按钮
mcp_chrome_click_element(selector=SEARCH_BTN)
time.sleep(3)
```

### 5. 结果列表解析

```python
def parse_list_page(page_content):
    """解析搜索结果列表页"""
    candidates = []
    
    # 找到所有候选人卡片
    cards = find_elements(page_content, CANDIDATE_CARD_ITEM)
    
    for card in cards:
        candidate = {
            'name': extract_text(card, CANDIDATE_NAME),
            'title': extract_text(card, CANDIDATE_TITLE),
            'company': extract_text(card, CANDIDATE_COMPANY),
            'location': extract_text(card, CANDIDATE_LOCATION),
            'avatar_url': extract_attr(card, CANDIDATE_AVATAR, 'src'),
        }
        candidates.append(candidate)
    
    return candidates
```

### 6. 分页处理

```python
# 方式1: 点击下一页
for page in range(pages):
    # 解析当前页
    page_content = mcp_chrome_read_page()
    candidates = parse_list_page(page_content)
    
    # 检查是否有下一页
    next_btn = find_element(page_content, NEXT_PAGE_BTN)
    if not next_btn:
        break
    
    # 点击下一页
    mcp_chrome_click_element(selector=NEXT_PAGE_BTN)
    time.sleep(2 + random())

# 方式2: 滚动加载 (无限滚动)
for scroll in range(pages):
    # 滚动到底部
    mcp_chrome_computer(action="scroll", scroll_direction="down", scroll_amount=5)
    time.sleep(1.5 + random())
    
    # 解析内容
    page_content = mcp_chrome_read_page()
    candidates = parse_list_page(page_content)
```

### 7. 详情页采集

```python
# 点击进入详情页
mcp_chrome_click_element(selector=DETAIL_LINK)
time.sleep(2)

# 解析详情页
page_content = mcp_chrome_read_page()

candidate_data = {
    'name': extract_text(page_content, CANDIDATE_DETAIL_NAME),
    'title': extract_text(page_content, CANDIDATE_DETAIL_TITLE),
    'location': extract_text(page_content, CANDIDATE_DETAIL_LOCATION),
    # ... 其他字段
}

# 返回列表页
mcp_chrome_computer(action="key", text="Backspace")
# 或者
mcp_chrome_navigate(url=previous_url)
time.sleep(1)
```

### 8. 反反爬虫策略

```python
# 1. 随机延迟
def random_delay(min_sec=1, max_sec=3):
    time.sleep(min_sec + random() * (max_sec - min_sec))

# 2. 模拟人类滚动
def human_scroll():
    for _ in range(random.randint(2, 4)):
        mcp_chrome_computer(action="scroll", scroll_direction="down", scroll_amount=random.randint(1, 3))
        random_delay(0.5, 1)

# 3. 鼠标移动轨迹 (可选，通过 chrome_computer)
# 点击元素前先移动鼠标

# 4. 采集频率控制
MIN_REQUEST_INTERVAL = 2  # 最小请求间隔(秒)
last_request_time = 0

def rate_limited_call():
    global last_request_time
    now = time.time()
    if now - last_request_time < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - (now - last_request_time))
    last_request_time = time.time()
    # 执行操作
```

### 9. 错误处理与重试

```python
def safe_click(selector, max_retries=3):
    for attempt in range(max_retries):
        try:
            mcp_chrome_click_element(selector=selector)
            random_delay()
            return True
        except Exception as e:
            logger.warning(f"点击失败 (尝试 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    return False

def safe_fill(selector, value, max_retries=3):
    for attempt in range(max_retries):
        try:
            mcp_chrome_fill_or_select(selector=selector, value=value)
            random_delay(0.3, 0.8)
            return True
        except Exception as e:
            logger.warning(f"输入失败 (尝试 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    return False
```

### 10. 验证码处理

```python
def handle_captcha():
    """检测并处理验证码"""
    page_content = mcp_chrome_read_page()
    
    # 检查滑块验证码
    slider = find_element(page_content, VERIFY_SLIDER)
    if slider:
        logger.info("检测到滑块验证码")
        # 需要人工介入
        mcp_chrome_screenshot()
        logger.warning("请手动完成滑块验证")
        # 等待用户完成
        time.sleep(10)
        return True
    
    # 检查图片验证码
    captcha = find_element(page_content, VERIFY_CAPTCHA)
    if captcha:
        logger.info("检测到图片验证码")
        mcp_chrome_screenshot()
        logger.warning("请手动输入验证码")
        time.sleep(15)
        return True
    
    return False

# 在每次操作后检查
def after_action_check():
    time.sleep(1)
    handle_captcha()
```

## 平台特定说明

### BOSS 直聘
- 强烈建议使用扫码登录
- 搜索结果是职位列表，需要点击职位后查看应聘者
- 有较严格的频率限制，建议单页间隔 5 秒以上

### 猎聘
- 招聘方后台(hunter.liepin.com)功能最完善
- 需要企业账号才能查看联系方式
- 有每日查看次数限制

### 领英
- 搜索需要登录
- 查看联系方式可能需要 Premium 账号
- 反爬机制严格，建议操作间隔 3-5 秒
- 建议使用无限滚动而非分页点击

### 脉脉
- 人脉关系会影响可见内容
- 查看详细资料需要加好友
- 有每日搜索和查看限制

## 最佳实践

1. **先手动测试**：先用真实浏览器走完一遍流程，确认所有选择器有效
2. **逐步调试**：先测试登录，再测试搜索，最后测试详情采集
3. **保存中间状态**：及时保存 Cookie 和已采集数据
4. **详细日志**：每个关键步骤都要有日志输出
5. **用户确认**：涉及登录和验证码时，及时提示用户操作
6. **异常捕获**：所有工具调用都要 try-catch 并处理
7. **超时处理**：设置合理的超时时间，避免无限等待
