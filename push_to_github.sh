#!/bin/bash
# Hunter Auto Search - 快速推送到 GitHub 脚本

echo "🚀 Hunter Auto Search - GitHub 推送脚本"
echo ""

# 检查 git 状态
echo "📊 Git 状态:"
git status

echo ""
echo "📦 当前提交:"
git log --oneline -1

echo ""
echo "🔄 正在推送到 GitHub..."
echo "仓库地址: https://github.com/lsiten/hunter-auto-search"
echo ""

# 推送代码
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo "🌐 访问仓库: https://github.com/lsiten/hunter-auto-search"
else
    echo ""
    echo "❌ 推送失败，请检查网络连接或代理设置"
    echo ""
    echo "💡 提示：如果需要使用代理，可以设置环境变量："
    echo "   export https_proxy=http://127.0.0.1:7890"
    echo "   export http_proxy=http://127.0.0.1:7890"
    echo "   然后重新运行此脚本"
fi
