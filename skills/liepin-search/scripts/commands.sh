#!/bin/bash
# 猎聘搜索快捷命令
# 使用方法: bash skills/liepin-search/scripts/commands.sh <command> [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_help() {
    echo -e "${BLUE}猎聘搜索工具 - 快捷命令${NC}"
    echo ""
    echo "用法: $0 <command> [options]"
    echo ""
    echo "可用命令:"
    echo "  login [account]           登录猎聘账号（扫码）"
    echo "  check [account]           检查 Cookie 状态"
    echo "  search <keyword> [options] 搜索候选人"
    echo "  help                      显示此帮助信息"
    echo ""
    echo "搜索选项:"
    echo "  --city <name>             城市筛选 (如: 北京, 上海)"
    echo "  --salary <range>          薪资范围 (如: 20-30k)"
    echo "  --experience <years>      工作经验 (如: 3-5年)"
    echo "  --pages <num>             采集页数 (默认: 1)"
    echo "  --account <name>          指定账号 (默认: default)"
    echo "  --output <path>           输出文件路径"
    echo ""
    echo "示例:"
    echo "  $0 login"
    echo "  $0 login myaccount"
    echo "  $0 check"
    echo "  $0 search \"Python 开发\" --city 北京 --pages 3"
    echo "  $0 search \"Java 架构师\" --salary 50-80k --account myaccount"
}

cmd_login() {
    ACCOUNT="${1:-default}"
    echo -e "${GREEN}启动猎聘登录流程...${NC}"
    echo -e "账号: ${YELLOW}$ACCOUNT${NC}"
    echo ""
    python has_cli.py liepin login --account "$ACCOUNT"
}

cmd_check() {
    ACCOUNT="${1:-default}"
    echo -e "${GREEN}检查猎聘 Cookie 状态...${NC}"
    echo -e "账号: ${YELLOW}$ACCOUNT${NC}"
    echo ""
    python has_cli.py liepin check --account "$ACCOUNT"
}

cmd_search() {
    KEYWORD="$1"
    shift

    if [ -z "$KEYWORD" ]; then
        echo -e "${RED}错误: 请指定搜索关键词${NC}"
        echo ""
        print_help
        exit 1
    fi

    echo -e "${GREEN}开始搜索猎聘候选人...${NC}"
    echo -e "关键词: ${YELLOW}$KEYWORD${NC}"
    echo ""

    python has_cli.py liepin search --keyword "$KEYWORD" "$@"
}

# 主命令分发
case "${1:-help}" in
    login)
        shift
        cmd_login "$@"
        ;;
    check)
        shift
        cmd_check "$@"
        ;;
    search)
        shift
        cmd_search "$@"
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac
