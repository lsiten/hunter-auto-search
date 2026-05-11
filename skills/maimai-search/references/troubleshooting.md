# 脉脉故障排除指南

> 本文档记录脉脉平台常见问题和解决方案，帮助快速定位和解决问题。

---

## 目录

1. [登录问题](#登录问题)
2. [搜索问题](#搜索问题)
3. [解析问题](#解析问题)
4. [风控与验证](#风控与验证)
5. [权限与限制](#权限与限制)
6. [性能问题](#性能问题)

---

## 登录问题

### 问题 1: 滑块验证无法通过

**症状:**
```
登录时出现滑块验证码
拖动后显示验证失败
多次尝试均不成功
```

**可能原因:**
1. 浏览器环境被识别为自动化
2. 拖动轨迹过于规整
3. IP 地址异常

**解决方案:**
```python
# 方案 1: 人工手动处理验证 (推荐)
print("⚠️  检测到滑块验证，请手动完成后继续")
input("完成后按 Enter 继续...")

# 方案 2: 更换登录方式
# 使用二维码登录代替手机号登录
mcp_chrome_click_element(selector=".qr-login-tab")
print("请使用脉脉 App 扫描二维码登录")
input("完成后按 Enter 继续...")

# 方案 3: 调整浏览器环境
# 使用正常的用户配置文件
# 禁用自动化相关的浏览器标识
```

---

### 问题 2: 二维码很快过期

**症状:**
```
二维码显示后几秒钟就失效
刷新后仍然很快过期
```

**可能原因:**
1. 页面长时间无操作被检测
2. 网络环境异常
3. 账号存在风险

**解决方案:**
```python
# 1. 及时扫码，不要等待太久
print("⚠️  二维码已生成，请在 30 秒内完成扫码")

# 2. 自动刷新机制
import time
start_time = time.time()
while time.time() - start_time < 60:
    # 检查二维码是否过期
    is_expired = mcp_chrome_javascript(code="""
        return document.querySelector('.qrcode-expired') !== null;
    """)
    if is_expired:
        print("二维码过期，自动刷新...")
        mcp_chrome_click_element(selector=".refresh-qrcode")
        time.sleep(2)
    time.sleep(5)

# 3. 切换网络环境
# 使用手机热点或其他网络
```

---

### 问题 3: Cookie 保存后无法使用

**症状:**
```
[脉脉] 账号 'default' Cookie 已过期
即使刚登录保存，check 也显示过期
```

**可能原因:**
1. 关键 Cookie 字段缺失
2. 登录状态未完全建立
3. 多设备登录被踢下线

**解决方案:**
```bash
# 1. 检查 Cookie 文件内容
cat cookies/maimai_default.json

# 2. 确认关键 Cookie 存在
# access_token 和 uid 必须存在

# 3. 重新完整登录流程
# - 打开登录页
# - 完成滑块验证（如出现）
# - 输入手机号获取验证码
# - 输入验证码登录
# - 等待完全跳转至首页
# - 确认右上角头像已显示
# - 等待 10 秒让所有 Cookie 加载
# - 然后再保存 Cookie

# 4. 避免多设备同时登录
# 自动化操作期间，不要在手机上使用脉脉
```

---

## 搜索问题

### 问题 1: 搜索结果数量少

**症状:**
```
搜索"产品经理"只返回几十个结果
正常应该有几千个结果
```

**可能原因:**
1. 搜索次数达到每日限额
2. 账号没有 VIP 权限
3. 搜索范围限制过严
4. 人脉圈限制

**解决方案:**
```python
# 1. 检查账号权限
# 免费账号: ~50 次/天
# VIP 账号: ~500+ 次/天

# 2. 扩大搜索范围
# 移除城市筛选
# 使用更宽泛的关键词

# 3. 分时段搜索
# 上午搜索一部分
# 下午搜索一部分
# 晚上搜索一部分

# 4. 使用多个账号轮换
# account1 - 上午使用
# account2 - 下午使用
# account3 - 晚上使用

# 5. 升级 VIP 账号
# 解锁更多搜索次数和筛选条件
```

---

### 问题 2: 滚动加载不触发

**症状:**
```
滚动到页面底部后没有新加载内容
只显示第一页约 20 个结果
```

**可能原因:**
1. 滚动位置不够低
2. 加载时间不足
3. 需要点击"加载更多"按钮
4. 已达到搜索结果上限

**解决方案:**
```python
# 1. 滚动到真正的底部
mcp_chrome_javascript(code="""
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
""")
time.sleep(3)

# 2. 检查是否有加载更多按钮
has_load_more = mcp_chrome_javascript(code="""
    return document.querySelector('.load-more-btn') !== null;
""")

if has_load_more:
    print("点击加载更多按钮...")
    mcp_chrome_click_element(selector=".load-more-btn")
    time.sleep(3)

# 3. 多次滚动触发
for i in range(3):
    mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

# 4. 检查是否已达到结果上限
# 脉脉搜索通常只显示前 200-500 个结果
# 超过后需要换关键词重新搜索
```

---

### 问题 3: 页面显示"今日搜索次数已用完"

**症状:**
```
页面显示红色提示框
"今日搜索次数已达上限，请明天继续"
```

**可能原因:**
1. 免费账号每日次数用完
2. VIP 账号高频操作触发临时限制

**解决方案:**
```bash
# 方案 1: 等待明天重置
# 脉脉每日 0 点重置搜索次数

# 方案 2: 使用备用账号
python has_cli.py maimai login --account backup
python has_cli.py maimai search --keyword "Python" --account backup

# 方案 3: 升级更高等级 VIP
# 更高等级会员有更多搜索次数
```

---

## 解析问题

### 问题 1: 候选人姓名解析为空

**症状:**
```
name: None
所有文本字段都解析失败
```

**可能原因:**
1. 页面还在加载中
2. 选择器不匹配新版页面
3. 需要登录才能看到完整信息

**解决方案:**
```python
# 1. 增加等待时间
time.sleep(5)

# 2. 使用多个备用选择器
NAME_SELECTORS = [
    ".name",
    ".user-name",
    ".profile-name",
    ".contact-name"
]

for selector in NAME_SELECTORS:
    try:
        name = mcp_chrome_javascript(
            code=f"document.querySelector('{selector}')?.textContent?.trim()"
        )
        if name:
            print(f"成功获取姓名: {name}")
            break
    except Exception as e:
        print(f"选择器 {selector} 失败: {e}")
        continue

# 3. 确认已登录
# 脉脉很多信息需要登录后才能看到
if not searcher.check_cookie():
    print("⚠️  Cookie 无效，请先登录")
    searcher.login()
```

---

### 问题 2: 联系方式无法获取

**症状:**
```
email: None
phone: None
wechat: None
```

**可能原因:**
1. 候选人没有公开联系方式
2. 需要 VIP 权限才能查看
3. 需要添加为联系人才能查看
4. 人脉层级不够

**解决方案:**
```python
# 1. 检查是否有 VIP 权限
is_vip = mcp_chrome_javascript(code="""
    return document.querySelector('.vip-badge') !== null;
""")

if not is_vip:
    print("⚠️  非 VIP 账号，联系方式查看受限")
    print("建议: 升级 VIP 账号或从其他渠道获取联系方式")

# 2. 检查是否需要添加联系人
need_connect = mcp_chrome_javascript(code="""
    return document.querySelector('.add-contact-btn') !== null;
""")

if need_connect:
    print("⚠️  需要添加为联系人才能查看完整信息")
    # 注意: 频繁添加联系人可能触发风控

# 3. 从其他渠道获取联系方式
# - 邮箱可能在个人简介中
# - 公司邮箱格式推断
# - 其他社交平台交叉搜索
```

---

## 风控与验证

### 问题 1: 账号被临时限制

**症状:**
```
登录时显示"账号异常，请联系客服"
搜索时频繁出现验证码
所有功能无法正常使用
```

**可能原因:**
1. 操作频率过高触发风控
2. 短时间内大量查看档案
3. IP 地址频繁切换
4. 使用了代理/VPN 被检测

**解决方案:**
```python
# 1. 立即停止所有操作
# 不要尝试登录或刷新

# 2. 冷却期
# 轻度限制: 24-48 小时
# 中度限制: 3-7 天
# 重度限制: 可能需要联系客服解封

print("⚠️  检测到账号限制，建议冷却 48 小时后再试")
print("冷却期间不要进行任何操作")

# 3. 后续预防措施
# - 增加请求间隔: 从 3 秒增加到 10 秒
# - 每天操作不超过 3 小时
# - 只在白天工作时间段操作
# - 模拟正常人类作息时间
# - 每次操作后随机等待
# - 每次操作后滚动页面模拟浏览

# 4. 使用备用账号
# 不要把所有操作集中在一个账号上
```

---

### 问题 2: 频繁出现滑块验证

**症状:**
```
每次搜索都出现滑块
搜索 5 次出现 3 次验证
```

**可能原因:**
1. 请求频率太高
2. IP 被标记为高风险
3. 账号行为模式异常

**解决方案:**
```python
# 1. 大幅降低操作频率
# 原: 3 秒/次 → 改为: 15-30 秒/次
time.sleep(20)

# 2. 加入更多模拟人类行为
import random

# 随机滚动页面
mcp_chrome_javascript(code=f"window.scrollTo(0, {random.randint(100, 1500)})")
time.sleep(random.randint(2, 5))

# 随机停留
time.sleep(random.randint(10, 30))

# 模拟鼠标移动 (如有能力)
# 这有助于通过行为分析检测

# 3. 更换 IP 地址
# 使用不同的网络
# 使用手机热点

# 4. 更换账号
# 使用备用账号继续操作
# 原账号冷却一段时间
```

---

## 权限与限制

### 问题 1: "需要 VIP 权限才能查看"

**症状:**
```
点击查看详情时显示提示
"升级 VIP 解锁完整档案"
```

**可能原因:**
1. 查看的是 3 度人脉
2. 某些高级信息需要 VIP
3. 联系方式查看受限

**解决方案:**
```python
# 1. 调整搜索策略
# 主要搜索 2 度人脉，信息更完整
# 过滤掉 3 度人脉结果

# 2. 升级 VIP 账号
# 这是最直接的解决方案
# 建议: 如果是商业用途，值得投资

# 3. 从搜索列表提取信息
# 即使不进入详情页，列表也有基本信息
# 姓名、职位、公司、所在地
# 这些通常不需要 VIP
```

---

### 问题 2: "今日查看档案数已达上限"

**症状:**
```
查看第 50 个档案后出现限制
无法继续查看更多详情
```

**可能原因:**
1. 免费账号限制 (~50 人/天)
2. VIP 账号也有每日上限 (~300-500 人/天)

**解决方案:**
```bash
# 方案 1: 分批次查看
# 每天查看一部分
# 重要候选人优先查看

# 方案 2: 使用多个账号
# account1: 查看 1-50
# account2: 查看 51-100
# account3: 查看 101-150

# 方案 3: 只查看高质量候选人
# 先从列表筛选出最匹配的
# 只对 Top 30% 查看详情
# 节省查看配额
```

---

## 性能问题

### 问题 1: 脉脉页面加载慢

**症状:**
```
页面加载需要 10 秒以上
经常超时失败
```

**可能原因:**
1. 网络质量差
2. 脉脉服务器压力大
3. 页面资源太多

**解决方案:**
```python
# 1. 增加超时时间
# 默认超时可能不够
time.sleep(10)

# 2. 刷新重试
# 如果加载失败，刷新页面
mcp_chrome_navigate(url=current_url)
time.sleep(5)

# 3. 避开高峰时段
# 高峰: 9:00-11:00, 14:00-17:00
# 建议: 11:00-14:00, 19:00-21:00

# 4. 检查网络连接
# 确保网络稳定
# 避免使用不稳定的 WiFi
```

---

## 常见错误速查表

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `access_token missing` | 登录状态丢失 | 重新登录获取 Cookie |
| `Slider verification required` | 需要滑块验证 | 人工完成验证 |
| `Daily limit reached` | 达到每日上限 | 换账号或等明天 |
| `VIP membership required` | 需要 VIP 权限 | 升级 VIP 或调整策略 |
| `Account restricted` | 账号被限制 | 停止操作，等待解封 |
| `Page not loaded` | 页面加载超时 | 增加超时时间，刷新重试 |
| `Element not found` | 选择器不匹配 | 更新选择器，检查页面结构 |
| `Network Error` | 网络连接问题 | 检查网络设置 |
| `Too many requests` | 请求频率过高 | 增加间隔，降低频率 |

---

## 调试技巧

### 1. 保存调试截图
```python
# 关键步骤保存截图
mcp_chrome_screenshot(name=f"maimai_debug_{int(time.time())}")
```

### 2. 输出页面 HTML
```python
# 解析失败时保存页面源码
html = mcp_chrome_javascript(code="return document.documentElement.outerHTML")
with open(f"maimai_debug_{int(time.time())}.html", "w") as f:
    f.write(html)
```

### 3. 检查浏览器控制台
```python
# 获取控制台错误信息
logs = mcp_chrome_javascript(code="""
    return window.console?.logs?.slice(-10) || [];
""")
print("浏览器控制台日志:", logs)
```

---

## 脉脉风控特点总结

```text
脉脉是所有招聘平台中风控最严格的之一:

1. 滑块验证: 极验滑块，几乎无法自动化绕过
2. 行为分析: 对操作频率、鼠标轨迹、页面停留时间都有检测
3. 频率限制: 免费账号限制非常严格 (~50 次/天)
4. IP 监控: 短时间大量请求会立即触发验证
5. 多设备检测: 不允许多设备同时登录

最佳实践:
✅ 使用有头模式登录和处理验证
✅ 操作间隔 10 秒以上
✅ 只在白天工作时间段操作
✅ 每次操作后滚动页面模拟浏览
✅ 使用多个账号轮换
✅ 遇到风控立即停止，不要硬扛
```

---

## 联系支持

如遇到本文档未涵盖的问题，请：
1. 检查脉脉帮助中心和社区
2. 查看最新的页面结构变化
3. 更新选择器定义
4. 联系脉脉客服（账号问题）
