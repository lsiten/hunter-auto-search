# 脉脉 CLI 命令契约

## 命令结构

```bash
python has_cli.py maimai <command> [options]
```

## 可用命令

### 1. 登录命令

```bash
python has_cli.py maimai login [options]
```

**选项:**
- `--account <name>`: 账号名称 (默认: default)
- `--headed`: 显示浏览器窗口 (默认: True，脉脉登录建议使用有头模式)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [脉脉] 账号 'default' 登录流程启动
  请通过 Hermes Agent 执行以下步骤:
  1. mcp_chrome_navigate(url='https://maimai.cn/login')
  2. 选择手机号验证码或扫码登录
  3. 登录成功后调用 save_cookies() 保存 Cookie
```

**返回码:**
- `0`: 登录流程启动成功
- `1`: 登录失败

---

### 2. Cookie 检查命令

```bash
python has_cli.py maimai check [options]
```

**选项:**
- `--account <name>`: 账号名称 (默认: default)

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [脉脉] 账号 'default' Cookie 有效 ✓
```

**返回码:**
- `0`: Cookie 有效
- `1`: Cookie 无效或不存在

---

### 3. 搜索命令

```bash
python has_cli.py maimai search [options]
```

**选项:**
- `--keyword <text>`, `-k <text>`: 搜索关键词 (必填)
- `--city <name>`, `-c <name>`: 城市筛选
- `--company <name>`: 公司筛选
- `--position <name>`: 职位筛选
- `--industry <name>`: 行业筛选
- `--school <name>`: 学校筛选
- `--degree <level>`: 人脉度数 (1st, 2nd, 3rd)
- `--pages <num>`, `-p <num>`: 采集页数 (默认: 1)
- `--account <name>`: 账号名称 (默认: default)
- `--output <path>`, `-o <path>`: 输出文件路径

**输出示例:**
```
[2026-05-11 23:00:00] INFO  [脉脉] 开始搜索: '产品经理'
  城市: 北京, 页数: 1
  请通过 Hermes Agent 执行搜索流程
[2026-05-11 23:01:00] INFO  已采集 20 位候选人，保存至: output/maimai_search_20260511_230100.json
```

**返回码:**
- `0`: 搜索成功
- `1`: 搜索失败（未登录）

---

### 4. 详情采集命令

```bash
python has_cli.py maimai fetch [options]
```

**选项:**
- `--id <candidate_id>`: 候选人 ID (必填)
- `--account <name>`: 账号名称 (默认: default)
- `--output <path>`, `-o <path>`: 输出文件路径

---

## Cookie 存储格式

**文件位置:** `cookies/maimai_<account>.json`

