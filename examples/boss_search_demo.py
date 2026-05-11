#!/usr/bin/env python3
"""
BOSS 直聘搜索演示脚本
展示如何使用 MCP Chrome 工具进行完整的搜索流程

注意：此脚本是流程示例，实际运行需要在 Hermes Agent 环境中
使用 MCP Chrome 工具进行浏览器操作。
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from searcher.boss_searcher import BossSearcher
from searcher.models import Candidate, CandidateContact, CandidateExperience, CandidateEducation
from utils.data_exporter import DataExporter
from utils import log


class BossSearchDemo:
    """BOSS 直聘搜索演示流程"""
    
    def __init__(self, account: str = "default"):
        self.searcher = BossSearcher(account)
        self.exporter = DataExporter()
        self.collected_candidates = []
    
    def step1_login_flow(self):
        """步骤 1: 登录流程演示"""
        print("\n" + "="*60)
        print("步骤 1: BOSS 直聘登录流程")
        print("="*60)
        login_url = self.searcher.login_url
        print(f"登录地址: {login_url}")
        
        print(f"\nMCP 工具调用流程:")
        print(f"  1. mcp_chrome_navigate(url='{login_url}')")
        print(f"  2. mcp_chrome_read_page(filter='interactive')")
        print(f"  3. 识别二维码或登录按钮")
        print(f"  4. mcp_chrome_screenshot() -> 展示给用户扫码")
        print(f"  5. 等待用户扫码完成")
        print(f"  6. 保存 Cookie: {self.searcher.cookie_manager.cookie_file}")
        
        # 检查是否已有有效 Cookie
        is_valid = self.searcher.check_cookie()
        print(f"\n当前 Cookie 状态: {'存在' if is_valid else '不存在'}")
        
        if not is_valid:
            print("\n需要执行登录流程:")
            print("  - 请使用 Hermes Agent 加载 boss-search Skill")
            print("  - 执行扫码登录操作")
        
        return is_valid
    
    def step2_search_flow(self, keyword: str = "Python 开发", city: str = "北京"):
        """步骤 2: 搜索流程演示"""
        print("\n" + "="*60)
        print(f"步骤 2: 搜索流程 - 关键词: {keyword}, 城市: {city}")
        print("="*60)
        
        search_url = self.searcher.search_url
        print(f"搜索地址: {search_url}")
        
        print(f"\nMCP 工具调用流程:")
        print(f"  1. mcp_chrome_navigate(url='{search_url}')")
        print(f"  2. mcp_chrome_read_page(filter='interactive') -> 识别搜索框")
        print(f"  3. mcp_chrome_fill_or_select(selector='搜索框', value='{keyword}')")
        print(f"  4. mcp_chrome_click_element(selector='搜索按钮')")
        print(f"  5. mcp_chrome_wait_for_navigation -> 等待搜索结果")
        print(f"  6. mcp_chrome_read_page() -> 解析列表数据")
        
        print(f"\n页面选择器参考:")
        from searcher.boss_searcher import selectors
        selector_dict = {
            k: v for k, v in selectors.__dict__.items()
            if not k.startswith('_') and isinstance(v, str)
        }
        for key, value in list(selector_dict.items())[:5]:
            print(f"  - {key}: {value}")
        
        return search_url
    
    def step3_parse_list_data(self, raw_html_data: dict = None):
        """步骤 3: 解析列表页数据"""
        print("\n" + "="*60)
        print("步骤 3: 解析搜索结果列表")
        print("="*60)
        
        # 模拟解析的数据
        mock_candidates = self._create_mock_candidates(5)
        
        print(f"解析到 {len(mock_candidates)} 条候选人信息")
        print("\n候选人信息预览:")
        for i, candidate in enumerate(mock_candidates[:3], 1):
            print(f"\n  {i}. {candidate.name}")
            print(f"     职位: {candidate.current_title}")
            print(f"     公司: {candidate.current_company}")
            print(f"     薪资: {candidate.current_salary}")
            print(f"     地点: {candidate.location}")
        
        self.collected_candidates.extend(mock_candidates)
        return mock_candidates
    
    def step4_fetch_detail_page(self, candidate_id: str = "demo_001"):
        """步骤 4: 采集详情页"""
        print("\n" + "="*60)
        print(f"步骤 4: 采集候选人详情 - ID: {candidate_id}")
        print("="*60)
        
        print(f"\nMCP 工具调用流程:")
        print(f"  1. mcp_chrome_click_element(selector='候选人卡片')")
        print(f"  2. mcp_chrome_wait_for_navigation -> 等待详情页加载")
        print(f"  3. mcp_chrome_read_page() -> 解析详情页数据")
        print(f"  4. mcp_chrome_javascript(code='获取联系方式')")
        print(f"  5. mcp_chrome_navigate(history='back') -> 返回列表页")
        
        print(f"\n解析详情页字段:")
        detail_fields = [
            "工作经历（公司、职位、时间、描述）",
            "教育经历（学校、学历、专业、时间）",
            "技能标签",
            "联系方式（手机、邮箱、微信）",
            "自我描述",
            "求职期望"
        ]
        for field in detail_fields:
            print(f"  - {field}")
        
        # 创建一个详细的候选人示例
        detailed_candidate = self._create_detailed_candidate()
        print(f"\n详细候选人数据:")
        print(f"  - 工作经历: {len(detailed_candidate.experiences)} 条")
        print(f"  - 教育经历: {len(detailed_candidate.educations)} 条")
        print(f"  - 技能标签: {len(detailed_candidate.skills)} 个")
        
        return detailed_candidate
    
    def step5_pagination_flow(self, total_pages: int = 3):
        """步骤 5: 分页采集"""
        print("\n" + "="*60)
        print(f"步骤 5: 分页采集 - 共 {total_pages} 页")
        print("="*60)
        
        print(f"\nMCP 工具调用流程:")
        for page in range(1, total_pages + 1):
            print(f"\n  第 {page} 页:")
            print(f"    - 解析当前页 {len(self.collected_candidates)} 条")
            print(f"    - mcp_chrome_click_element(selector='下一页按钮')")
            print(f"    - 等待页面加载")
            print(f"    - mcp_chrome_read_page() -> 解析下一页")
        
        print(f"\n注意事项:")
        print(f"  - 每页间隔 2-5 秒，避免触发反爬")
        print(f"  - 模拟人类滚动行为")
        print(f"  - 遇到验证码时暂停，通知用户")
    
    def step6_export_data(self):
        """步骤 6: 数据导出"""
        print("\n" + "="*60)
        print("步骤 6: 数据导出")
        print("="*60)
        
        if not self.collected_candidates:
            print("没有收集到数据，使用模拟数据演示")
            self.collected_candidates = self._create_mock_candidates(10)
        
        # 导出 JSON
        json_path = DataExporter.to_json(
            self.collected_candidates,
            "boss_search_demo"
        )
        print(f"\nJSON 导出: {json_path}")
        
        # 导出 CSV
        csv_path = DataExporter.to_csv(
            self.collected_candidates,
            "boss_search_demo"
        )
        print(f"CSV 导出: {csv_path}")
        
        # 统计信息
        print(f"\n数据统计:")
        print(f"  - 总人数: {len(self.collected_candidates)}")
        platforms = set(c.platform for c in self.collected_candidates)
        print(f"  - 来源平台: {', '.join(platforms)}")
        
        return json_path, csv_path
    
    def step7_data_validation(self):
        """步骤 7: 数据验证"""
        print("\n" + "="*60)
        print("步骤 7: 数据验证与去重")
        print("="*60)
        
        try:
            from utils.data_validator import DataValidator
            
            validator = DataValidator()
            
            # 完整性评分
            scores = validator.batch_completeness_score(self.collected_candidates)
            avg_score = sum(scores) / len(scores) if scores else 0
            print(f"\n数据完整性评分:")
            print(f"  - 平均分: {avg_score:.1f}/100")
            print(f"  - 最高: {max(scores):.1f}/100")
            print(f"  - 最低: {min(scores):.1f}/100")
            
            # 去重
            deduplicated = validator.deduplicate_candidates(
                self.collected_candidates,
                merge=True
            )
            print(f"\n去重结果:")
            print(f"  - 原始数量: {len(self.collected_candidates)}")
            print(f"  - 去重后: {len(deduplicated)}")
            print(f"  - 移除重复: {len(self.collected_candidates) - len(deduplicated)}")
            
        except Exception as e:
            print(f"验证工具暂时不可用: {e}")
    
    def run_full_demo(self):
        """运行完整演示流程"""
        print("\n" + "#"*60)
        print("#     BOSS 直聘自动化搜索 - 完整流程演示")
        print("#"*60)
        
        # 步骤 1: 登录
        has_valid_cookie = self.step1_login_flow()
        
        # 步骤 2: 搜索
        self.step2_search_flow("Python 开发工程师", "北京")
        
        # 步骤 3: 解析列表
        self.step3_parse_list_data()
        
        # 步骤 4: 详情采集
        self.step4_fetch_detail_page()
        
        # 步骤 5: 分页
        self.step5_pagination_flow(3)
        
        # 步骤 6: 导出
        self.step6_export_data()
        
        # 步骤 7: 验证
        self.step7_data_validation()
        
        print("\n" + "#"*60)
        print("#     演示完成！")
        print("#"*60)
        print("\n下一步:")
        print("  1. 在 Hermes Agent 中加载 boss-search Skill")
        print("  2. 按照 Skill 文档执行 MCP 工具调用")
        print("  3. 使用此框架处理采集到的数据")
        print("  4. 查看 output/ 目录下的导出文件")
    
    def _create_mock_candidates(self, count: int = 5):
        """创建模拟候选人数据"""
        import random
        from datetime import datetime
        
        names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
        titles = ["Python 开发工程师", "高级 Python 工程师", "全栈开发工程师", 
                 "后端开发工程师", "数据工程师"]
        companies = ["字节跳动", "阿里巴巴", "腾讯", "美团", "京东", "百度", "小米"]
        salaries = ["20K-40K", "25K-45K", "30K-50K", "15K-25K", "35K-55K"]
        locations = ["北京", "上海", "深圳", "杭州", "广州"]
        experiences = ["3-5年", "5-10年", "1-3年", "10年以上"]
        
        candidates = []
        for i in range(count):
            name = random.choice(names)
            candidate = Candidate(
                platform="boss",
                candidate_id=f"boss_demo_{i:03d}",
                name=name,
                avatar_url=f"https://example.com/avatar/{i}.jpg",
                gender=random.choice(["男", "女"]),
                age=random.randint(25, 40),
                location=random.choice(locations),
                current_title=random.choice(titles),
                current_company=random.choice(companies),
                current_salary=random.choice(salaries),
                work_years=random.choice(experiences),
                profile_url=f"https://www.zhipin.com/candidate/{i}",
                last_active="刚刚",
                collected_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                skills=["Python", "Django", "Flask", "MySQL", "Redis"][:random.randint(3, 5)]
            )
            candidates.append(candidate)
        
        return candidates
    
    def _create_detailed_candidate(self):
        """创建详细的候选人数据"""
        from datetime import datetime
        
        candidate = Candidate(
            platform="boss",
            candidate_id="boss_detailed_001",
            name="技术大牛",
            avatar_url="https://example.com/avatar/detailed.jpg",
            gender="男",
            age=32,
            location="北京",
            current_title="高级 Python 开发工程师",
            current_company="某知名互联网公司",
            current_salary="35K-55K",
            expected_salary="40K-60K",
            work_years="8年",
            profile_url="https://www.zhipin.com/candidate/detail/001",
            last_active="30分钟前",
            collected_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            contact=CandidateContact(
                phone="138****8888",
                email="example@example.com",
                wechat="tech_master"
            ),
            skills=["Python", "Django", "FastAPI", "MySQL", "PostgreSQL", 
                    "Redis", "MongoDB", "Docker", "Kubernetes", "AWS"],
            experiences=[
                CandidateExperience(
                    company="字节跳动",
                    title="Python 开发工程师",
                    duration="2019.03 - 至今",
                    description="负责核心业务系统开发，参与微服务架构设计"
                ),
                CandidateExperience(
                    company="阿里巴巴",
                    title="后端开发工程师",
                    duration="2017.07 - 2019.02",
                    description="负责电商平台后端开发，优化系统性能"
                ),
                CandidateExperience(
                    company="某创业公司",
                    title="全栈开发工程师",
                    duration="2015.07 - 2017.06",
                    description="从 0 到 1 搭建公司技术架构"
                )
            ],
            educations=[
                CandidateEducation(
                    school="清华大学",
                    degree="硕士",
                    major="计算机科学与技术",
                    duration="2013 - 2015"
                ),
                CandidateEducation(
                    school="北京大学",
                    degree="学士",
                    major="软件工程",
                    duration="2009 - 2013"
                )
            ]
        )
        return candidate


if __name__ == "__main__":
    demo = BossSearchDemo(account="default")
    demo.run_full_demo()
