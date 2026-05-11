#!/usr/bin/env python3
"""
Hunter Auto Search - 交互式启动向导
一键开始招聘平台自动化搜索
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.log import logger
from conf import PLATFORM_BOSS, PLATFORM_LIEPIN, PLATFORM_LINKEDIN, PLATFORM_MAIMAI


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗        ║
║   ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗       ║
║   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝       ║
║   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗       ║
║   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║       ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ║
║                                                              ║
║   █████╗ ██╗   ██╗████████╗ ██████╗                          ║
║  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗                         ║
║  ███████║██║   ██║   ██║   ██║   ██║                         ║
║  ██╔══██║██║   ██║   ██║   ██║   ██║                         ║
║  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝                         ║
║  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝                          ║
║                                                              ║
║   招聘平台人才搜索自动化工具 - Hermes Agent 集成版            ║
║   支持 BOSS直聘 | 猎聘 | 领英 | 脉脉                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def show_menu():
    """显示主菜单"""
    print("\n" + "="*60)
    print("  主菜单")
    print("="*60)
    print("\n  1. 🚀 快速开始 - BOSS 直聘搜索演示")
    print("  2. 🔍 查看已安装的 Hermes Skills")
    print("  3. 📋 查看 CLI 命令帮助")
    print("  4. 📊 运行核心功能测试")
    print("  5. 📖 打开快速开始文档")
    print("  6. 🌐 打开 GitHub 仓库")
    print("  7. 🔧 查看项目状态")
    print("  0. ❌ 退出")
    print("\n" + "="*60)


def quick_start_demo():
    """快速开始演示"""
    logger.info("🚀 开始 BOSS 直聘搜索演示...")
    print("\n" + "="*60)
    print("  BOSS 直聘搜索演示")
    print("="*60)
    
    try:
        from examples.boss_search_demo import run_full_demo
        success = run_full_demo()
        if success:
            logger.success("✅ 演示完成！数据已导出到 output/ 目录")
        else:
            logger.error("❌ 演示执行失败")
    except Exception as e:
        logger.error(f"演示执行出错: {e}")
        import traceback
        traceback.print_exc()


def show_skills():
    """查看已安装的 Skills"""
    print("\n" + "="*60)
    print("  已安装的 Hermes Skills")
    print("="*60)
    
    skills_dir = "/Users/leishicheng/.hermes/skills"
    if os.path.exists(skills_dir):
        skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        
        hunter_skills = [s for s in skills if s in ['boss-search', 'liepin-search', 'linkedin-search', 'maimai-search']]
        
        print(f"\n  📦 共找到 {len(hunter_skills)} 个 Hunter Auto Search Skills:")
        for skill in hunter_skills:
            print(f"    ✅ {skill}")
        
        print(f"\n  💡 在 Hermes Agent 中使用:")
        print(f"    skill_view('boss-search')")
        print(f"    skill_view('liepin-search')")
        print(f"    skill_view('linkedin-search')")
        print(f"    skill_view('maimai-search')")
    else:
        logger.warning("未找到 Hermes Skills 目录")


def show_cli_help():
    """查看 CLI 帮助"""
    print("\n" + "="*60)
    print("  CLI 命令帮助")
    print("="*60)
    
    import subprocess
    result = subprocess.run([sys.executable, 'has_cli.py', '--help'], capture_output=True, text=True)
    print(result.stdout)
    
    print("\n" + "="*60)
    print("  BOSS 直聘命令")
    print("="*60)
    result = subprocess.run([sys.executable, 'has_cli.py', 'boss', '--help'], capture_output=True, text=True)
    print(result.stdout)


def run_tests():
    """运行核心功能测试"""
    logger.info("🧪 运行核心功能测试...")
    print("\n" + "="*60)
    print("  核心功能测试")
    print("="*60)
    
    import subprocess
    result = subprocess.run([sys.executable, 'test_core.py'], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)


def open_document():
    """打开快速开始文档"""
    doc_path = "/Users/leishicheng/Documents/workspace/code/hunter-auto-search/docs/QUICKSTART.md"
    if os.path.exists(doc_path):
        print(f"\n  📖 快速开始文档: {doc_path}")
        print("\n" + "="*60)
        with open(doc_path, 'r') as f:
            content = f.read()
            print(content[:2000] + "\n...\n" + "="*60)
    else:
        logger.warning("文档不存在")


def open_github():
    """打开 GitHub 仓库"""
    print("\n  🌐 GitHub 仓库: https://github.com/lsiten/hunter-auto-search")
    print("\n  在浏览器中打开以上链接查看项目")


def show_project_status():
    """查看项目状态"""
    print("\n" + "="*60)
    print("  项目状态")
    print("="*60)
    
    # 统计文件数量
    py_files = []
    md_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.py'):
                py_files.append(os.path.join(root, f))
            elif f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    
    # 统计代码行数
    total_lines = 0
    for f in py_files:
        try:
            with open(f, 'r') as fp:
                total_lines += len(fp.readlines())
        except:
            pass
    
    print(f"\n  📊 项目统计:")
    print(f"    Python 文件: {len(py_files)} 个")
    print(f"    Markdown 文档: {len(md_files)} 个")
    print(f"    总代码行数: {total_lines:,} 行")
    
    # 检查输出目录
    output_dir = "/Users/leishicheng/Documents/workspace/code/hunter-auto-search/output"
    if os.path.exists(output_dir):
        output_files = os.listdir(output_dir)
        print(f"\n  📁 输出文件 ({len(output_files)} 个):")
        for f in sorted(output_files)[:5]:
            size = os.path.getsize(os.path.join(output_dir, f))
            print(f"    - {f} ({size:,} bytes)")
    
    # 检查 Skills
    skills_dir = "/Users/leishicheng/.hermes/skills"
    hunter_skills = []
    if os.path.exists(skills_dir):
        for s in ['boss-search', 'liepin-search', 'linkedin-search', 'maimai-search']:
            if os.path.exists(os.path.join(skills_dir, s)):
                hunter_skills.append(s)
    
    print(f"\n  🎯 Hermes Skills: {len(hunter_skills)}/4 已安装")
    for s in hunter_skills:
        print(f"    ✅ {s}")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    print_banner()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n  请选择操作 (0-7): ").strip()
            
            if choice == '0':
                logger.info("👋 感谢使用 Hunter Auto Search！再见！")
                break
            elif choice == '1':
                quick_start_demo()
            elif choice == '2':
                show_skills()
            elif choice == '3':
                show_cli_help()
            elif choice == '4':
                run_tests()
            elif choice == '5':
                open_document()
            elif choice == '6':
                open_github()
            elif choice == '7':
                show_project_status()
            else:
                logger.warning("无效的选择，请输入 0-7")
            
            input("\n  按 Enter 继续...")
            
        except KeyboardInterrupt:
            logger.info("\n\n👋 感谢使用 Hunter Auto Search！再见！")
            break
        except Exception as e:
            logger.error(f"操作出错: {e}")


if __name__ == '__main__':
    main()
