#!/bin/bash
# 🦞 龔蝦米 Cloudflare Worker 部署腳本

echo "🦞 部署龔蝦米 Worker 網站"
echo "================================"

# 檢查必要工具
echo "🔍 檢查必要工具..."
which npm > /dev/null || { echo "❌ 需要 npm"; exit 1; }
which wrangler > /dev/null || { 
    echo "⚠️  wrangler 未安裝，嘗試安裝..."
    npm install -g wrangler 2>/dev/null || {
        echo "❌ 無法安裝 wrangler，請手動安裝：npm install -g wrangler"
        exit 1
    }
}

# 檢查登入狀態
echo "🔐 檢查 Cloudflare 登入狀態..."
wrangler whoami 2>/dev/null || {
    echo "⚠️  未登入 Cloudflare，請執行："
    echo "   wrangler login"
    echo "然後重新執行此腳本"
    exit 1
}

# 部署 Worker
echo "🚀 部署 Worker..."
cd "$(dirname "$0")"

# 建立 package.json 如果不存在
if [ ! -f package.json ]; then
    echo '{
  "name": "lobster-upload-worker",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "deploy": "wrangler deploy"
  }
}' > package.json
fi

# 部署
echo "📦 部署到 Cloudflare Workers..."
wrangler deploy

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 部署成功！"
    echo "================================"
    echo "🌐 Worker 網址："
    echo "  https://lobster-upload-worker.<你的子網域>.workers.dev"
    echo ""
    echo "📋 測試指令："
    echo "  curl https://lobster-upload-worker.<你的子網域>.workers.dev/"
    echo "  curl -X POST -F \"file=@test.txt\" https://lobster-upload-worker.<你的子網域>.workers.dev/upload"
    echo ""
    echo "🎯 架構優勢："
    echo "  ✅ 無 ngrok 警告頁"
    echo "  ✅ 固定網址"
    echo "  ✅ 全球 CDN"
    echo "  ✅ 可擴展到 R2 儲存"
    echo ""
    echo "🔧 後續設定："
    echo "  1. 設定自訂網域（選用）"
    echo "  2. 設定 R2 bucket 永久儲存"
    echo "  3. 設定環境變數"
else
    echo "❌ 部署失敗"
    exit 1
fi