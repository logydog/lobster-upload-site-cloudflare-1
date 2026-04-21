#!/bin/bash
# 🦞 更新前端 BACKEND_URL

if [ -z "$1" ]; then
    echo "使用方法: $0 <新的後端網址>"
    echo "範例: $0 https://lobster-upload-worker.example.workers.dev"
    exit 1
fi

NEW_URL="$1"
echo "🦞 更新前端 BACKEND_URL 為: $NEW_URL"

# 更新 index.html
if [ -f "index.html" ]; then
    sed -i "s|const BACKEND_URL = '.*'|const BACKEND_URL = '$NEW_URL'|g" index.html
    echo "✅ 更新 index.html"
fi

# 更新 simple_upload_cf.html
if [ -f "simple_upload_cf.html" ]; then
    sed -i "s|const BACKEND_URL = '.*'|const BACKEND_URL = '$NEW_URL'|g" simple_upload_cf.html
    echo "✅ 更新 simple_upload_cf.html"
fi

echo ""
echo "📋 更新完成，需要重新部署到 Cloudflare Pages："
echo "   1. 壓縮整個目錄"
echo "   2. 到 Cloudflare Dashboard → Workers & Pages → Pages"
echo "   3. 重新上傳檔案"
echo "   4. 等待部署完成"
echo ""
echo "🧪 測試指令："
echo "   curl \"$NEW_URL/\""
echo "   curl -X POST -F \"file=@test.txt\" \"$NEW_URL/upload\""