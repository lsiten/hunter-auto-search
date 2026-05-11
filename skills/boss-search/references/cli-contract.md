# CLI 命令契约

## 通用约定

- 所有命令失败时返回非 0 退出码
- 所有命令成功时返回退出码 0
- 错误信息输出到 stderr，正常输出到 stdout
- 使用 JSON 格式输出结构化数据（当指定 `--json` 时）

## 命令契约

### `has boss login --account <name> [--headed]`

**功能**: 登录 BOSS 直聘并保存 Cookie

**输入参数**:
- `--account`: 账号标识（必填，用于区分不同账号的 Cookie）
- `--headed`: 是否显示浏览器窗口（可选，默认 False）

**输出**:
- 成功: 输出 "登录成功，Cookie 已保存"
- 失败: 输出错误原因

**退出码**:
- 0: 成功
- 1: 登录失败
- 2: 用户取消扫码
- 3: 二维码超时

**示例**:
```bash
$ has boss login --account my_account --headed
[INFO] 导航到登录页面...
[INFO] 二维码已加载，请使用 BOSS 直聘 APP 扫码
[INFO] 扫码成功，正在验证...
[INFO] 登录成功，Cookie 已保存
```

---

### `has boss check --account <name>`

**功能**: 检查指定账号的 Cookie 是否有效

**输入参数**:
- `--account`: 账号标识（必填）

**输出**:
- 有效: 输出 "Cookie 有效" + 账号基本信息
- 无效: 输出 "Cookie 已失效，需要重新登录"

**退出码**:
- 0: Cookie 有效
- 1: Cookie 无效
- 2: Cookie 文件不存在

**示例**:
```bash
$ has boss check --account my_account
[INFO] 检查 Cookie 有效性...
[INFO] Cookie 有效 - 用户: 张三 (某公司招聘者)
```

---

### `has boss search [OPTIONS]`

**功能**: 搜索候选人并导出数据

**输入参数**:
- `--account/-a`: 账号标识（必填）
- `--keyword/-k`: 搜索关键词（必填）
- `--city/-c`: 城市筛选（可选）
- `--salary/-s`: 薪资范围筛选（可选）
- `--pages/-p`: 采集页数（可选，默认 1）
- `--output/-o`: 导出格式（可选，json/csv，默认 json）
- `--headed`: 是否显示浏览器窗口（可选）

**输出**:
- 成功: 输出采集统计 + 导出文件路径
- 失败: 输出错误原因

**退出码**:
- 0: 搜索成功
- 1: 搜索失败
- 2: Cookie 无效
- 3: 网络错误

**示例**:
```bash
$ has boss search --account my_account --keyword "Python 开发" --pages 2
[INFO] 恢复会话成功
[INFO] 开始搜索: Python 开发
[INFO] 第 1 页: 采集到 30 条
[INFO] 第 2 页: 采集到 30 条
[INFO] 采集详情: 60/60
[INFO] 已导出: /path/to/output/search_Python_开发_20260511_223000.json
[INFO] 总计: 60 条候选人数据
```

## 错误码对照表

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 通用失败 |
| 2 | Cookie 无效/不存在 |
| 3 | 网络错误 |
| 4 | 页面元素未找到 |
| 5 | 用户取消操作 |
| 6 | 反爬拦截 |
