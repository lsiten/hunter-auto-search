# 领英故障排除指南

> 本文档记录领英平台常见问题和解决方案，帮助快速定位和解决问题。

---

## 目录

1. [登录问题](#登录问题)
2. [搜索问题](#搜索问题)
3. [解析问题](#解析问题)
4. [风控与验证](#风控与验证)
5. [性能问题](#性能问题)
6. [数据导出问题](#数据导出问题)

---

## 登录问题

### 问题 1: 登录后立即退出

**症状:**
```
刚登录成功，刷新页面就需要重新登录
Cookie 保存后很快失效
```

**可能原因:**
1. 网络 IP 频繁变化
2. 浏览器指纹不一致
3. 多设备同时登录
4. 领英检测到异常活动

**解决方案:**
```python
# 1. 使用固定 IP 地址
# 2. 保持浏览器环境一致
# 3. 避免同一账号多设备同时登录

# 4. 登录后不要立即大量操作，先"养号"
time.sleep(60)  # 登录后静默 1 分钟

# 5. 模拟正常用户行为
mcp_chrome_javascript(code="window.scrollTo(0, 500)")  # 滚动页面
time.sleep(5)
mcp_chrome_javascript(code="window.scrollTo(0, 1000)")
```

---

### 问题 2: 出现人机验证

**症状:**
```
登录时显示"验证你是人类"
需要选择图片、拖动滑块等
```

**可能原因:**
1. IP 在领英风控名单中
2. 登录频率过高
3. 账号行为异常

**解决方案:**
```python
# 1. 人工处理验证
print("⚠️  检测到人机验证，请手动完成后继续")
input("完成后按 Enter 继续...")

# 2. 更换 IP 地址
# 使用 VPN 或代理切换网络

# 3. 降低操作频率
# 下次登录间隔至少 24 小时

# 4. 使用已登录的设备获取 Cookie
# 在正常浏览器登录后，导出 Cookie 使用
```

---

### 问题 3: Cookie 保存后无法使用

**症状:**
```
[领英] 账号 'default' Cookie 已过期
即使刚登录保存，check 也显示过期
```

**可能原因:**
1. 关键 Cookie 字段缺失
2. Cookie 格式不正确
3. 登录状态未完全建立

**解决方案:**
```bash
# 1. 检查 Cookie 文件内容
cat cookies/linkedin_default.json

# 2. 确认关键 Cookie 存在
# li_at 和 JSESSIONID 必须存在

# 3. 重新完整登录流程
# - 打开登录页
# - 输入账号密码
# - 等待完全跳转至首页
# - 确认右上角头像已显示
# - 然后再保存 Cookie
```

---

## 搜索问题

### 问题 1: 搜索结果数量很少

**症状:**
```
搜索"软件工程师"只返回几十个结果
正常应该有几千个结果
```

**可能原因:**
1. 搜索次数达到月度限额
2. 账号连接度过低
3. 搜索范围限制过严
4. 搜索语法错误

**解决方案:**
```python
# 1. 检查账号搜索限额
# 免费账号: ~300 次/月
# Premium 账号: 无限制

# 2. 扩大搜索范围
# 移除过多筛选条件
# 使用更宽泛的关键词

# 3. 使用布尔搜索语法
# "软件工程师" OR "后端开发"
# "Python" AND "北京" NOT "实习"

# 4. 升级到 Premium 账号
# 解锁无限搜索和更多筛选
```

---

### 问题 2: 滚动加载不触发

**症状:**
```
滚动到页面底部后没有新加载内容
只显示第一页约 10 个结果
```

**可能原因:**
1. 滚动位置不够低
2. 加载时间不足
3. 网络延迟导致加载失败

**解决方案:**
```python
# 1. 滚动到真正的底部
mcp_chrome_javascript(code="""
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
""")

# 2. 增加等待时间
time.sleep(5)  # 从 2 秒增加到 5 秒

# 3. 多次滚动触发
for i in range(3):
    mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    # 检查是否有新加载内容
    new_height = mcp_chrome_javascript(code="return document.body.scrollHeight")
    print(f"页面高度: {new_height}")
```

---

### 问题 3: 页面显示"搜索受限"

**症状:**
```
页面显示"已达到本月搜索上限"
或"升级账号解锁更多搜索结果"
```

**可能原因:**
1. 免费账号搜索次数用完
2. 账号被限制部分功能

**解决方案:**
```bash
# 方案 1: 等待下月重置
# 领英每月 1 号重置搜索次数

# 方案 2: 使用多个账号轮换
# account1 - 上半月使用
# account2 - 下半月使用

# 方案 3: 升级 LinkedIn Recruiter
# 专业招聘账号，功能更强大
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
3. A/B 测试显示不同布局

**解决方案:**
```python
# 1. 等待页面完全加载
time.sleep(5)  # 增加等待时间

# 2. 增加备用选择器
NAME_SELECTORS = [
    "h1.text-heading-xlarge",
    ".pv-top-card--list li:first-child",
    ".profile-name",
    ".name"
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

# 3. 检查领英是否在进行 A/B 测试
# 使用多个账号确认页面结构
```

---

### 问题 2: 联系方式无法获取

**症状:**
```
email: None
phone: None
即使点击了"查看联系方式"也获取不到
```

**可能原因:**
1. 候选人没有公开联系方式
2. 连接度不够（需要 1 度人脉）
3. 联系方式区域是懒加载的

**解决方案:**
```python
# 1. 点击查看联系方式按钮
try:
    mcp_chrome_click_element(selector="#top-card-text-details-contact-info")
    time.sleep(2)  # 等待弹窗出现
except:
    print("没有找到联系方式按钮，候选人可能未公开")

# 2. 检查是否需要连接后才能查看
# 领英限制: 通常只能查看 1 度人脉的联系方式

# 3. 从其他渠道获取联系方式
# - 邮箱可能在个人简介中
# - 网站链接可能指向个人主页
# - Twitter/GitHub 链接可能有线索
```

---

## 风控与验证

### 问题 1: 账号被临时限制

**症状:**
```
登录时显示"账号暂时受限"
需要验证邮箱或手机号
搜索功能无法使用
```

**可能原因:**
1. 操作频率过高触发风控
2. IP 地址异常（频繁切换）
3. 短时间内大量查看档案
4. 发送过多连接请求

**解决方案:**
```python
# 1. 立即停止所有操作
# 不要尝试登录或刷新

# 2. 等待冷却期
# 轻度限制: 24-48 小时
# 中度限制: 3-7 天
# 重度限制: 可能需要人工申诉

# 3. 完成验证步骤
# - 邮箱验证
# - 手机验证
# - 上传证件照片（极少情况）

# 4. 后续预防措施
time.sleep(10)  # 请求间隔从 2 秒增加到 10 秒
# 每天操作不超过 2 小时
# 模拟正常人类作息时间
```

---

### 问题 2: 频繁出现验证码

**症状:**
```
每次搜索都需要验证
滑动验证码、图片选择等
```

**可能原因:**
1. 请求频率太高
2. IP 被标记为高风险
3. 账号行为模式异常

**解决方案:**
```python
# 1. 大幅降低操作频率
# 原: 2 秒/次 → 改为: 10-15 秒/次
time.sleep(15)

# 2. 加入更多模拟人类行为
# 随机滚动页面
mcp_chrome_javascript(code=f"window.scrollTo(0, {random.randint(100, 1000)})")
time.sleep(random.randint(2, 5))

# 随机停留
time.sleep(random.randint(5, 15))

# 3. 更换 IP 地址
# 使用不同的代理或 VPN

# 4. 更换账号
# 使用备用账号继续操作
```

---

## 性能问题

### 问题 1: 领英页面加载极慢

**症状:**
```
页面加载需要 30 秒以上
经常超时失败
```

**可能原因:**
1. 网络到领英服务器延迟高
2. CDN 节点访问慢
3. 页面资源太多（图片、视频等）

**解决方案:**
```bash
# 1. 测试网络延迟
ping www.linkedin.com
# 理想: < 150ms
# 可接受: < 300ms
# 较差: > 500ms 考虑换网络

# 2. 使用更优的网络路线
# 尝试不同的代理服务器
# 选择离领英服务器近的节点

# 3. 禁用图片加载 (如浏览器支持)
# 可大幅加快加载速度
```

---

### 问题 2: 采集速度过慢

**症状:**
```
每小时只能采集几十个候选人
效率太低
```

**优化方案:**
```python
# 1. 批量获取而非逐个点击
# 从搜索列表页提取基本信息，只对高质量候选人查看详情

# 2. 并行策略 (谨慎使用)
# 注意: 领英风控严格，不建议真正的并行请求
# 替代方案: 多账号轮换操作

# 3. 优化等待时间
# 根据实际加载情况动态调整等待
import time
start = time.time()
while time.time() - start < 10:
    if page_loaded():
        break
    time.sleep(0.5)

# 4. 数据预处理
# 先快速筛选，后详细采集
```

---

## 数据导出问题

### 问题 1: 导出数据乱码

**症状:**
```
Excel 打开 CSV 文件中文显示乱码
"????" 或奇怪字符
```

**解决方案:**
```python
# 1. 使用 UTF-8 with BOM 编码
import csv

with open("output.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)

# 2. Excel 导入时指定编码
# 数据 → 自文本/CSV → 选择 UTF-8 编码
```

---

### 问题 2: 数据有大量重复

**症状:**
```
同一个候选人出现多次
去重后数量大幅减少
```

**可能原因:**
1. 翻页时边界重复
2. 搜索结果排序变化
3. 推荐算法重复推荐

**解决方案:**
```python
# 1. 基于候选人 ID 去重
# candidate_id 是唯一标识
seen_ids = set()
unique_candidates = []

for candidate in candidates:
    cid = candidate.get("candidate_id")
    if cid and cid not in seen_ids:
        seen_ids.add(cid)
        unique_candidates.append(candidate)

# 2. 记录采集范围和页码
# 避免重叠采集
```

---

## 常见错误速查表

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `li_at cookie missing` | 登录状态丢失 | 重新登录获取 Cookie |
| `Rate limit exceeded` | 请求频率过高 | 增加间隔，等待后重试 |
| `Challenge required` | 需要人机验证 | 人工完成验证 |
| `Profile not found` | 候选人档案已删除 | 跳过该候选人 |
| `Network Error` | 网络连接问题 | 检查网络和代理设置 |
| `Page not loaded` | 页面加载超时 | 增加超时时间，刷新重试 |
| `Element not found` | 选择器不匹配 | 更新选择器，检查页面语言 |
| `Account restricted` | 账号被限制 | 停止操作，等待解封 |
| `Search quota exceeded` | 搜索次数用完 | 换账号或等下月重置 |

---

## 调试技巧

### 1. 保存调试截图
```python
# 关键步骤保存截图
mcp_chrome_screenshot(name=f"debug_{int(time.time())}")
```

### 2. 输出页面 HTML
```python
# 解析失败时保存页面源码
html = mcp_chrome_javascript(code="return document.documentElement.outerHTML")
with open(f"debug_page_{int(time.time())}.html", "w") as f:
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

## 联系支持

如遇到本文档未涵盖的问题，请：
1. 检查领英社区和帮助中心
2. 查看最新的页面结构变化
3. 更新选择器定义
4. 提交 Issue 到项目仓库
