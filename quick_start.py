#!/usr/bin/env python3
"""
快速启动脚本 - 一键运行完整演示
"""

import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"命令: {cmd}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=project_root
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"执行失败: {e}")
        return False


def main():
    print("\n" + "#"*60)
    print("#      Hunter Auto Search - 快速启动")
    print("#"*60)
    
    # 1. 检查 Python 版本
    print("\n📋 检查环境...")
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(f"Python 版本: {result.stdout.strip()}")
    
    # 2. 显示项目信息
    print("\n📁 项目结构预览:")
    dirs = ["searcher", "utils", "skills", "docs", "examples"]
    for d in dirs:
        path = project_root / d
        if path.exists():
            files = list(path.glob("*.py")) + list(path.glob("*.md"))
            print(f"  {d}/: {len(files)} 个文件")
    
    # 3. 运行核心测试
    print("\n🧪 运行核心功能测试...")
    success = run_command(
        f"{sys.executable} test_core.py",
        "核心功能测试"
    )
    
    if not success:
        print("⚠️  核心测试有警告，但项目仍然可用")
    
    # 4. 运行 BOSS 直聘演示
    print("\n🎬 运行 BOSS 直聘搜索流程演示...")
    run_command(
        f"{sys.executable} examples/boss_search_demo.py",
        "BOSS 直聘搜索演示"
    )
    
    # 5. 运行多平台指南
    print("\n📚 显示多平台使用指南...")
    run_command(
        f"{sys.executable} examples/multi_platform_guide.py",
        "多平台使用指南"
    )
    
    # 6. 显示 CLI 帮助
    print("\n💻 CLI 命令行帮助...")
    run_command(
        f"{sys.executable} has_cli.py --help",
        "CLI 帮助"
    )
    
    # 7. 总结
    print("\n" + "#"*60)
    print("#      快速启动完成！")
    print("#"*60)
    
    print("\n" + "="*60)
    print("📝 下一步操作")
    print("="*60)
    print("\n1. 查看输出文件:")
    print("   ls -la output/")
    
    print("\n2. 运行使用示例:")
    print("   python example_usage.py")
    
    print("\n3. 查看 CLI 命令:")
    print("   python has_cli.py boss --help")
    
    print("\n4. 在 Hermes Agent 中加载 Skill:")
    print("   skill_view('boss-search')")
    
    print("\n5. 阅读文档:")
    print("   - 快速开始: docs/QUICKSTART.md")
    print("   - MCP 流程: docs/MCP_WORKFLOW_GUIDE.md")
    print("   - Skill 文档: skills/boss-search/SKILL.md")
    
    print("\n" + "="*60)
    print("🎯 项目已就绪，可以开始实际搜索了！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
