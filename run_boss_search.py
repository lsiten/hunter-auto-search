#!/usr/bin/env python3
"""
BOSS 直聘 - 完整搜索流程引导
=================================
这个脚本将引导你完成完整的 BOSS 直聘搜索流程

步骤：
1. 登录准备 - 扫码登录
2. 执行搜索 - 关键词搜索
3. 数据采集 - 解析候选人列表
4. 数据导出 - JSON/CSV 格式
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from searcher import BossSearcher
from searcher.models import Candidate, CandidateContact, CandidateExperience, CandidateEducation
from utils import log as logger, CookieManager, DataExporter


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_step(step_num, title):
    """打印步骤"""
    print(f"\n{'─' * 60}")
    print(f"  [{step_num}] {title}")
    print(f"{'─' * 60}\n")


def main():
    print_header("🚀 BOSS 直聘 - 完整搜索流程引导")
    
    # 初始化搜索器
    searcher = BossSearcher(account_name="default")
    
    # ========== 步骤 1: 准备登录 ==========
    print_step(1, "准备登录 BOSS 直聘")
    print("📱 请在 Hermes Agent 中执行以下操作：")
    print()
    print("1️⃣  加载 Skill:")
    print("   skill_view('boss-search')")
    print()
    print("2️⃣  打开登录页面:")
    print(f"   mcp_chrome_navigate(url='{searcher.login_url}')")
    print()
    print("3️⃣  显示二维码:")
    print("   mcp_chrome_screenshot()")
    print()
    print("4️⃣  扫码登录后，确认页面跳转到主页")
    print()
    
    input("👉 扫码登录完成后按 Enter 继续...")
    
    # ========== 步骤 2: 保存 Cookie ==========
    print_step(2, "保存登录状态 (Cookie)")
    
    # 保存模拟 Cookie（实际使用时从浏览器获取）
    cookie_data = {
        "last_check": datetime.now().isoformat(),
        "status": "valid",
        "login_time": datetime.now().isoformat()
    }
    
    searcher.save_cookie(cookie_data)
    logger.success(f"✅ Cookie 已保存到: {searcher.cookie_file}")
    
    # 验证 Cookie
    cookie_info = searcher.load_cookie_info()
    logger.info(f"📋 Cookie 信息: {cookie_info}")
    
    # ========== 步骤 3: 执行搜索 ==========
    print_step(3, "执行关键词搜索")
    
    # 提示在 Hermes 中执行搜索
    print("🔍 请在 Hermes Agent 中执行以下搜索操作：")
    print()
    print("1️⃣  打开搜索页面:")
    print(f"   mcp_chrome_navigate(url='{searcher.search_url}')")
    print()
    print("2️⃣  输入搜索关键词（例如: Python 开发、前端工程师）")
    print()
    print("3️⃣  点击搜索按钮")
    print()
    print("4️⃣  获取页面内容用于解析:")
    print("   mcp_chrome_get_web_content(htmlContent=true)")
    print()
    
    # ========== 步骤 4: 模拟数据解析 ==========
    print_step(4, "解析候选人数据")
    
    logger.info("📝 正在解析候选人列表...")
    
    # 创建模拟的候选人数据（实际使用时从 HTML 解析）
    candidates = [
        Candidate(
            platform="boss",
            candidate_id=f"demo_{i:04d}",
            name=f"候选人{i:03d}",
            age=25 + i,
            gender="男" if i % 2 == 0 else "女",
            location="北京",
            current_title=f"高级{keyword}工程师" if i % 2 == 0 else f"{keyword}开发工程师",
            current_company=f"字节跳动" if i % 3 == 0 else f"阿里巴巴" if i % 3 == 1 else "腾讯",
            current_salary=f"{20 + i * 5}K",
            expected_salary=f"{25 + i * 5}K-{35 + i * 5}K",
            work_years=f"{3 + i}年",
            experiences=[
                CandidateExperience(
                    company=f"公司A-{i}",
                    title=f"工程师",
                    duration=f"202{i}-至今",
                    description=f"负责{keyword}相关开发工作"
                ),
                CandidateExperience(
                    company=f"公司B-{i}",
                    title=f"初级工程师",
                    duration=f"202{i-1}-202{i}"
                )
            ],
            educations=[
                CandidateEducation(
                    school=f"北京大学" if i % 2 == 0 else "清华大学",
                    degree="本科",
                    major="计算机科学与技术"
                )
            ],
            skills=[keyword, "Python", "Django", "MySQL", "Redis"],
            contact=CandidateContact(
                phone=f"138****{1000+i}",
                email=f"candidate{i}@example.com"
            ),
            profile_url=f"https://www.zhipin.com/geek/{i}",
            last_active=f"{i}小时前",
            collected_at=datetime.now().isoformat()
        )
        for i, keyword in enumerate(["Python", "Java", "Go", "前端", "后端"], 1)
    ]
    
    logger.success(f"✅ 成功解析 {len(candidates)} 位候选人")
    
    # ========== 步骤 5: 数据导出 ==========
    print_step(5, "数据导出")
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON 导出
    json_file = DataExporter.to_json(candidates, f"boss_search_result_{timestamp}")
    logger.success(f"📦 JSON 导出完成: {json_file}")
    
    # CSV 导出
    csv_file = DataExporter.to_csv(candidates, f"boss_search_result_{timestamp}")
    logger.success(f"📦 CSV 导出完成: {csv_file}")
    
    # ========== 步骤 6: 结果展示 ==========
    print_step(6, "搜索结果预览")
    
    print(f"{'序号':<6} {'姓名':<12} {'职位':<20} {'公司':<15} {'薪资':<12} {'地点'}")
    print("─" * 90)
    
    for i, c in enumerate(candidates, 1):
        print(f"{i:<6} {c.name:<12} {c.current_title:<20} {c.current_company:<15} {c.current_salary:<12} {c.location}")
    
    # ========== 完成 ==========
    print_header("🎉 搜索流程完成！")
    
    print("📊 统计信息:")
    print(f"   候选人数量: {len(candidates)} 位")
    print(f"   JSON 文件: {json_file}")
    print(f"   CSV 文件:  {csv_file}")
    print(f"   Cookie 文件: {searcher.cookie_file}")
    print()
    
    print("💡 下一步建议:")
    print("   1. 查看导出的数据文件")
    print("   2. 尝试不同的搜索关键词")
    print("   3. 测试其他招聘平台（猎聘、领英、脉脉）")
    print("   4. 使用数据验证工具检查数据质量")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断，退出程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
