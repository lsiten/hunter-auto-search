# 领英 CLI 命令契约

## 命令结构

```bash
python has_cli.py linkedin <command> [options]
```

## 可用命令

### 1. 登录命令

```bash
python has_cli.py linkedin login [options]
```

**选项:**
- `--account <name>`: 账号名称 (默认: default)
- `--headed`: 显示浏览器窗口 (默认: 无头模式)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [领英] 账号 'default' 登录流程启动
  请通过 Hermes Agent 执行以下步骤:
  1. mcp_chrome_navigate(url='https://www.linkedin.com/login')
  2. 输入账号密码登录
  3. 登录成功后调用 save_cookies() 保存 Cookie
```

**返回码:**
- `0`: 登录流程启动成功
- `1`: 登录失败

---

### 2. Cookie 检查命令

```bash
python has_cli.py linkedin check [options]
```

**选项:**
- `--account <name>`: 账号名称 (默认: default)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [领英] 账号 'default' Cookie 有效 ✓
```

**返回码:**
- `0`: Cookie 有效
- `1`: Cookie 无效或不存在

---

### 3. 搜索命令

```bash
python has_cli.py linkedin search [options]
```

**选项:**
- `--keyword <text>`, `-k <text>`: 搜索关键词 (必填)
- `--location <name>`, `-l <name>`: 地区筛选
- `--company <name>`, `-c <name>`: 当前公司筛选
- `--school <name>`, `-s <name>`: 学校筛选
- `--industry <name>`: 行业筛选
- `--network <degree>`: 人脉连接度 (1st, 2nd, 3rd)
- `--pages <num>`, `-p <num>`: 采集页数 (默认: 1)
- `--account <name>`: 账号名称 (默认: default)
- `--output <path>`, `-o <path>`: 输出文件路径

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [领英] 开始搜索: 'Python 开发'
  地区: 北京, 页数: 1
  请通过 Hermes Agent 执行搜索流程
[2026-05-11 23:01:00] INFO  已采集 10 位候选人，保存至: output/linkedin_search_20260511_230100.json
```

**返回码:**
- `0`: 搜索成功
- `1`: 搜索失败（未登录）

---

### 4. 详情采集命令

```bash
python has_cli.py linkedin fetch [options]
```

**选项:**
- `--id <candidate_id>`: 候选人 ID (必填，即领英 profile slug)
- `--account <name>`: 账号名称 (默认: default)
- `--output <path>`, `-o <path>`: 输出文件路径

---

## Cookie 存储格式

**文件位置:** `cookies/linkedin_<account>.json`

```json
{
  "account": "default",
  "platform": "linkedin",
  "created_at": "2026-05-11T23:00:00",
  "cookies": [
    {
      "name": "li_at",
      "value": "AQEDA...",
      "domain": ".linkedin.com",
      "path": "/",
      "expires": 1234567890,
      "httpOnly": true,
      "secure": true
    }
  ]
}
```

**关键 Cookie 说明:**
| Cookie | 作用 | 重要性 |
|--------|------|--------|
| `li_at` | 登录状态令牌 | ⭐⭐⭐ 必需 |
| `JSESSIONID` | 会话 ID | ⭐⭐⭐ 必需 |
| `lidc` | 负载均衡路由 | ⭐⭐ 推荐 |

---

## 数据输出格式

### JSON 格式 (`output/linkedin_search_*.json`)

```json
{
  "search_info": {
    "platform": "linkedin",
    "keyword": "Python 开发",
    "location": "北京",
    "pages": 1,
    "collected_at": "2026-05-11 23:00:00",
    "total_candidates": 10
  },
  "candidates": [
    {
      "platform": "linkedin",
      "candidate_id": "john-smith-123456",
      "name": "John Smith",
      "current_title": "Senior Software Engineer",
      "current_company": "Google",
      "location": "Beijing, China",
      "profile_url": "https://www.linkedin.com/in/john-smith-123456",
      "connections": "500+",
      "experiences": [
        {
          "company": "Google",
          "position": "Senior Software Engineer",
          "duration": "2020 - Present",
          "location": "Beijing",
          "description": "..."
        }
      ],
      "educations": [
        {
          "school": "清华大学",
          "degree": "Bachelor",
          "major": "Computer Science",
          "duration": "2016 - 2020"
        }
      ],
      "skills": ["Python", "Java", "Machine Learning"],
      "contact": {
        "email": "john@example.com",
        "phone": "+86 138 **** 8888"
      }
    }
  ]
}
```

### CSV 格式 (`output/linkedin_search_*.csv`)

扁平结构，适合 Excel 查看和数据分析。

---

## 搜索参数详解

### 关键词搜索 (`--keyword`)
支持领英高级搜索语法：
```
"Python" AND "北京"         # 同时包含
"数据科学家" OR "算法工程师" # 包含其一
"机器学习" NOT "实习"        # 排除
```

### 地区筛选 (`--location`)
支持的地区格式：
```
北京
Beijing, China
中国 北京
101084335 (领英地区代码)
```

### 人脉连接度 (`--network`)
- `1st`: 1 度人脉（直接联系人）
- `2nd`: 2 度人脉（朋友的朋友）
- `3rd`: 3 度及以上
- `all`: 全部连接度

---

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `NOT_LOGGED_IN` | 未登录或 Cookie 过期 | 重新执行 `login` 命令 |
| `COOKIE_NOT_FOUND` | Cookie 文件不存在 | 先执行 `login` 命令 |
| `SEARCH_FAILED` | 搜索请求失败 | 检查网络连接和登录状态 |
| `RATE_LIMITED` | 请求频率过高触发风控 | 增加请求间隔，暂停后重试 |
| `CAPTCHA_REQUIRED` | 需要验证码验证 | 人工处理验证码后继续 |
| `PROFILE_LOCKED` | 账号被临时锁定 | 暂停使用 24-48 小时 |
| `CONNECTION_LIMIT` | 搜索次数已达上限 | 使用高级账号或等待下月重置 |
| `PAGE_PARSE_ERROR` | 页面解析失败 | 页面结构可能已变更，更新选择器 |

---

## 使用示例

### 完整工作流

```bash
# 1. 登录
python has_cli.py linkedin login --account myaccount

