#!/bin/bash
# 龔蝦米網站啟動腳本

echo "🦞 啟動龔蝦米網站..."

# 檢查目錄
if [ ! -d "/tmp/lobster_website" ]; then
    echo "❌ 錯誤: /tmp/lobster_website 目錄不存在"
    exit 1
fi

cd /tmp/lobster_website

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 找不到 python3"
    exit 1
fi

# 檢查端口是否被佔用
check_port() {
    local port=$1
    if command -v netstat &> /dev/null; then
        netstat -tln | grep -q ":$port "
        return $?
    elif command -v ss &> /dev/null; then
        ss -tln | grep -q ":$port "
        return $?
    elif command -v lsof &> /dev/null; then
        lsof -i :$port &> /dev/null
        return $?
    else
        # 嘗試連接測試
        timeout 1 bash -c "echo > /dev/tcp/localhost/$port" 2>/dev/null
        return $?
    fi
}

# 嘗試不同端口
PORTS=(8888 8889 8890 8891 8892)
PORT=""

for p in "${PORTS[@]}"; do
    if ! check_port $p; then
        PORT=$p
        echo "✅ 找到可用端口: $p"
        break
    else
        echo "⚠️  端口 $p 已被佔用"
    fi
done

if [ -z "$PORT" ]; then
    echo "❌ 錯誤: 所有端口都被佔用"
    exit 1
fi

# 啟動伺服器
echo "🚀 啟動伺服器在端口 $PORT..."
python3 start_server.py --port $PORT &

SERVER_PID=$!
echo "📝 伺服器 PID: $SERVER_PID"

# 等待伺服器啟動
sleep 2

# 檢查伺服器是否運行
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ 伺服器啟動成功！"
    echo "🌐 網址: http://localhost:$PORT"
    echo "📄 首頁: http://localhost:$PORT/index.html"
    
    # 嘗試啟動 ngrok
    if command -v ngrok &> /dev/null; then
        echo "🚀 嘗試啟動 ngrok..."
        ngrok http $PORT > /tmp/lobster_website_ngrok.log 2>&1 &
        NGROK_PID=$!
        echo "📝 ngrok PID: $NGROK_PID"
        
        sleep 3
        
        # 嘗試取得公開網址
        if curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -q "public_url"; then
            PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | \
                python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])" 2>/dev/null)
            echo "🌍 公開網址: $PUBLIC_URL"
        else
            echo "⚠️  ngrok 啟動中，請稍後檢查 /tmp/lobster_website_ngrok.log"
        fi
    else
        echo "⚠️  找不到 ngrok，僅本地訪問"
    fi
    
    echo ""
    echo "📋 伺服器資訊:"
    echo "   目錄: /tmp/lobster_website"
    echo "   端口: $PORT"
    echo "   PID: $SERVER_PID"
    [ ! -z "$NGROK_PID" ] && echo "   ngrok PID: $NGROK_PID"
    [ ! -z "$PUBLIC_URL" ] && echo "   公開網址: $PUBLIC_URL"
    
    echo ""
    echo "🛑 停止伺服器: kill $SERVER_PID"
    [ ! -z "$NGROK_PID" ] && echo "🛑 停止 ngrok: kill $NGROK_PID"
    
else
    echo "❌ 伺服器啟動失敗"
    exit 1
fi