#!/bin/bash
# 领英搜索快捷命令
# 使用方法: bash skills/linkedin-search/scripts/commands.sh <command> [options]

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
    echo -e "${BLUE}领英搜索工具 - 快捷命令${NC}"
    echo ""
    echo "用法: $0 <command> [options]"
    echo ""
    echo "可用命令:"
    echo "  login [account]           登录领英账号"
    echo "  check [account]           检查 Cookie 状态"
    echo "  search <keyword> [options] 搜索候选人"
    echo "  fetch <candidate_id>      获取候选人详情"
    echo "  help                      显示此帮助信息"
    echo ""
    echo "搜索选项:"
    echo "  --location <name>         地区筛选 (如: 北京, Shanghai)"
    echo "  --company <name>          当前公司筛选"
    echo "  --school <name>           学校筛选"
    echo "  --industry <name>         行业筛选"
    echo "  --network <degree>        人脉连接度 (1st, 2nd, 3rd)"
    echo "  --pages <num>             采集页数 (默认: 1)"
    echo "  --account <name>          指定账号 (默认: default)"
    echo "  --output <path>           输出文件路径"
    echo ""
    echo "示例:"
    echo "  $0 login"
    echo "  $0 login my_account"
    echo "  $0 check"
    echo "  $0 search \"Software Engineer\" --location Beijing --pages 3"
    echo "  $0 search \"数据科学家\" --company \"阿里巴巴\" --school \"清华大学\""
    echo "  $0 fetch john-smith-123456"
}

cmd_login() {
    ACCOUNT="${1:-default}"
    echo -e "${GREEN}启动领英登录流程...${NC}"
    echo -e "账号: ${YELLOW}$ACCOUNT${NC}"
    echo ""
    echo "请在 Hermes Agent 中执行以下步骤:"
    echo "  1. 打开登录页: mcp_chrome_navigate(url='https://www.linkedin.com/login')"
    echo "  2. 输入账号密码并登录"
    echo "  3. 登录成功后保存 Cookie"
    echo ""
    python has_cli.py linkedin login --account "$ACCOUNT"
}

cmd_check() {
    ACCOUNT="${1:-default}"
    echo -e "${GREEN}检查领英 Cookie 状态...${NC}"
    echo -e "账号: ${YELLOW}$ACCOUNT${NC}"
    echo ""
    python has_cli.py linkedin check --account "$ACCOUNT"
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

    echo -e "${GREEN}开始搜索领英候选人...${NC}"
    echo -e "关键词: ${YELLOW}$KEYWORD${NC}"
    echo ""

    python has_cli.py linkedin search --keyword "$KEYWORD" "$@"
}

cmd_fetch() {
    CANDIDATE_ID="$1"
    shift

    if [ -z "$CANDIDATE_ID" ]; then
        echo -e "${RED}错误: 请指定候选人 ID${NC}"
        echo ""
        print_help
        exit 1
    fi

    echo -e "${GREEN}获取领英候选人详情...${NC}"
    echo -e "候选人 ID: ${YELLOW}$CANDIDATE_ID${NC}"
    echo ""

    python has_cli.py linkedin fetch --id "$CANDIDATE_ID" "$@"
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
    fetch)
        shift
        cmd_fetch "$@"
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
