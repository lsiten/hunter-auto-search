# 猎聘故障排除指南

> 本文档记录猎聘平台常见问题和解决方案，帮助快速定位和解决问题。

---

## 目录

1. [登录问题](#登录问题)
2. [搜索问题](#搜索问题)
3. [解析问题](#解析问题)
4. [验证码问题](#验证码问题)
5. [性能问题](#性能问题)
6. [数据导出问题](#数据导出问题)

---

## 登录问题

### 问题 1: 二维码不显示

**症状:**
```
[猎聘] 打开登录页面，但二维码区域空白
```

**可能原因:**
1. 网络连接问题，资源加载失败
2. 页面未完全加载完成
3. CDN 资源被防火墙拦截

**解决方案:**
```python
# 1. 检查网络连接
mcp_chrome_navigate(url="https://www.baidu.com")

# 2. 刷新猎聘页面
mcp_chrome_navigate(url="https://www.liepin.com/")
time.sleep(5)  # 等待页面完全加载

# 3. 检查二维码元素
qrcode = mcp_chrome_read_page(filter="interactive")
if not any("qrcode" in str(elem) for elem in qrcode):
    print("二维码未加载，尝试刷新")
    mcp_chrome_click_element(selector=".refresh-qrcode")
```

---

### 问题 2: 扫码后无响应

**症状:**
- 手机扫码确认后，网页没有跳转
- 仍然显示二维码页面

**可能原因:**
1. 扫码超时（二维码已过期）
2. 网络延迟导致状态未同步
3. 浏览器缓存问题

**解决方案:**
```python
# 1. 检查二维码是否过期
time.sleep(30)  # 等待用户扫码
page_content = mcp_chrome_get_web_content()

if "二维码已失效" in page_content.get("text", ""):
    print("二维码已过期，正在刷新...")
    mcp_chrome_click_element(selector=".refresh-qrcode")

# 2. 检查是否已登录
user_avatar = mcp_chrome_read_page(filter="interactive")
if any("user-avatar" in str(elem) for elem in user_avatar):
    print("登录成功！")
    # 保存 Cookie
    cookies = mcp_chrome_javascript(code="return document.cookie")
    searcher.save_cookies(cookies)
```

---

### 问题 3: Cookie 保存后仍无法登录

**症状:**
```
[猎聘] 账号 'default' 未找到 Cookie
```

**可能原因:**
1. Cookie 保存路径错误
2. Cookie 文件损坏
3. Cookie 已过期

**解决方案:**
```bash
# 1. 检查 Cookie 文件
ls -la cookies/liepin_*.json

# 2. 查看 Cookie 内容
cat cookies/liepin_default.json

# 3. 重新登录获取新 Cookie
python has_cli.py liepin login --account default
```

---

## 搜索问题

### 问题 1: 搜索结果为空

**症状:**
```
[猎聘] 开始搜索: 'Python 开发'
[猎聘] 已采集 0 位候选人
```

**可能原因:**
1. 关键词太冷门
2. 筛选条件太严格
3. 页面未完全加载
4. 登录状态失效

**解决方案:**
```python
# 1. 检查登录状态
if not searcher.check_cookie():
    print("Cookie 已过期，请重新登录")
    exit(1)

# 2. 放宽筛选条件
print("尝试放宽筛选条件...")
print("移除城市、薪资、经验限制")

# 3. 检查页面加载状态
time.sleep(5)  # 等待搜索结果加载
page_data = mcp_chrome_get_web_content()

if "暂无符合条件的简历" in page_data.get("text", ""):
    print("确实无搜索结果，请调整关键词")
```

---

### 问题 2: 只能采集第一页

**症状:**
- 第一页采集正常
- 点击下一页后无数据
- 分页按钮点击无效

**可能原因:**
1. 分页选择器错误
2. AJAX 加载需要等待
3. 反爬虫限制

**解决方案:**
```python
# 1. 等待 AJAX 加载完成
mcp_chrome_click_element(selector=".next-page")
time.sleep(3)  # 等待数据加载

# 2. 检查页面是否更新
current_page = mcp_chrome_javascript(
    code="return document.querySelector('.current').textContent"
)
print(f"当前页码: {current_page}")

# 3. 滚动触发加载
mcp_chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight)")
time.sleep(2)
```

---

## 解析问题

### 问题 1: 字段解析为空

**症状:**
```
候选人名称: None
当前职位: None
```

**可能原因:**
1. 页面结构变更
2. 选择器不匹配
3. 数据异步加载

**解决方案:**
```python
# 1. 打印完整页面结构调试
page_data = mcp_chrome_get_web_content(htmlContent=True)
print(page_data.get("html", "")[:5000])  # 查看前 5000 字符

# 2. 尝试备用选择器
SELECTORS = [
    ".resume-name",    # 首选
    ".user-name",      # 备选 1
    ".name",           # 备选 2
]

for selector in SELECTORS:
    try:
        name = mcp_chrome_javascript(
            code=f"return document.querySelector('{selector}')?.textContent"
        )
        if name:
            print(f"使用选择器 {selector} 获取成功: {name}")
            break
    except:
        continue
```

---

### 问题 2: 联系方式无法获取

**症状:**
- 其他字段正常
- 手机号、邮箱始终为空

**可能原因:**
1. 需要点击"查看联系方式"按钮
2. 权限不足（账号级别不够）
3. 需要消耗查看次数

**解决方案:**
```python
# 1. 点击查看联系方式按钮
try:
    mcp_chrome_click_element(selector=".view-contact-btn")
    time.sleep(2)  # 等待数据加载
except:
    print("无法点击查看联系方式按钮")

# 2. 检查是否有查看次数限制
page_content = mcp_chrome_get_web_content()
if "今日查看次数已用完" in page_content.get("text", ""):
    print("⚠️  今日查看次数已用完，请明天再试或升级账号")
```

---

## 验证码问题

### 问题 1: 出现滑块验证码

**症状:**
- 页面显示"请按住滑块，拖动到最右边"
- 无法继续采集

**可能原因:**
- 请求频率过高
- IP 被风控
- 账号行为异常

**解决方案:**
```python
# 1. 降低请求频率
print("检测到验证码，增加延迟...")
time.sleep(10)  # 增加等待时间

# 2. 提示人工处理
print("⚠️  需要人工处理验证码")
print("请在浏览器中完成滑块验证后继续")

# 3. 等待用户确认
input("处理完成后按 Enter 继续...")

# 4. 验证是否通过
page_content = mcp_chrome_get_web_content()
if "验证成功" in page_content.get("text", ""):
    print("✅ 验证通过，继续采集")
```

---

### 问题 2: 出现图片验证码

**症状:**
- 显示 4 张图片，需要选择正确的
- 无法自动识别

**解决方案:**
```python
# 猎聘图片验证码通常需要人工识别
print("⚠️  检测到图片验证码，需要人工处理")
print("请在浏览器中完成验证码选择后继续")
input("处理完成后按 Enter 继续...")
```

---

## 性能问题

### 问题 1: 采集速度过慢

**症状:**
- 每页采集需要 30 秒以上
- 整体效率很低

**优化方案:**
```python
# 1. 减少不必要的等待
# time.sleep(5)  # 移除过长等待
time.sleep(2)    # 使用更合理的等待

# 2. 批量获取数据而非逐个元素
# 一次性获取所有候选人卡片
cards = mcp_chrome_javascript(
    code="""
    return Array.from(document.querySelectorAll('.resume-card')).map(card => ({
        name: card.querySelector('.name')?.textContent,
        title: card.querySelector('.title')?.textContent,
        // 更多字段...
    }))
    """
)

# 3. 并发处理（谨慎使用，避免触发风控）
# 不建议浏览器层面并发，建议按顺序采集
```

---

### 问题 2: 内存占用过高

**症状:**
- 浏览器标签页卡顿
- 系统内存占用持续上升

**解决方案:**
```bash
# 1. 定期刷新页面（每采集 10 页刷新一次）
if page_num % 10 == 0:
    mcp_chrome_navigate(url="https://hunter.liepin.com/resume/search")
    time.sleep(3)

# 2. 清理浏览器缓存
mcp_chrome_javascript(code="localStorage.clear(); sessionStorage.clear();")
```

---

## 数据导出问题

### 问题 1: CSV 文件乱码

**症状:**
- Excel 打开 CSV 文件显示乱码
- 中文显示为问号或乱码

**解决方案:**
```python
# 确保使用 UTF-8 with BOM 编码
import csv

with open("output.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)

# 或者使用 Excel 打开时选择 UTF-8 编码
print("如遇乱码，请使用 Excel 的 '数据 > 自文本' 功能导入，并选择 UTF-8 编码")
```

---

### 问题 2: JSON 文件过大

**症状:**
- JSON 文件超过 100MB
- 打开和处理缓慢

**解决方案:**
```python
# 1. 分批导出，每 100 条一个文件
BATCH_SIZE = 100
for i in range(0, len(candidates), BATCH_SIZE):
    batch = candidates[i:i+BATCH_SIZE]
    DataExporter.to_json(batch, f"output/batch_{i//BATCH_SIZE+1}.json")

# 2. 压缩导出
import gzip
with gzip.open("output/candidates.json.gz", "wt", encoding="utf-8") as f:
    json.dump({"candidates": candidates}, f, ensure_ascii=False, indent=2)
```

---

## 常见错误速查表

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `No such element` | 选择器找不到元素 | 更新选择器，等待元素加载 |
| `Element not clickable` | 元素被遮挡或未就绪 | 等待后重试，滚动到可视区域 |
| `Timeout` | 页面加载超时 | 增加超时时间，检查网络 |
| `Stale element reference` | 元素已失效 | 重新获取元素 |
| `Rate limited` | 请求过于频繁 | 增加延迟，降低采集速度 |
| `Permission denied` | 账号权限不足 | 升级账号，减少采集量 |

---

## 调试技巧

### 1. 开启详细日志
```python
# 在 utils/log.py 中设置日志级别
logger.setLevel(logging.DEBUG)
```

### 2. 保存页面截图
```python
# 关键步骤保存截图
mcp_chrome_screenshot(name=f"debug_step_{step}")
```

### 3. 保存页面源码
```python
# 解析失败时保存页面源码
html = mcp_chrome_javascript(code="return document.documentElement.outerHTML")
with open(f"debug_page_{int(time.time())}.html", "w") as f:
    f.write(html)
```

---

## 联系支持

如遇到本文档未涵盖的问题，请：
1. 检查最新的页面结构
2. 更新选择器定义
3. 提交 Issue 到项目仓库
