# 故障排查指南

## 登录相关问题

### 问题 1: 二维码不显示
**症状**: 登录页面没有显示二维码，显示空白或加载中

**排查步骤**:
1. 检查网络连接是否正常
2. 确认可以正常访问 `https://www.zhipin.com`
3. 使用 `chrome_screenshot` 查看实际页面状态
4. 尝试刷新页面: `mcp_chrome_chrome_navigate(url=登录页)`

**解决方案**:
```python
# 强制刷新页面
mcp_chrome_chrome_navigate(url="https://www.zhipin.com/web/user/?ka=header-login")
time.sleep(5)
# 检查是否有其他登录方式（如账号密码）
elements = mcp_chrome_chrome_read_page(filter="interactive")
```

---

### 问题 2: 扫码后无法登录
**症状**: 用户已扫码，但页面没有跳转，仍显示登录状态

**排查步骤**:
1. 检查用户是否在 APP 上确认了登录
2. 检查是否有滑块验证或其他验证步骤
3. 使用 `chrome_screenshot` 确认页面状态

**解决方案**:
```python
# 等待一段时间让页面完成跳转
time.sleep(5)
# 检查是否出现了验证弹窗
elements = mcp_chrome_chrome_read_page(filter="interactive")
for elem in elements:
    if "验证" in elem.get("text", "") or "滑块" in elem.get("text", ""):
        # 需要用户手动完成验证
        print("检测到滑块验证，请手动完成")
        break
```

---

### 问题 3: Cookie 很快失效
**症状**: 刚登录后可以搜索，但过几个小时就需要重新登录

**可能原因**:
1. 使用了隐身窗口模式
2. 被检测到异常行为，强制登出
3. IP 地址发生变化

**解决方案**:
1. 不要使用隐身模式（默认配置）
2. 降低操作频率，增加间隔时间
3. 确保网络环境稳定，不要频繁切换 IP

---

## 搜索相关问题

### 问题 4: 搜索结果为空
**症状**: 执行搜索后没有找到任何结果

**排查步骤**:
1. 检查是否已登录: `has boss check --account my_account`
2. 确认关键词是否正确
3. 使用 `chrome_screenshot` 查看实际搜索结果页
4. 检查是否有滑块验证或登录弹窗

**解决方案**:
```python
# 1. 检查登录状态
if not is_logged_in:
    print("需要重新登录")
    # 执行登录流程

# 2. 检查是否有验证弹窗
elements = mcp_chrome_chrome_read_page(filter="interactive")
for elem in elements:
    if "验证" in elem.get("text", "") or "安全" in elem.get("text", ""):
        print("检测到安全验证，请手动完成")
        break
```

---

### 问题 5: 元素定位失败
**症状**: `chrome_click_element` 或 `chrome_fill_or_select` 报错找不到元素

**排查步骤**:
1. 使用 `chrome_read_page` 获取当前页面所有交互元素
2. 检查页面是否跳转或加载完成
3. 确认选择器是否仍然有效（BOSS 直聘可能改版）

**解决方案**:
```python
# 获取当前页面交互元素
elements = mcp_chrome_chrome_read_page(filter="interactive")
print("页面元素列表:")
for elem in elements:
    print(f"  - {elem.get('text', '')}: {elem.get('selector', '')}")

# 动态查找元素
for elem in elements:
    text = elem.get("text", "")
    if "搜索" in text and "按钮" in text.lower():
        print(f"找到搜索按钮: {elem.get('selector', '')}")
        break
```

---

### 问题 6: 被反爬拦截
**症状**: 页面显示 "访问过于频繁"、"请稍后再试"、验证码或空白页

**特征识别**:
- 包含 "频繁"、"稍后"、"验证"、"安全" 等关键词
- 页面空白但 HTTP 状态码正常
- 所有搜索结果都为空

**解决方案**:
1. **立即停止操作**: 不要再发送任何请求
2. **等待冷却**: 建议等待 30 分钟以上
3. **降低频率**: 恢复后将操作间隔调整为 10 秒以上
4. **更换账号**: 如果被封 IP，尝试切换账号或网络

**预防措施**:
- 每页采集间隔 >= 5 秒
- 每次搜索间隔 >= 10 秒
- 单次搜索不超过 5 页
- 每天总采集量控制在 500 条以内

---

## 数据相关问题

### 问题 7: 导出的 JSON 文件无法解析
**症状**: JSON 文件损坏或包含非法字符

**排查步骤**:
1. 检查导出过程中是否有中断
2. 查看 JSON 文件大小是否正常（不应为 0）

**解决方案**:
```python
import json

# 尝试修复 JSON
with open('broken.json', 'r', encoding='utf-8') as f:
    content = f.read()

# 移除非法控制字符
import re
content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)

data = json.loads(content)
```

---

## 性能问题

### 问题 8: 采集速度太慢
**症状**: 采集一页需要超过 30 秒

**优化建议**:
1. 关闭详情采集（只采集列表信息）: `--no-detail`
2. 减少每页采集数量
3. 调整超时设置
4. 使用更快的网络

---

## 调试技巧

### 启用详细日志
```python
# 在调用前设置日志级别
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### 截图验证
```python
# 关键步骤都截图保存
mcp_chrome_chrome_screenshot(storeBase64=True, savePng=True, name="step_1_login")
```

### 页面内容检查
```python
# 获取页面完整文本
content = mcp_chrome_chrome_get_web_content(textContent=True)
print(content[:500])  # 只打印前 500 字符
```

---

## 联系支持

如果以上方案都无法解决问题，请提供以下信息：
1. 错误截图或 `chrome_screenshot` 结果
2. 控制台完整错误日志
3. 执行的具体命令
4. 问题复现步骤
5. 系统环境（OS、Python 版本）
