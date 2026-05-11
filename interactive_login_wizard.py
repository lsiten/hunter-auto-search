#!/usr/bin/env python3
"""
交互式账号配置与登录引导向导
通过问答方式引导用户完成账号配置和登录流程
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.log import logger
from conf import (
    COOKIES_DIR,
    CONFIG_DIR,
    PLATFORM_BOSS,
    PLATFORM_LIEPIN,
    PLATFORM_LINKEDIN,
    PLATFORM_MAIMAI,
    PLATFORMS
)


class InteractiveLoginWizard:
    """交互式登录引导向导"""
    
    def __init__(self):
        self.platform_configs = {
            PLATFORM_BOSS: {
                'name': 'BOSS 直聘',
                'login_url': 'https://www.zhipin.com/web/user/',
                'description': '互联网招聘首选，候选人活跃度高',
                'scan_qr': True,
                'account_type': '手机扫码登录'
            },
            PLATFORM_LIEPIN: {
                'name': '猎聘',
                'login_url': 'https://www.liepin.com/',
                'description': '中高端人才集中，猎头资源丰富',
                'scan_qr': True,
                'account_type': '手机扫码登录'
            },
            PLATFORM_LINKEDIN: {
                'name': '领英',
                'login_url': 'https://www.linkedin.com/',
                'description': '全球覆盖，高端人才首选',
                'scan_qr': False,
                'account_type': '账号密码/验证码登录'
            },
            PLATFORM_MAIMAI: {
                'name': '脉脉',
                'login_url': 'https://maimai.cn/',
                'description': '职场社交属性强，人脉拓展好用',
                'scan_qr': True,
                'account_type': '手机扫码登录'
            }
        }
        self.account_file = Path(CONFIG_DIR) / 'accounts.json'
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保必要目录存在"""
        Path(COOKIES_DIR).mkdir(parents=True, exist_ok=True)
        Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    
    def _print_header(self, title: str):
        """打印标题头"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")
    
    def _print_separator(self):
        """打印分隔线"""
        print("\n" + "-" * 60 + "\n")
    
    def _input_with_default(self, prompt: str, default: str = "") -> str:
        """带默认值的输入"""
        if default:
            result = input(f"{prompt} [默认: {default}]: ").strip()
            return result if result else default
        return input(f"{prompt}: ").strip()
    
    def _select_option(self, prompt: str, options: List[str], default: int = 0) -> int:
        """选择选项"""
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = input(f"\n请选择 (1-{len(options)}, 默认 {default+1}): ").strip()
                if not choice:
                    return default
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return idx
                print(f"请输入 1 到 {len(options)} 之间的数字")
            except ValueError:
                print("请输入有效的数字")
    
    def _confirm(self, prompt: str, default: bool = True) -> bool:
        """确认对话框"""
        default_str = "Y/n" if default else "y/N"
        while True:
            result = input(f"{prompt} [{default_str}]: ").strip().lower()
            if not result:
                return default
            if result in ['y', 'yes']:
                return True
            if result in ['n', 'no']:
                return False
            print("请输入 y 或 n")
    
    def load_accounts(self) -> Dict:
        """加载已保存的账号配置"""
        if self.account_file.exists():
            try:
                with open(self.account_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"加载账号配置失败: {e}")
        return {
            'accounts': {},
            'last_updated': None
        }
    
    def save_accounts(self, accounts: Dict):
        """保存账号配置"""
        accounts['last_updated'] = datetime.now().isoformat()
        with open(self.account_file, 'w', encoding='utf-8') as f:
            json.dump(accounts, f, indent=2, ensure_ascii=False)
        logger.info(f"账号配置已保存到: {self.account_file}")
    
    def show_platform_overview(self):
        """显示平台概览"""
        self._print_header("招聘平台概览")
        
        print(f"{'平台':<12} {'登录方式':<18} {'特点':<30}")
        print("-" * 60)
        
        for platform_key in PLATFORMS:
            config = self.platform_configs[platform_key]
            print(f"{config['name']:<12} {config['account_type']:<18} {config['description']:<30}")
        
        self._print_separator()
    
    def select_platform(self) -> Optional[str]:
        """选择平台"""
        self._print_header("步骤 1: 选择招聘平台")
        
        platforms_list = []
        for platform_key in PLATFORMS:
            config = self.platform_configs[platform_key]
            platforms_list.append(f"{config['name']} - {config['description']}")
        
        platforms_list.append("所有平台（依次配置）")
        
        choice = self._select_option("请选择要配置的平台:", platforms_list)
        
        if choice == len(PLATFORMS):
            return 'all'
        return PLATFORMS[choice]
    
    def configure_account(self, platform: str) -> Dict:
        """配置单个平台账号"""
        config = self.platform_configs[platform]
        platform_name = config['name']
        
        self._print_header(f"配置 {platform_name} 账号")
        
        print(f"\n平台: {platform_name}")
        print(f"登录方式: {config['account_type']}")
        print(f"登录地址: {config['login_url']}")
        self._print_separator()
        
        account_name = self._input_with_default(
            "请输入账号名称（用于标识不同账号）",
            default="main_account"
        )
        
        description = self._input_with_default(
            "请输入账号描述（可选，如：公司主账号、个人号等）",
            default=""
        )
        
        account = {
            'platform': platform,
            'account_name': account_name,
            'description': description,
            'login_url': config['login_url'],
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        print(f"\n✅ 账号信息已配置:")
        print(f"   平台: {platform_name}")
        print(f"   账号名称: {account_name}")
        if description:
            print(f"   描述: {description}")
        
        return account
    
    def guide_login_process(self, platform: str, account_name: str):
        """引导登录流程"""
        config = self.platform_configs[platform]
        platform_name = config['name']
        
        self._print_header(f"引导 {platform_name} 登录流程")
        
        print(f"\n📋 登录步骤说明:")
        print(f"\n1. 打开浏览器并访问: {config['login_url']}")
        
        if config['scan_qr']:
            print(f"\n2. 找到页面上的二维码")
            print(f"3. 使用手机 {platform_name} APP 扫码登录")
            print(f"4. 等待页面跳转，确认登录成功")
        else:
            print(f"\n2. 输入你的账号（邮箱/手机号）和密码")
            print(f"3. 完成验证码验证（如有）")
            print(f"4. 等待页面跳转，确认登录成功")
        
        print(f"\n5. 登录成功后，按回车键继续...")
        self._print_separator()
        
        input("按回车键继续...")
        
        # 检查登录状态
        print(f"\n🔍 正在检查登录状态...")
        
        # 创建示例 Cookie 文件
        cookie_path = Path(COOKIES_DIR) / f"{platform}_{account_name}.json"
        cookie_data = {
            'platform': platform,
            'account_name': account_name,
            'status': 'manual_login_required',
            'message': '请在浏览器中登录后，保存 Cookie',
            'login_url': config['login_url'],
            'created_at': datetime.now().isoformat()
        }
        
        with open(cookie_path, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Cookie 占位文件已创建:")
        print(f"   路径: {cookie_path}")
        print(f"\n💡 提示:")
        print(f"   1. 请确保在浏览器中已成功登录 {platform_name}")
        print(f"   2. 使用浏览器开发者工具获取实际的 Cookie")
        print(f"   3. 将 Cookie 数据更新到上述文件中")
        print(f"   4. 或使用 Hermes Agent 的 MCP 工具保存 Cookie")
    
    def configure_all_platforms(self):
        """配置所有平台"""
        accounts = self.load_accounts()
        
        for platform in PLATFORMS:
            if self._confirm(f"\n是否配置 {self.platform_configs[platform]['name']}?"):
                account = self.configure_account(platform)
                
                if 'accounts' not in accounts:
                    accounts['accounts'] = {}
                if platform not in accounts['accounts']:
                    accounts['accounts'][platform] = {}
                
                accounts['accounts'][platform][account['account_name']] = account
                
                if self._confirm("是否现在引导登录流程?"):
                    self.guide_login_process(platform, account['account_name'])
        
        self.save_accounts(accounts)
    
    def show_account_status(self):
        """显示账号状态"""
        self._print_header("当前账号状态")
        
        accounts = self.load_accounts()
        
        if not accounts.get('accounts'):
            print("❌ 还没有配置任何账号")
            return
        
        print(f"{'平台':<12} {'账号名称':<20} {'描述':<20} {'状态':<10}")
        print("-" * 62)
        
        for platform, platform_accounts in accounts['accounts'].items():
            for account_name, account_info in platform_accounts.items():
                # 检查 Cookie 文件
                cookie_path = Path(COOKIES_DIR) / f"{platform}_{account_name}.json"
                status = "✅ 已配置" if cookie_path.exists() else "⚠️  未登录"
                
                platform_name = self.platform_configs[platform]['name']
                description = account_info.get('description', '-')[:18]
                
                print(f"{platform_name:<12} {account_name:<20} {description:<20} {status:<10}")
        
        self._print_separator()
    
    def run_wizard(self):
        """运行完整向导"""
        print("\n" + "🚀" * 30)
        print("   Hunter Auto Search - 交互式账号配置与登录引导向导")
        print("🚀" * 30)
        
        # 显示平台概览
        self.show_platform_overview()
        
        # 显示当前账号状态
        self.show_account_status()
        
        # 选择平台
        platform = self.select_platform()
        
        if platform == 'all':
            # 配置所有平台
            self.configure_all_platforms()
        else:
            # 配置单个平台
            accounts = self.load_accounts()
            account = self.configure_account(platform)
            
            if 'accounts' not in accounts:
                accounts['accounts'] = {}
            if platform not in accounts['accounts']:
                accounts['accounts'][platform] = {}
            
            accounts['accounts'][platform][account['account_name']] = account
            
            if self._confirm("是否现在引导登录流程?"):
                self.guide_login_process(platform, account['account_name'])
            
            self.save_accounts(accounts)
        
        # 完成总结
        self._print_header("配置完成")
        
        print("\n✅ 账号配置已完成!")
        print("\n📋 下一步操作:")
        print("\n1. 使用 Hermes Agent 加载 Skill")
        print("   ```python")
        print("   skill_view('boss-search')  # 或其他平台")
        print("   ```")
        print("\n2. 使用 MCP 工具执行实际登录")
        print("   - mcp_chrome_navigate(url=登录地址)")
        print("   - 完成扫码/账号密码登录")
        print("   - mcp_chrome_screenshot() 验证")
        print("\n3. 执行搜索任务")
        print("   ```bash")
        print("   python has_cli.py boss search --keyword 'Python'")
        print("   ```")
        
        self._print_separator()
        print("\n🎉 欢迎使用 Hunter Auto Search!")


def main():
    """主函数"""
    try:
        wizard = InteractiveLoginWizard()
        wizard.run_wizard()
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        logger.error(f"向导运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
