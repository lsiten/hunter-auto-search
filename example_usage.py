#!/usr/bin/env python3
"""
Hunter Auto Search 使用示例
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🎯 Hunter Auto Search 使用示例")
print("=" * 60)

# 示例 1: 使用数据模型创建候选人
print("\n📝 示例 1: 创建候选人数据")
print("-" * 40)

from searcher.models import Candidate, CandidateContact, CandidateExperience, CandidateEducation

# 创建联系方式
contact = CandidateContact(
    phone="13800138000",
    email="zhangsan@example.com",
    wechat="zhangsan_wx"
)

# 创建工作经历
exp1 = CandidateExperience(
    company="字节跳动",
    title="高级Python工程师",
    duration="2021-至今",
    description="负责AI平台后端开发，使用FastAPI、Django等框架"
)

exp2 = CandidateExperience(
    company="阿里巴巴",
    title="Python工程师",
    duration="2019-2021",
    description="电商平台核心系统开发"
)

# 创建教育背景
edu = CandidateEducation(
    school="清华大学",
    degree="硕士",
    major="计算机科学与技术",
    duration="2016-2019"
)

# 创建完整的候选人信息
candidate = Candidate(
    platform="boss",
    candidate_id="boss_12345",
    name="张三",
    gender="男",
    age=30,
    location="北京",
    current_title="高级Python工程师",
    current_company="字节跳动",
    current_salary="40-60K·15薪",
    expected_salary="50-70K",
    work_years="5-10年",
    contact=contact,
    experiences=[exp1, exp2],
    educations=[edu],
    skills=["Python", "FastAPI", "Django", "AI", "Machine Learning", "Docker", "K8s"],
    profile_url="https://www.zhipin.com/geek/12345",
    collected_at="2024-01-15",
    search_keyword="Python 高级工程师"
)

print(f"✅ 候选人创建成功: {candidate.name}")
print(f"   - 职位: {candidate.current_title}")
print(f"   - 公司: {candidate.current_company}")
print(f"   - 薪资: {candidate.current_salary}")
print(f"   - 工作经历: {len(candidate.experiences)} 条")
print(f"   - 技能: {', '.join(candidate.skills)}")

# 示例 2: 导出数据
print("\n💾 示例 2: 数据导出")
print("-" * 40)

from utils.data_exporter import DataExporter

# 导出为 JSON
candidates = [candidate]
json_path = DataExporter.to_json(candidates, "example_candidates")
print(f"✅ JSON 已导出: {os.path.basename(json_path)}")

# 导出为 CSV
csv_path = DataExporter.to_csv(candidates, "example_candidates")
print(f"✅ CSV 已导出: {os.path.basename(csv_path)}")

# 示例 3: 使用搜索器
print("\n🔍 示例 3: 初始化搜索器")
print("-" * 40)

from searcher.boss_searcher import BossSearcher

# 初始化 BOSS 直聘搜索器
searcher = BossSearcher("my_account")
print(f"✅ {searcher.platform_name} 搜索器已初始化")
print(f"   - 账号: {searcher.account}")
print(f"   - 登录页: {searcher.login_url}")
print(f"   - 搜索页: {searcher.search_url}")

# 示例 4: CLI 使用提示
print("\n💻 示例 4: CLI 命令行使用")
print("-" * 40)
print("   查看帮助:")
print("     python has_cli.py --help")
print("")
print("   BOSS 直聘命令:")
print("     python has_cli.py boss --help")
print("     python has_cli.py boss login --account my_account")
print("     python has_cli.py boss check --account my_account")
print("     python has_cli.py boss search --account my_account --keyword \"Python\"")
print("")
print("   其他平台:")
print("     python has_cli.py liepin --help")
print("     python has_cli.py linkedin --help")
print("     python has_cli.py maimai --help")

# 示例 5: Skill 使用提示
print("\n🧠 示例 5: Hermes Agent Skill 使用")
print("-" * 40)
print("   在 Hermes Agent 中加载 Skill:")
print("     skill_view('boss-search')")
print("")
print("   MCP 工具调用流程:")
print("     1. mcp_chrome_navigate(url=登录页)")
print("     2. 等待扫码登录")
print("     3. mcp_chrome_navigate(url=搜索页)")
print("     4. mcp_chrome_read_page() 解析搜索结果")
print("     5. 使用 parse_search_result() 处理数据")
print("     6. 导出为 JSON/CSV")

print("\n" + "=" * 60)
print("🎉 使用示例运行完成！")
print("=" * 60)
print("\n📚 更多文档:")
print("   - docs/QUICKSTART.md")
print("   - docs/MCP_WORKFLOW_GUIDE.md")
print("   - skills/boss-search/SKILL.md")
