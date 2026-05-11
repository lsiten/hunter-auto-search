#!/bin/bash
# 脉脉搜索快捷命令
# 使用方法: bash skills/maimai-search/scripts/commands.sh <command> [options]

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
    echo -e "${BLUE}脉脉搜索工具 - 快捷命令${NC}"
    echo ""
    echo "用法: $0 <command> [options]"
    echo ""
    echo "可用命令:"
    echo "  login [account]           登录脉脉账号 (建议使用有头模式)"
    echo "  check [account]           检查 Cookie 状态"
    echo "  search <keyword> [options] 搜索候选人"
    echo "  fetch <candidate_id>      获取候选人详情"
    echo "  help                      显示此帮助信息"
    echo ""
    echo "搜索选项:"
    echo "  --city <name>             城市筛选 (如: 北京, 上海)"
    echo "  --company <name>          公司筛选"
    echo "  --position <name>         职位筛选"
    echo "  --industry <name>         行业筛选"
    echo "  --school <name>           学校筛选"
    echo "  --degree <level>          人脉度数 (1st, 2nd, 3rd)"
    echo "  --pages <num>             采集页数 (默认: 1)"
    echo "  --account <name>          指定账号 (默认: default)"
    echo "  --output <path>           输出文件路径"
    echo ""
    echo "示例:"
    echo "  $0 login"
    echo "  $0 login my_vip_account"
    echo "  $0 check"
    echo "  $0 search \"产品经理\" --city 北京 --pages 3"
    echo "  $0 search \"算法工程师\" --company \"阿里巴巴\" --school \"清华大学\""
    echo "  $0 fetch 12345678"
    echo ""
    echo -e "${YELLOW}注意事项:${NC}"
    echo "  1. 脉脉风控严格，建议操作间隔 10 秒以上"
    echo "  2. 登录时可能需要滑块验证，请人工处理"
    echo "  3. 免费账号每日搜索次数有限 (~50 次)"
    echo "  4. VIP 账号解锁更多功能和搜索次数"
    echo "  5. 联系方式查看通常需要 VIP 或添加好友"
    echo "  6. 建议只在白天工作时间段操作"
}

cmd_login() {
    ACCOUNT="${1:-default}"
    echo -e "${GREEN}启动脉脉登录流程...${NC}"
    echo -e "账号: ${YELLOW}$ACCOUNT${NC}"
    echo ""
    echo -e "${YELLOW}注意: 脉脉登录可能需要处理滑块验证码${NC}"
    echo "请在 Hermes Agent 中执行以下步骤:"
    echo "  1. mcp_chrome_navigate(url='https://maimai.cn/login')"
    echo "  2. 选择二维码登录或手机号验证码登录"
    echo "  3. 如遇滑块验证，请人工完成"
    echo "  4. 登录成功后保存 Cookie"
    echo ""
    python has_cli.py maimai login --account "$ACCOUNT" --headed
}

cmd_check() {
    ACCOUNT="${1:-default}"
    echo -e "${GREEN}检查脉脉 Cookie 状态...${NC}"
    echo -e "账号: ${YELLOW}$ACCOUNT${NC}"
    echo ""
    python has_cli.py maimai check --account "$ACCOUNT"
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

    echo -e "${GREEN}开始搜索脉脉候选人...${NC}"
    echo -e "关键词: ${YELLOW}$KEYWORD${NC}"
    echo ""
    echo -e "${YELLOW}注意: 脉脉风控严格，请控制采集频率${NC}"
    echo -e "推荐: 每采集 20 条数据暂停 5-10 分钟${NC}"
    echo ""

    python has_cli.py maimai search --keyword "$KEYWORD" "$@"
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

    echo -e "${GREEN}获取脉脉候选人详情...${NC}"
    echo -e "候选人 ID: ${YELLOW}$CANDIDATE_ID${NC}"
    echo ""
    echo -e "${YELLOW}注意: 查看详情会消耗每日额度${NC}"
    echo ""

    python has_cli.py maimai fetch --id "$CANDIDATE_ID" "$@"
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