# 2. 检查 Cookie 状态
python has_cli.py linkedin check --account myaccount

# 3. 基础搜索
python has_cli.py linkedin search --keyword "软件工程师" --location 北京 --pages 2

# 4. 高级筛选搜索
python has_cli.py linkedin search --keyword "数据科学家" --company "阿里巴巴" --school "清华大学"

# 5. 采集单个候选人详情
python has_cli.py linkedin fetch --id "zhang-san-456789"
```

### 多账号管理

```bash
# 账号 1 - 招聘专用
python has_cli.py linkedin login --account recruiter
python has_cli.py linkedin search --keyword "销售经理" --account recruiter

# 账号 2 - 技术专用
python has_cli.py linkedin login --account tech_recruiter
python has_cli.py linkedin search --keyword "全栈工程师" --account tech_recruiter
```

---

## 性能建议

### 采集速度设置
```text
推荐配置 (平衡速度与安全):
┌───────────────┬───────────────┐
│ 参数          │ 推荐值        │
├───────────────┼───────────────┤
│ 请求间隔      │ 3-5 秒        │
│ 单页等待      │ 5-8 秒        │
│ 每 10 页暂停  │ 5 分钟        │
│ 每日采集量    │ 200-500 条    │
│ 每小时采集量  │ 50-100 条     │
└───────────────┴───────────────┘
```

### 批量采集脚本示例
```bash
#!/bin/bash
KEYWORDS=("Python" "Java" "前端" "数据分析")
for kw in "${KEYWORDS[@]}"; do
    echo "开始搜索: $kw"
    python has_cli.py linkedin search --keyword "$kw" --pages 3
    echo "休息 3 分钟..."
    sleep 180
done
```

---

## 注意事项

1. **账号安全**: 领英风控严格，请谨慎控制采集频率，避免账号被封
2. **数据隐私**: 领英数据受隐私法保护，请合法使用，不得转售
3. **页面变更**: 领英页面结构经常更新，请定期检查选择器有效性
4. **语言设置**: 建议使用英文界面，选择器匹配更准确
5. **网络稳定**: 领英对网络质量敏感，请确保网络稳定
6. **Cookie 管理**: 定期检查 Cookie 状态，提前备份有效 Cookie
