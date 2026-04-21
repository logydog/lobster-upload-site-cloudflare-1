# 🦞 龔蝦米混合架構網站部署指南

## 🏗️ 架構概述
- **前端**: Cloudflare Pages (靜態網站)
- **後端**: ngrok + Python HTTP Server (動態 API)
- **通訊**: JavaScript Fetch API + CORS

## 📁 檔案結構
```
/tmp/lobster_website_cloudflare/
├── index.html                    # 混合架構首頁
├── simple_upload_cf.html         # Cloudflare 前端上傳頁面
├── simple_upload.html           # 傳統上傳頁面 (備用)
├── upload_handler.py            # 後端上傳處理器
├── theme_one_man_army.html      # 主題頁面
├── theme_reverse_simple.html    # 主題頁面
├── about.html                   # 關於頁面
├── uploads/                     # 上傳檔案目錄
└── DEPLOY.md                    # 本文件
```

## 🚀 部署步驟

### 1. 後端部署 (ngrok)
```bash
# 啟動後端伺服器
cd /tmp/lobster_website_cloudflare
python3 upload_handler.py > upload_server.log 2>&1 &

# 用 ngrok 公開後端
ngrok http 8890 > ngrok.log 2>&1 &

# 取得公開網址
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])"
```

### 2. 前端部署 (Cloudflare Pages)

#### 方法 A: 網頁介面上傳
1. 登入 Cloudflare Dashboard
2. 進入 "Workers & Pages"
3. 點擊 "Create application" → "Pages"
4. 選擇 "Direct Upload"
5. 上傳整個 `/tmp/lobster_website_cloudflare` 目錄
6. 設定專案名稱 (如 `lobster-site`)
7. 部署完成後取得網址: `https://lobster-site.pages.dev`

#### 方法 B: 使用 wrangler CLI (需要 Node.js v20+)
```bash
# 安裝 wrangler
npm install -g wrangler

# 登入 Cloudflare
wrangler login

# 部署到 Cloudflare Pages
wrangler pages deploy /tmp/lobster_website_cloudflare --project-name lobster-site
```

### 3. 設定 CORS (後端)
後端 `upload_handler.py` 已支援 CORS，在 `do_POST` 方法中加入：
```python
self.send_header('Access-Control-Allow-Origin', '*')
self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
self.send_header('Access-Control-Allow-Headers', 'Content-Type')
```

## 🔧 設定調整

### 更新後端網址
在 Cloudflare 前端的 HTML 檔案中，更新 `BACKEND_URL`：
```javascript
const BACKEND_URL = 'https://你的-ngrok-網址.ngrok-free.dev';
```

檔案需要更新：
- `index.html` (第 245 行)
- `simple_upload_cf.html` (第 128 行)

### 測試連線
```bash
# 測試後端 API
curl -X POST -F "file=@test.txt" https://你的-ngrok-網址.ngrok-free.dev/upload

# 測試前端連線
curl https://lobster-site.pages.dev/
```

## ⚠️ 注意事項

### CORS 限制
- 前端 (Cloudflare) 和後端 (ngrok) 不同網域
- 需要後端設定 `Access-Control-Allow-Origin: *`
- 瀏覽器會發送預檢請求 (OPTIONS)

### ngrok 限制
- 免費版網址會變動
- 有頻寬和連線限制
- 需要定期重啟

### Cloudflare Pages 限制
- 只能託管靜態檔案
- 無法執行伺服器端程式
- 檔案上傳需要透過 API

## 🔄 自動化腳本

### 啟動腳本 (`start_hybrid.sh`)
```bash
#!/bin/bash
# 啟動混合架構

echo "🦞 啟動龔蝦米混合架構網站"

# 1. 啟動後端
echo "🚀 啟動後端伺服器..."
cd /tmp/lobster_website_cloudflare
python3 upload_handler.py > upload_server.log 2>&1 &
BACKEND_PID=$!

# 2. 啟動 ngrok
echo "🌐 啟動 ngrok 隧道..."
ngrok http 8890 > ngrok.log 2>&1 &
NGROK_PID=$!

# 3. 取得公開網址
echo "⏳ 等待 ngrok 啟動..."
sleep 5
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | \
  python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])" 2>/dev/null)

echo "✅ 後端已啟動: http://localhost:8890"
echo "✅ 公開網址: $PUBLIC_URL"
echo ""
echo "📋 下一步："
echo "1. 將前端部署到 Cloudflare Pages"
echo "2. 更新前端 HTML 中的 BACKEND_URL"
echo "3. 測試檔案上傳功能"
echo ""
echo "🛑 停止指令: pkill -f 'upload_handler.py' && pkill ngrok"
```

## 🧪 測試流程

1. **後端測試**
   ```bash
   curl https://你的-ngrok-網址.ngrok-free.dev/
   ```

2. **前端測試**
   打開瀏覽器訪問: `https://lobster-site.pages.dev`

3. **上傳測試**
   - 訪問 `https://lobster-site.pages.dev/simple_upload_cf.html`
   - 選擇檔案並上傳
   - 檢查後端日誌

## 📊 監控與維護

### 日誌檔案
- 後端日誌: `upload_server.log`
- ngrok 日誌: `ngrok.log`
- 上傳記錄: 檢查 `uploads/` 目錄

### 定期檢查
1. ngrok 網址是否變更
2. 後端伺服器是否運行
3. 上傳目錄空間使用情況

## 🔗 相關資源
- [Cloudflare Pages 文件](https://developers.cloudflare.com/pages/)
- [ngrok 文件](https://ngrok.com/docs)
- [CORS 說明](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

**最後更新**: 2026-04-21  
**架構版本**: 混合架構 v1.0  
**適用場景**: 靜態前端 + 動態後端分離部署