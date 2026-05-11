#!/bin/bash
# BOSS 直聘常用命令示例

# ============== 登录相关 ==============

# 1. 登录（无头模式）
has boss login --account default

# 2. 登录（有头模式，显示浏览器窗口）
has boss login --account default --headed

# 3. 检查 Cookie 状态
has boss check --account default

# ============== 搜索相关 ==============

# 4. 基本搜索
has boss search --account default --keyword "Python 开发"

# 5. 带城市筛选
has boss search --account default --keyword "算法工程师" --city "北京"

# 6. 带薪资筛选
has boss search --account default --keyword "产品经理" --salary "30-50K"

# 7. 多页采集
has boss search --account default --keyword "Java 开发" --pages 3

# 8. 导出为 CSV 格式
has boss search --account default --keyword "前端开发" --output csv

# 9. 完整参数示例
has boss search \
  --account default \
  --keyword "技术总监" \
  --city "上海" \
  --salary "50K以上" \
  --pages 5 \
  --output json \
  --headed

# ============== 多账号管理 ==============

# 使用不同的账号标识来管理多个账号
has boss login --account company_hr
has boss login --account headhunter

# 使用不同账号搜索
has boss search --account company_hr --keyword "销售经理"
has boss search --account headhunter --keyword "CTO"
