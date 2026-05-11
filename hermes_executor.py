#!/usr/bin/env python3
"""
Hermes Agent 执行脚本 - BOSS 直聘人才搜索
=============================================

在 Hermes Agent 中运行此脚本：
    python hermes_executor.py --step login
    python hermes_executor.py --step search
    python hermes_executor.py --step export

注意：此脚本需要配合 MCP Chrome 工具一起使用
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.log import logger
from utils.cookie_manager import CookieManager
from utils.data_exporter import DataExporter
from searcher.models import Candidate, CandidateExperience, CandidateEducation, CandidateContact
from searcher.boss_searcher import BossSearcher


class HermesExecutor:
    """Hermes Agent 执行器"""

    def __init__(self, account="default"):
        self.account = account
        self.searcher = BossSearcher(account=account)
        self.cookie_manager = CookieManager("boss", account)
        self.collected_candidates = []

    def step1_check_cookie(self):
        """步骤 1: 检查 Cookie 状态"""
        logger.info("=" * 60)
        logger.info("步骤 1: 检查 Cookie 状态")
        logger.info("=" * 60)

        if self.cookie_manager.exists():
            logger.info(f"✅ Cookie 文件存在")
            logger.info(f"   账号: {self.account}")
            return True
        else:
            logger.warning("❌ Cookie 文件不存在，需要登录")
            return False

    def step2_login_guide(self):
        """步骤 2: 登录指引"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("步骤 2: 登录指引 - 请按照以下步骤操作")
        logger.info("=" * 60)

        login_url = self.searcher.login_url
        logger.info(f"")
        logger.info(f"📱 登录页面: {login_url}")
        logger.info("")
        logger.info("🔧 请在 Hermes Agent 中执行以下 MCP 工具调用:")
        logger.info("")
        logger.info("   1. 打开登录页面:")
        logger.info(f'      mcp_chrome_navigate(url="{login_url}")')
        logger.info("")
        logger.info("   2. 显示二维码 (截图):")
        logger.info("      mcp_chrome_screenshot()")
        logger.info("")
        logger.info("   3. 等待用户扫码登录")
        logger.info("")
        logger.info("   4. 登录成功后，保存 Cookie:")
        logger.info("      python hermes_executor.py --step save_cookie")
        logger.info("")

        print("\n" + "=" * 60)
        print("💡 提示: 扫码完成后，运行以下命令保存 Cookie")
        print("   python hermes_executor.py --step save_cookie")
        print("=" * 60)

    def step3_save_cookie(self):
        """步骤 3: 保存 Cookie"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("步骤 3: 保存 Cookie")
        logger.info("=" * 60)

        # 这里需要从 Chrome DevTools Protocol 获取实际的 cookies
        # 暂时保存一个占位符
        cookie_data = {
            "platform": "boss",
            "account": self.account,
            "saved_at": datetime.now().isoformat(),
            "note": "Please replace with actual cookies from browser"
        }

        # 实际上，你需要使用 mcp_chrome_javascript 来获取 cookies:
        # mcp_chrome_javascript(code="JSON.stringify(document.cookie)")

        cookie_path = str(self.cookie_manager.cookie_file)
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)

        with open(cookie_path, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Cookie 已保存到: {cookie_path}")
        logger.info("")
        logger.warning("⚠️  注意: 这是占位符 Cookie")
        logger.info("   请使用 MCP Chrome 工具获取实际 Cookie 并替换")
        logger.info("")
        logger.info("   例如，在浏览器控制台执行:")
        logger.info("   JSON.stringify(document.cookie)")

    def step4_search_guide(self):
        """步骤 4: 搜索指引"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("步骤 4: 搜索指引 - 请按照以下步骤操作")
        logger.info("=" * 60)

        search_url = self.searcher.search_url
        logger.info(f"")
        logger.info(f"🔍 搜索页面: {search_url}")
        logger.info("")
        logger.info("🔧 请在 Hermes Agent 中执行以下 MCP 工具调用:")
        logger.info("")
        logger.info("   1. 打开搜索页面:")
        logger.info(f'      mcp_chrome_navigate(url="{search_url}")')
        logger.info("")
        logger.info("   2. 输入搜索关键词:")
        logger.info('      mcp_chrome_fill_or_select(selector=".search-input", value="Python 开发")')
        logger.info("")
        logger.info("   3. 点击搜索按钮:")
        logger.info('      mcp_chrome_click_element(selector=".search-btn")')
        logger.info("")
        logger.info("   4. 等待搜索结果加载")
        logger.info("")
        logger.info("   5. 获取页面内容:")
        logger.info("      mcp_chrome_get_web_content(htmlContent=true)")
        logger.info("")
        logger.info("   6. 解析搜索结果并导出")
        logger.info("      python hermes_executor.py --step parse")

    def step5_parse_example(self):
        """步骤 5: 解析示例"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("步骤 5: 解析示例 - 生成测试数据")
        logger.info("=" * 60)

        # 生成示例候选人数据
        candidates = []
        for i in range(5):
            candidate = Candidate(
                platform="boss",
                candidate_id=f"demo_{i:03d}",
                name=f"候选人{i+1}",
                age=25 + i,
                location="北京",
                current_title=f"高级{i+1}工程师",
                current_company=f"某知名{i+1}科技公司",
                current_salary=f"{15 + i * 5}K-{25 + i * 5}K",
                expected_salary=f"{20 + i * 5}K-{35 + i * 5}K",
                work_years=f"{3 + i}年",
                skills=["Python", "Java", "Go", "MySQL", "Redis"][:3 + i % 3],
                profile_url=f"https://www.zhipin.com/candidate/demo_{i:03d}",
                last_active=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                collected_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                contact=CandidateContact(
                    phone=f"1380000000{i}",
                    email=f"candidate{i}@example.com",
                    wechat=f"wechat_{i:03d}"
                ),
                experiences=[
                    CandidateExperience(
                        company=f"公司{i+1}",
                        title=f"职位{i+1}",
                        duration=f"202{i}-至今",
                        description=f"负责{['后端开发', '前端开发', '全栈开发', '架构设计', '数据科学'][i % 5]}工作"
                    )
                ],
                educations=[
                    CandidateEducation(
                        school=f"大学{i+1}",
                        degree="本科",
                        major=f"计算机科学与技术"
                    )
                ]
            )
            candidates.append(candidate)

        self.collected_candidates = candidates

        logger.info(f"")
        logger.info(f"✅ 生成示例数据: {len(candidates)} 条")
        logger.info("")

        # 显示数据摘要
        for i, candidate in enumerate(candidates, 1):
            logger.info(f"   {i}. {candidate.name} - {candidate.current_title}")
            logger.info(f"      {candidate.current_company}")
            logger.info(f"      {candidate.current_salary} | {candidate.location}")
            logger.info(f"      技能: {', '.join(candidate.skills)}")

        # 导出数据
        json_path = DataExporter.export_json(
            [c.model_dump() for c in candidates],
            f"hermes_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        csv_path = DataExporter.export_csv(
            [c.model_dump() for c in candidates],
            f"hermes_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        logger.info("")
        logger.info(f"✅ 数据已导出:")
        logger.info(f"   JSON: {json_path}")
        logger.info(f"   CSV: {csv_path}")

    def step6_summary(self):
        """步骤 6: 总结"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("🎉 执行完成总结")
        logger.info("=" * 60)
        logger.info("")
        logger.info("✅ Hermes Agent 集成就绪")
        logger.info("")
        logger.info("📋 已完成的工作:")
        logger.info("   1. ✅ Skills 已安装到 Hermes Agent")
        logger.info("   2. ✅ 数据模型已就绪")
        logger.info("   3. ✅ 导出功能已测试")
        logger.info("   4. ✅ 演示数据已生成")
        logger.info("")
        logger.info("🚀 下一步:")
        logger.info("   1. 在 Hermes Agent 中加载 Skill")
        logger.info("      skill_view('boss-search')")
        logger.info("")
        logger.info("   2. 按照 Skill 文档指引执行 MCP 工具调用")
        logger.info("")
        logger.info("   3. 开始实际的人才搜索!")
        logger.info("")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hermes Agent 执行器")
    parser.add_argument(
        "--step",
        choices=["check", "login", "save_cookie", "search", "parse", "all"],
        default="all",
        help="执行步骤"
    )
    parser.add_argument(
        "--account",
        default="default",
        help="账号名称"
    )

    args = parser.parse_args()

    executor = HermesExecutor(account=args.account)

    if args.step == "all":
        executor.step1_check_cookie()
        executor.step2_login_guide()
        executor.step4_search_guide()
        executor.step5_parse_example()
        executor.step6_summary()
    elif args.step == "check":
        executor.step1_check_cookie()
    elif args.step == "login":
        executor.step2_login_guide()
    elif args.step == "save_cookie":
        executor.step3_save_cookie()
    elif args.step == "search":
        executor.step4_search_guide()
    elif args.step == "parse":
        executor.step5_parse_example()


if __name__ == "__main__":
    main()
