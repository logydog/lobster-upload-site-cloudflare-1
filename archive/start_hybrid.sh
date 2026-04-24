#!/bin/bash
# 🦞 龔蝦米混合架構網站啟動腳本

echo "🦞 啟動龔蝦米混合架構網站"
echo "================================"

# 檢查必要工具
echo "🔍 檢查必要工具..."
which python3 > /dev/null || { echo "❌ 需要 python3"; exit 1; }
which ngrok > /dev/null || { echo "❌ 需要 ngrok"; exit 1; }
which curl > /dev/null || { echo "❌ 需要 curl"; exit 1; }

# 1. 停止現有服務
echo "🛑 停止現有服務..."
pkill -f "upload_handler.py" 2>/dev/null
pkill ngrok 2>/dev/null
sleep 2

# 2. 啟動後端伺服器
echo "🚀 啟動後端伺服器 (port 8890)..."
cd "$(dirname "$0")"
python3 upload_handler.py > upload_server.log 2>&1 &
BACKEND_PID=$!
sleep 3

# 檢查後端是否啟動
if ! curl -s http://localhost:8890/ > /dev/null 2>&1; then
    echo "❌ 後端伺服器啟動失敗"
    exit 1
fi

# 3. 啟動 ngrok 隧道
echo "🌐 啟動 ngrok 隧道..."
ngrok http 8890 > ngrok.log 2>&1 &
NGROK_PID=$!
sleep 5

# 4. 取得公開網址
echo "⏳ 取得公開網址..."
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | \
  python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])" 2>/dev/null)

if [ -z "$PUBLIC_URL" ]; then
    echo "⚠️  無法取得 ngrok 網址，請檢查 ngrok.log"
    PUBLIC_URL="https://你的-ngrok-網址.ngrok-free.dev"
fi

# 5. 顯示結果
echo ""
echo "✅ 部署完成！"
echo "================================"
echo "📊 服務狀態："
echo "  🔹 後端伺服器: http://localhost:8890 (PID: $BACKEND_PID)"
echo "  🔹 公開網址: $PUBLIC_URL"
echo "  🔹 ngrok 面板: http://localhost:4040"
echo ""
echo "📁 日誌檔案："
echo "  🔸 後端日誌: upload_server.log"
echo "  🔸 ngrok 日誌: ngrok.log"
echo ""
echo "🚀 下一步："
echo "  1. 將前端部署到 Cloudflare Pages"
echo "  2. 更新前端 HTML 中的 BACKEND_URL："
echo "     const BACKEND_URL = '$PUBLIC_URL';"
echo "  3. 測試檔案上傳功能"
echo ""
echo "🧪 測試指令："
echo "  curl $PUBLIC_URL/"
echo "  curl -X POST -F \"file=@test.txt\" $PUBLIC_URL/upload"
echo ""
echo "🛑 停止指令："
echo "  pkill -f 'upload_handler.py' && pkill ngrok"
echo ""
echo "📋 詳細說明請參考 DEPLOY.md"
echo "================================"

# 儲存網址到檔案
echo "$PUBLIC_URL" > backend_url.txt
echo "後端網址已儲存到: backend_url.txt"

# 保持腳本運行（按 Ctrl+C 停止）
echo ""
echo "按 Ctrl+C 停止所有服務..."
echo ""
wait