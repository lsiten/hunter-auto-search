#!/usr/bin/env python3
"""
多平台搜索流程演示
展示如何在不同招聘平台之间切换搜索
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from searcher import (
    BossSearcher,
    LiepinSearcher,
    LinkedInSearcher,
    MaimaiSearcher
)
from utils import log


class MultiPlatformSearchDemo:
    """多平台搜索流程演示"""
    
    def __init__(self):
        self.searchers = {
            "boss": BossSearcher("default"),
            "liepin": LiepinSearcher("default"),
            "linkedin": LinkedInSearcher("default"),
            "maimai": MaimaiSearcher("default")
        }
    
    def show_platform_comparison(self):
        """展示各平台对比"""
        print("\n" + "="*80)
        print("招聘平台功能对比")
        print("="*80)
        
        platforms_info = [
            {
                "name": "BOSS 直聘",
                "searcher": "BossSearcher",
                "skill": "boss-search",
                "login_url": self.searchers["boss"].login_url,
                "features": ["扫码登录", "关键词搜索", "城市筛选", "薪资筛选", "直接沟通"]
            },
            {
                "name": "猎聘",
                "searcher": "LiepinSearcher",
                "skill": "liepin-search",
                "login_url": self.searchers["liepin"].login_url,
                "features": ["账号登录", "高级搜索", "简历下载", "猎头服务"]
            },
            {
                "name": "领英",
                "searcher": "LinkedInSearcher",
                "skill": "linkedin-search",
                "login_url": self.searchers["linkedin"].login_url,
                "features": ["国际平台", "职业社交", "公司信息", "技能验证"]
            },
            {
                "name": "脉脉",
                "searcher": "MaimaiSearcher",
                "skill": "maimai-search",
                "login_url": self.searchers["maimai"].login_url,
                "features": ["职场社交", "匿名爆料", "公司点评", "人脉拓展"]
            }
        ]
        
        for platform in platforms_info:
            print(f"\n【{platform['name']}】")
            print(f"  Skill 名称: {platform['skill']}")
            print(f"  登录地址: {platform['login_url']}")
            print(f"  主要功能: {', '.join(platform['features'])}")
    
    def show_search_workflow(self):
        """展示搜索工作流程"""
        print("\n" + "="*80)
        print("完整自动化搜索工作流程")
        print("="*80)
        
        workflow = [
            {
                "step": 1,
                "title": "准备阶段",
                "actions": [
                    "检查并安装项目依赖: pip install -e .",
                    "加载对应平台的 Skill: skill_view('boss-search')",
                    "检查 Cookie 有效性: searcher.check_cookie_validity()",
                    "配置搜索参数（关键词、城市、薪资等）"
                ]
            },
            {
                "step": 2,
                "title": "登录阶段",
                "actions": [
                    "导航到登录页面: mcp_chrome_navigate(url=login_url)",
                    "识别登录方式（扫码/账号密码）",
                    "执行登录操作（用户扫码或输入账号）",
                    "等待登录成功: mcp_chrome_wait_for_navigation()",
                    "保存 Cookie: searcher.save_cookies(cookies)"
                ]
            },
            {
                "step": 3,
                "title": "搜索阶段",
                "actions": [
                    "导航到搜索页面",
                    "输入搜索条件: mcp_chrome_fill_or_select()",
                    "点击搜索按钮: mcp_chrome_click_element()",
                    "等待搜索结果加载",
                    "设置筛选条件（城市、薪资、经验等）"
                ]
            },
            {
                "step": 4,
                "title": "数据采集阶段",
                "actions": [
                    "解析列表页: mcp_chrome_read_page() -> searcher.parse_candidate_list()",
                    "点击候选人卡片进入详情页",
                    "解析详情页: searcher.parse_candidate_detail()",
                    "提取联系方式: mcp_chrome_javascript()",
                    "返回列表页: mcp_chrome_navigate(history='back')",
                    "翻页继续采集: mcp_chrome_click_element(selector='下一页')"
                ]
            },
            {
                "step": 5,
                "title": "数据处理阶段",
                "actions": [
                    "数据验证: data_validator.validate_candidate()",
                    "完整性评分: data_validator.completeness_score()",
                    "去重处理: data_validator.deduplicate_candidates()",
                    "跨平台合并: search_aggregator.aggregate_all()",
                    "数据导出: data_exporter.export_to_json() / export_to_csv()"
                ]
            },
            {
                "step": 6,
                "title": "后续处理",
                "actions": [
                    "数据预览和统计: data_preview.preview_file()",
                    "生成搜索报告",
                    "AI 候选人评分（需集成大模型）",
                    "批量导出和发送"
                ]
            }
        ]
        
        for stage in workflow:
            print(f"\n步骤 {stage['step']}: {stage['title']}")
            for action in stage['actions']:
                print(f"  → {action}")
    
    def show_mcp_tool_reference(self):
        """展示 MCP 工具快速参考"""
        print("\n" + "="*80)
        print("MCP Chrome 工具快速参考")
        print("="*80)
        
        tools = [
            {
                "name": "mcp_chrome_navigate",
                "usage": "导航到指定 URL",
                "example": "mcp_chrome_navigate(url='https://www.zhipin.com')"
            },
            {
                "name": "mcp_chrome_read_page",
                "usage": "读取页面内容，解析可交互元素",
                "example": "mcp_chrome_read_page(filter='interactive')"
            },
            {
                "name": "mcp_chrome_click_element",
                "usage": "点击页面元素",
                "example": "mcp_chrome_click_element(selector='.search-btn')"
            },
            {
                "name": "mcp_chrome_fill_or_select",
                "usage": "填充输入框或选择下拉框",
                "example": "mcp_chrome_fill_or_select(selector='#keyword', value='Python 开发')"
            },
            {
                "name": "mcp_chrome_javascript",
                "usage": "执行 JavaScript 代码",
                "example": "mcp_chrome_javascript(code='return document.title')"
            },
            {
                "name": "mcp_chrome_screenshot",
                "usage": "截取页面截图",
                "example": "mcp_chrome_screenshot(name='login_page')"
            },
            {
                "name": "mcp_chrome_handle_dialog",
                "usage": "处理弹窗对话框",
                "example": "mcp_chrome_handle_dialog(action='accept')"
            },
            {
                "name": "mcp_chrome_network_capture",
                "usage": "捕获网络请求",
                "example": "mcp_chrome_network_capture(action='start')"
            }
        ]
        
        for tool in tools:
            print(f"\n🔧 {tool['name']}")
            print(f"   用途: {tool['usage']}")
            print(f"   示例: {tool['example']}")
    
    def show_tips_and_best_practices(self):
        """展示使用技巧和最佳实践"""
        print("\n" + "="*80)
        print("使用技巧与最佳实践")
        print("="*80)
        
        tips = [
            {
                "category": "🔐 登录技巧",
                "tips": [
                    "优先使用扫码登录，避免账号密码被风控",
                    "登录后及时保存 Cookie，避免重复登录",
                    "Cookie 有效期通常为 7-30 天，定期检查有效性",
                    "多账号轮换使用，降低单账号风险"
                ]
            },
            {
                "category": "🤖 反爬策略",
                "tips": [
                    "每次操作间隔 2-5 秒，模拟人类行为",
                    "随机滚动页面，不要固定节奏",
                    "遇到验证码立即暂停，通知人工处理",
                    "不要在短时间内大量请求同一页面"
                ]
            },
            {
                "category": "📊 数据质量",
                "tips": [
                    "采集后立即进行数据验证和完整性检查",
                    "跨平台去重，避免重复候选人",
                    "联系方式打码处理，保护隐私",
                    "定期备份采集的数据"
                ]
            },
            {
                "category": "⚡ 效率提升",
                "tips": [
                    "先采集列表，再批量打开详情页",
                    "使用多标签页并行采集（注意风险）",
                    "设置合理的采集上限，避免过载",
                    "优先处理高质量候选人"
                ]
            },
            {
                "category": "🛠️ 故障排查",
                "tips": [
                    "页面元素找不到时，先截图检查",
                    "使用 mcp_chrome_read_page() 查看实际元素",
                    "检查网络连接和 Cookie 有效性",
                    "查看日志文件定位问题原因"
                ]
            }
        ]
        
        for category in tips:
            print(f"\n{category['category']}")
            for tip in category['tips']:
                print(f"  • {tip}")
    
    def run(self):
        """运行完整演示"""
        print("\n" + "#"*80)
        print("#      Hunter Auto Search - 多平台搜索完整指南")
        print("#"*80)
        
        self.show_platform_comparison()
        self.show_search_workflow()
        self.show_mcp_tool_reference()
        self.show_tips_and_best_practices()
        
        print("\n" + "#"*80)
        print("#      指南结束！")
        print("#"*80)
        print("\n📚 相关文档:")
        print("  - 快速开始: docs/QUICKSTART.md")
        print("  - MCP 流程: docs/MCP_WORKFLOW_GUIDE.md")
        print("  - BOSS 直聘 Skill: skills/boss-search/SKILL.md")
        print("\n🚀 开始使用:")
        print("  1. python examples/boss_search_demo.py")
        print("  2. python has_cli.py boss --help")
        print("  3. 在 Hermes Agent 中加载 Skill")


if __name__ == "__main__":
    demo = MultiPlatformSearchDemo()
    demo.run()