```json
{
  "account": "default",
  "platform": "maimai",
  "created_at": "2026-05-11 23:00:00",
  "cookies": [
    {
      "name": "access_token",
      "value": "...",
      "domain": ".maimai.cn",
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
| `access_token` | 访问令牌 | ⭐⭐⭐ 必需 |
| `uid` | 用户 ID | ⭐⭐⭐ 必需 |
| `sess` | 会话 ID | ⭐⭐ 推荐 |

---

## 数据输出格式

### JSON 格式 (`output/maimai_search_*.json`)

```json
{
  "search_info": {
    "platform": "maimai",
    "keyword": "产品经理",
    "city": "北京",
    "pages": 1,
    "collected_at": "2026-05-11 23:00:00",
    "total_candidates": 20
  },
  "candidates": [
    {
      "platform": "maimai",
      "candidate_id": "123456",
      "name": "张三",
      "current_title": "高级产品经理",
      "current_company": "字节跳动",
      "location": "北京",
      "profile_url": "https://maimai.cn/web/personal?uid=123456",
      "degree": "2nd",
      "mutual_contacts": 15,
      "experiences": [
        {
          "company": "字节跳动",
          "position": "高级产品经理",
          "duration": "2020 - 至今",
          "description": "负责抖音核心产品..."
        }
      ],
      "educations": [
        {
          "school": "清华大学",
          "degree": "硕士",
          "major": "计算机科学",
          "duration": "2016 - 2019"
        }
      ],
      "skills": ["产品设计", "用户增长", "数据分析"],
      "tags": ["海归", "大厂经历", "创业经验"],
      "contact": {
        "email": "zhangsan@example.com",
        "phone": "138****8888",
        "wechat": "zhangsan_wx"
      }
    }
  ]
}
```

### CSV 格式 (`output/maimai_search_*.csv`)

扁平结构，适合 Excel 查看和数据分析。

---

## 搜索参数详解

### 关键词搜索 (`--keyword`)
支持的搜索语法：
```
"产品经理" AND "北京"
"数据" OR "算法"
"架构师" NOT "实习"
```

### 城市筛选 (`--city`)
支持的城市格式：
```
北京
上海市
深圳
杭州
广州
成都
```

### 人脉度数筛选 (`--degree`)
- `1st`: 1 度人脉（直接联系人）
- `2nd`: 2 度人脉（朋友的朋友）- 数量最多
- `3rd`: 3 度及以上

---

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `NOT_LOGGED_IN` | 未登录或 Cookie 过期 | 重新执行 `login` 命令 |
| `COOKIE_NOT_FOUND` | Cookie 文件不存在 | 先执行 `login` 命令 |
| `SEARCH_FAILED` | 搜索请求失败 | 检查网络连接和登录状态 |
| `RATE_LIMITED` | 请求频率过高触发风控 | 增加请求间隔，暂停后重试 |
| `SLIDER_CAPTCHA` | 需要滑块验证 | 人工处理滑块验证后继续 |
| `DAILY_LIMIT` | 达到每日搜索上限 | 换账号或等第二天继续 |
| `MEMBER_REQUIRED` | 需要会员权限 | 升级 VIP 账号或减少需求 |
| `PROFILE_LOCKED` | 账号被临时限制 | 停止操作，等待解封 |
| `PAGE_PARSE_ERROR` | 页面解析失败 | 页面结构可能已变更，更新选择器 |

---

## 使用示例

### 完整工作流

```bash
# 1. 登录 (建议使用有头模式)
python has_cli.py maimai login --account my_account --headed

# 2. 检查 Cookie 状态
python has_cli.py maimai check --account my_account

# 3. 基础搜索
python has_cli.py maimai search --keyword "技术总监" --city 北京 --pages 3

# 4. 高级筛选搜索
python has_cli.py maimai search --keyword "算法工程师" --company "阿里巴巴" --school "北京大学"

# 5. 采集单个候选人详情
python has_cli.py maimai fetch --id 12345678
```

### 多账号管理

```bash
# 账号 1 - 白天使用
python has_cli.py maimai login --account recruiter_day
python has_cli.py maimai search --keyword "销售经理" --account recruiter_day

# 账号 2 - 晚上使用
python has_cli.py maimai login --account recruiter_night
python has_cli.py maimai search --keyword "技术经理" --account recruiter_night
```

---

## 性能建议

### 采集速度设置
```text
推荐配置 (平衡速度与安全):
┌───────────────┬───────────────┐
│ 参数          │ 推荐值        │
├───────────────┼───────────────┤
│ 请求间隔      │ 5-10 秒       │
│ 单页等待      │ 8-12 秒       │
│ 每 20 页暂停  │ 10 分钟       │
│ 每日采集量    │ 100-300 条    │
│ 每小时采集量  │ 30-50 条      │
└───────────────┴───────────────┘
```

### 批量采集脚本示例
```bash
#!/bin/bash
KEYWORDS=("Java" "Python" "前端" "产品经理")
for kw in "${KEYWORDS[@]}"; do
    echo "开始搜索: $kw"
    python has_cli.py maimai search --keyword "$kw" --pages 2
    echo "休息 8 分钟..."
    sleep 480
done
```

---

## 注意事项

1. **账号安全**: 脉脉风控非常严格，请谨慎控制采集频率，避免账号被封
2. **滑块验证**: 脉脉登录和高频操作时会出现滑块验证码，需要人工处理
3. **每日限制**: 免费账号每日搜索次数有限 (~50 次)，VIP 账号限制更宽松
4. **页面变更**: 脉脉页面结构更新频繁，请定期检查选择器有效性
5. **人脉层级**: 2 度人脉数量最多，是主要的搜索对象
6. **联系方式**: 大部分联系方式需要 VIP 权限或对方同意才能查看
7. **工作时间**: 建议只在白天工作时间段操作，模拟真实人类行为
8. **IP 稳定**: 避免频繁切换 IP，保持网络环境稳定
