# 猎聘 CLI 命令契约

## 命令结构

```bash
python has_cli.py liepin <command> [options]
```

## 可用命令

### 1. 登录命令

```bash
python has_cli.py liepin login [options]
```

**选项:**
- `--account <name>`: 账号名称 (默认: default)
- `--headed`: 显示浏览器窗口 (默认: 无头模式)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [猎聘] 账号 'default' 登录流程启动
  请通过 Hermes Agent 执行以下步骤:
  1. mcp_chrome_navigate(url='https://www.liepin.com/')
  2. 等待二维码出现并扫码
  3. 登录成功后调用 save_cookies() 保存 Cookie
```

**返回码:**
- `0`: 登录流程启动成功
- `1`: 登录失败

---

### 2. Cookie 检查命令

```bash
python has_cli.py liepin check [options]
```

**选项:**
- `--account <name>`: 账号名称 (默认: default)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [猎聘] 账号 'default' Cookie 有效 ✓
```

**返回码:**
- `0`: Cookie 有效
- `1`: Cookie 无效或不存在

---

### 3. 搜索命令

```bash
python has_cli.py liepin search [options]
```

**选项:**
- `--keyword <text>`, `-k <text>`: 搜索关键词 (必填)
- `--city <name>`, `-c <name>`: 城市筛选
- `--salary <range>`, `-s <range>`: 薪资范围 (如: 20-30k)
- `--experience <years>`, `-e <years>`: 工作经验 (如: 3-5年)
- `--pages <num>`, `-p <num>`: 采集页数 (默认: 1)
- `--account <name>`: 账号名称 (默认: default)
- `--output <path>`, `-o <path>`: 输出文件路径 (默认: output/liepin_search_*.json)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [猎聘] 开始搜索: 'Python 开发'
  城市: 北京, 页数: 1
  请通过 Hermes Agent 执行搜索流程
[2026-05-11 23:01:00] INFO  已采集 25 位候选人，保存至: output/liepin_search_20260511_230100.json
```

**返回码:**
- `0`: 搜索成功
- `1`: 搜索失败（未登录）

---

### 4. 详情采集命令

```bash
python has_cli.py liepin fetch [options]
```

**选项:**
- `--id <candidate_id>`: 候选人 ID (必填)
- `--account <name>`: 账号名称 (默认: default)
- `--output <path>`, `-o <path>`: 输出文件路径

---

## Cookie 存储格式

**文件位置:** `cookies/liepin_<account>.json`

```json
{
  "account": "default",
  "platform": "liepin",
  "created_at": "2026-05-11T23:00:00",
  "cookies": [
    {
      "name": "uid",
      "value": "...",
      "domain": ".liepin.com",
      "path": "/",
      "expires": 1234567890,
      "httpOnly": true,
      "secure": true
    }
  ]
}
```

---

## 数据输出格式

### JSON 格式 (`output/liepin_search_*.json`)

```json
{
  "search_info": {
    "platform": "liepin",
    "keyword": "Python 开发",
    "city": "北京",
    "pages": 1,
    "collected_at": "2026-05-11 23:00:00",
    "total_candidates": 25
  },
  "candidates": [
    {
      "platform": "liepin",
      "candidate_id": "12345678",
      "name": "张三",
      "current_title": "高级 Python 工程师",
      "current_company": "某科技有限公司",
      "expected_salary": "25-35k·14薪",
      "location": "北京",
      "work_years": "5年",
      "age": 28,
      "gender": "男",
      "profile_url": "https://hunter.liepin.com/resume/detail/12345678",
      "experiences": [...],
      "educations": [...],
      "skills": ["Python", "Django", "MySQL"],
      "contact": {
        "phone": "138****8888",
        "email": "zhang***@example.com"
      },
      "last_active": "3天前"
    }
  ]
}
```

### CSV 格式 (`output/liepin_search_*.csv`)

扁平结构，适合 Excel 查看和数据分析。

---

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `NOT_LOGGED_IN` | 未登录或 Cookie 过期 | 重新执行 `login` 命令扫码登录 |
| `COOKIE_NOT_FOUND` | Cookie 文件不存在 | 先执行 `login` 命令 |
| `SEARCH_FAILED` | 搜索请求失败 | 检查网络连接，可能需要处理验证码 |
| `RATE_LIMITED` | 请求频率过高 | 增加请求间隔，降低采集速度 |
| `CAPTCHA_REQUIRED` | 需要验证码 | 人工处理验证码后继续 |
| `PAGE_PARSE_ERROR` | 页面解析失败 | 页面结构可能已变更，需要更新选择器 |

---

## 使用示例

### 完整工作流

```bash
# 1. 登录（扫码）
python has_cli.py liepin login --account myaccount

# 2. 检查 Cookie 状态
python has_cli.py liepin check --account myaccount

# 3. 执行搜索
python has_cli.py liepin search --keyword "Python 开发" --city "北京" --pages 3 --account myaccount

# 4. 采集单个候选人详情
python has_cli.py liepin fetch --id 12345678 --account myaccount
```

### 多账号管理

```bash
# 账号 1
python has_cli.py liepin login --account account1
python has_cli.py liepin search --keyword "Java" --account account1

# 账号 2
python has_cli.py liepin login --account account2
python has_cli.py liepin search --keyword "前端" --account account2
```

---

## 注意事项

1. **验证码处理**: 采集过程中可能出现验证码，需要人工处理
2. **频率限制**: 建议每采集 1-2 页暂停 10-30 秒
3. **数据隐私**: 导出的数据包含候选人联系方式，请妥善保管
4. **Cookie 有效期**: 猎聘 Cookie 通常有效期为 7-14 天
5. **页面变更**: 网站结构可能随时变更，如解析失败请更新选择器
