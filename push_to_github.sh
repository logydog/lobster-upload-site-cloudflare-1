#!/bin/bash
# 🦞 推送到 GitHub 腳本

echo "🦞 推送到 GitHub..."
echo "================================"

# 檢查是否在正確目錄
if [ ! -d .git ]; then
    echo "❌ 不是 Git repository"
    exit 1
fi

# 設定遠端 repository
REPO_URL="https://github.com/logydog/lobster-upload-site-cloudflare-1.git"

echo "🔗 設定遠端 repository..."
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"

echo "📤 推送到 GitHub..."
echo ""
echo "⚠️  需要 GitHub 認證"
echo "================================"
echo "方法 1：使用 GitHub token"
echo "  1. 前往 GitHub → Settings → Developer settings"
echo "  2. Personal access tokens → Generate new token"
echo "  3. 複製 token"
echo "  4. 執行："
echo "     git remote set-url origin https://TOKEN@github.com/logydog/lobster-upload-site-cloudflare-1.git"
echo "     git push -u origin main"
echo ""
echo "方法 2：使用 SSH"
echo "  1. 建立 SSH key：ssh-keygen -t ed25519 -C \"your-email@example.com\""
echo "  2. 新增到 GitHub：Settings → SSH and GPG keys"
echo "  3. 執行："
echo "     git remote set-url origin git@github.com:logydog/lobster-upload-site-cloudflare-1.git"
echo "     git push -u origin main"
echo ""
echo "方法 3：使用 GitHub CLI"
echo "  1. 安裝：sudo apt install gh"
echo "  2. 登入：gh auth login"
echo "  3. 執行：git push -u origin main"
echo "================================"

# 檢查當前狀態
echo ""
echo "📊 當前 Git 狀態："
git status

echo ""
echo "✅ 準備完成！選擇上述方法之一推送。"