#!/usr/bin/env python3
"""
Hunter Auto Search - 一键快速启动脚本
无需配置，直接开始使用
"""

import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))


def print_header():
    """打印标题"""
    print("\n" + "=" * 70)
    print("  🚀 Hunter Auto Search - 招聘平台自动化搜索工具")
    print("=" * 70 + "\n")


def print_menu():
    """打印主菜单"""
    print("📋 请选择操作:\n")
    print("  1. 交互式账号配置向导 (推荐新手)")
    print("  2. 查看当前账号状态")
    print("  3. BOSS 直聘 - 快速开始")
    print("  4. 猎聘 - 快速开始")
    print("  5. 领英 - 快速开始")
    print("  6. 脉脉 - 快速开始")
    print("  7. 查看项目文档")
    print("  8. 运行核心功能测试")
    print("  0. 退出")
    print("\n" + "-" * 70 + "\n")


def quick_start_boss():
    """BOSS 直聘快速开始"""
    print("\n" + "🎯" * 20)
    print("   BOSS 直聘 - 快速开始指南")
    print("🎯" * 20 + "\n")
    
    print("📝 步骤说明:\n")
    
    print("1️⃣  在 Hermes Agent 中加载 Skill")
    print("    ```python")
    print("    skill_view('boss-search')")
    print("    ```\n")
    
    print("2️⃣  打开登录页面")
    print("    ```python")
    print("    mcp_chrome_navigate(url='https://www.zhipin.com/web/user/')")
    print("    ```\n")
    
    print("3️⃣  扫码登录")
    print("    - 找到页面上的二维码")
    print("    - 使用手机 BOSS 直聘 APP 扫码")
    print("    - 确认登录成功\n")
    
    print("4️⃣  保存登录状态")
    print("    ```bash")
    print("    cd /Users/leishicheng/Documents/workspace/code/hunter-auto-search")
    print("    python interactive_login_wizard.py")
    print("    ```\n")
    
    print("5️⃣  执行搜索")
    print("    ```python")
    print("    # 在 Hermes Agent 中按照 Skill 文档指引执行搜索")
    print("    ```\n")
    
    input("按回车键返回主菜单...")


def quick_start_liepin():
    """猎聘快速开始"""
    print("\n" + "🎯" * 20)
    print("   猎聘 - 快速开始指南")
    print("🎯" * 20 + "\n")
    
    print("📝 步骤说明:\n")
    
    print("1️⃣  在 Hermes Agent 中加载 Skill")
    print("    ```python")
    print("    skill_view('liepin-search')")
    print("    ```\n")
    
    print("2️⃣  打开登录页面")
    print("    ```python")
    print("    mcp_chrome_navigate(url='https://www.liepin.com/')")
    print("    ```\n")
    
    print("3️⃣  扫码登录")
    print("    - 找到页面上的二维码")
    print("    - 使用手机猎聘 APP 扫码")
    print("    - 确认登录成功\n")
    
    print("4️⃣  保存登录状态")
    print("    ```bash")
    print("    python interactive_login_wizard.py")
    print("    ```\n")
    
    print("5️⃣  执行搜索")
    print("    按照 Skill 文档指引执行搜索操作\n")
    
    input("按回车键返回主菜单...")


def quick_start_linkedin():
    """领英快速开始"""
    print("\n" + "🎯" * 20)
    print("   领英 - 快速开始指南")
    print("🎯" * 20 + "\n")
    
    print("📝 步骤说明:\n")
    
    print("1️⃣  在 Hermes Agent 中加载 Skill")
    print("    ```python")
    print("    skill_view('linkedin-search')")
    print("    ```\n")
    
    print("2️⃣  打开登录页面")
    print("    ```python")
    print("    mcp_chrome_navigate(url='https://www.linkedin.com/')")
    print("    ```\n")
    
    print("3️⃣  账号密码登录")
    print("    - 输入你的邮箱/手机号和密码")
    print("    - 完成验证码验证")
    print("    - 确认登录成功\n")
    
    print("4️⃣  保存登录状态")
    print("    ```bash")
    print("    python interactive_login_wizard.py")
    print("    ```\n")
    
    print("5️⃣  执行搜索")
    print("    按照 Skill 文档指引执行搜索操作\n")
    
    input("按回车键返回主菜单...")


