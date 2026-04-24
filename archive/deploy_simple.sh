#!/bin/bash
# 🦞 簡化版 Cloudflare Worker 部署

echo "🦞 部署龔蝦米 Worker"
echo "================================"

# 檢查目錄
cd "$(dirname "$0")"

# 建立必要檔案
echo "📁 準備部署檔案..."

# 檢查 wrangler
if ! npx wrangler --version 2>/dev/null; then
    echo "⚠️  安裝 wrangler..."
    npm install wrangler --save-dev
fi

echo "🔐 請先登入 Cloudflare："
echo "   npx wrangler login"
echo ""
echo "📋 部署指令："
echo "   npx wrangler deploy"
echo ""
echo "🌐 部署完成後："
echo "   1. 取得 Worker 網址（格式：https://lobster-upload-worker.<子網域>.workers.dev）"
echo "   2. 更新前端 HTML 中的 BACKEND_URL"
echo "   3. 測試檔案上傳功能"
echo ""
echo "🎯 架構優勢："
echo "   ✅ 無 ngrok 警告頁"
echo "   ✅ 固定網址"
echo "   ✅ 全球 CDN"
echo "   ✅ 純 JavaScript，無需 Python 後端"
echo ""
echo "📁 檔案說明："
echo "   worker.js - Worker 程式碼"
echo "   wrangler.toml - 設定檔"
echo "   package.json - 依賴管理"
echo ""
echo "🚀 開始部署："