def quick_start_maimai():
    """脉脉快速开始"""
    print("\n" + "🎯" * 20)
    print("   脉脉 - 快速开始指南")
    print("🎯" * 20 + "\n")
    
    print("📝 步骤说明:\n")
    
    print("1️⃣  在 Hermes Agent 中加载 Skill")
    print("    ```python")
    print("    skill_view('maimai-search')")
    print("    ```\n")
    
    print("2️⃣  打开登录页面")
    print("    ```python")
    print("    mcp_chrome_navigate(url='https://maimai.cn/')")
    print("    ```\n")
    
    print("3️⃣  扫码登录")
    print("    - 找到页面上的二维码")
    print("    - 使用手机脉脉 APP 扫码")
    print("    - 确认登录成功\n")
    
    print("4️⃣  保存登录状态")
    print("    ```bash")
    print("    python interactive_login_wizard.py")
    print("    ```\n")
    
    print("5️⃣  执行搜索")
    print("    按照 Skill 文档指引执行搜索操作\n")
    
    input("按回车键返回主菜单...")


def view_documentation():
    """查看项目文档"""
    docs_dir = Path(__file__).parent / 'docs'
    
    print("\n📚 可用文档:\n")
    
    docs = list(docs_dir.glob('*.md'))
    for i, doc in enumerate(docs, 1):
        print(f"  {i}. {doc.name}")
    
    print("\n" + "-" * 70)
    print(f"\n📂 文档目录: {docs_dir}")
    print("\n💡 提示: 使用文本编辑器打开上述文档查看详细内容\n")
    
    # 显示 README
    readme_path = Path(__file__).parent / 'README.md'
    if readme_path.exists():
        print("\n" + "=" * 50)
        print("  📖 README.md (摘要)")
        print("=" * 50 + "\n")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 显示前 500 字符
            print(content[:800] + "\n...\n")
            print("(完整内容请查看文件)")
    
    input("\n按回车键返回主菜单...")


def run_tests():
    """运行核心功能测试"""
    print("\n🧪 运行核心功能测试...\n")
    
    test_script = Path(__file__).parent / 'test_core.py'
    if test_script.exists():
        os.system(f"python {test_script}")
    else:
        print("❌ 测试脚本不存在，跳过测试")
    
    input("\n按回车键返回主菜单...")


def run_interactive_wizard():
    """运行交互式配置向导"""
    wizard_script = Path(__file__).parent / 'interactive_login_wizard.py'
    if wizard_script.exists():
        os.system(f"python {wizard_script}")
    else:
        print("❌ 向导脚本不存在")
        input("按回车键返回主菜单...")


def show_account_status():
    """显示账号状态"""
    wizard_script = Path(__file__).parent / 'interactive_login_wizard.py'
    if wizard_script.exists():
        # 简单显示账号状态
        from utils.log import logger
        from conf import COOKIES_DIR, CONFIG_DIR, PLATFORMS
        
        print("\n" + "=" * 70)
        print("  📊 当前账号状态")
        print("=" * 70 + "\n")
        
        cookies_path = Path(COOKIES_DIR)
        if cookies_path.exists():
            cookie_files = list(cookies_path.glob('*.json'))
            
            if cookie_files:
                print(f"已配置的账号 ({len(cookie_files)} 个):\n")
                for cf in cookie_files:
                    print(f"  ✅ {cf.name}")
            else:
                print("❌ 还没有配置任何账号")
                print("\n💡 建议: 选择 [1] 运行交互式配置向导")
        else:
            print("❌ Cookie 目录不存在")
        
        print("\n" + "-" * 70 + "\n")
        input("按回车键返回主菜单...")


def main():
    """主函数"""
    while True:
        print_header()
        print_menu()
        
        try:
            choice = input("请输入选项 (0-8): ").strip()
            
            if choice == '0':
                print("\n👋 感谢使用 Hunter Auto Search!")
                print("\n📝 提示:")
                print("   - 在 Hermes Agent 中使用 skill_view() 加载平台 Skill")
                print("   - 有问题请查看 docs/ 目录下的文档")
                print("   - 项目地址: https://github.com/lsiten/hunter-auto-search")
                print("\n🎉 祝你使用愉快!\n")
                break
            
            elif choice == '1':
                run_interactive_wizard()
            
            elif choice == '2':
                show_account_status()
            
            elif choice == '3':
                quick_start_boss()
            
            elif choice == '4':
                quick_start_liepin()
            
            elif choice == '5':
                quick_start_linkedin()
            
            elif choice == '6':
                quick_start_maimai()
            
            elif choice == '7':
                view_documentation()
            
            elif choice == '8':
                run_tests()
            
            else:
                print("\n❌ 无效选项，请重新选择")
                input("按回车键继续...")
        
        except KeyboardInterrupt:
            print("\n\n👋 退出程序")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            input("按回车键继续...")


if __name__ == '__main__':
    main()
