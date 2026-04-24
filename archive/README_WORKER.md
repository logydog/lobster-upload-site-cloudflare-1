# 🦞 龔蝦米 Cloudflare Worker 部署指南

## 🚀 快速開始

### 1. 準備環境
```bash
cd /tmp/lobster_website_cloudflare

# 安裝依賴（如果還沒安裝）
npm install
```

### 2. 登入 Cloudflare
```bash
npx wrangler login
```
- 會打開瀏覽器，授權 Cloudflare 存取
- 授權完成後回到終端機

### 3. 部署 Worker
```bash
npx wrangler deploy
```
- 第一次部署會詢問專案名稱
- 部署完成後會顯示 Worker 網址

### 4. 更新前端設定
```bash
# 假設 Worker 網址是：https://lobster-upload-worker.example.workers.dev
./update_frontend.sh https://lobster-upload-worker.example.workers.dev
```

### 5. 重新部署前端
1. 壓縮整個目錄
2. 到 Cloudflare Dashboard → Workers & Pages → Pages
3. 重新上傳檔案
4. 等待部署完成

## 📁 檔案結構

```
/tmp/lobster_website_cloudflare/
├── worker.js              # Worker 程式碼
├── wrangler.toml          # Worker 設定
├── package.json           # 依賴管理
├── deploy_simple.sh       # 部署腳本
├── update_frontend.sh     # 前端更新腳本
├── index.html             # 混合架構首頁
├── simple_upload_cf.html  # 檔案上傳頁面
├── upload_handler.py      # Python 後端（備用）
└── README_WORKER.md       # 本文件
```

## 🔧 Worker 功能

### 支援的端點
- `GET /` - 首頁
- `HEAD /` - 連線檢查
- `OPTIONS /` - CORS 預檢
- `POST /upload` - 檔案上傳

### 檔案限制
- 最大檔案大小：10MB
- 支援所有檔案類型
- 暫時儲存（可擴展到 R2）

## 🌐 網址範例

- Worker 網址：`https://lobster-upload-worker.<子網域>.workers.dev`
- 前端網址：`https://lobster-site-10m.pages.dev/`

## 🧪 測試指令

```bash
# 測試 Worker 首頁
curl "https://lobster-upload-worker.example.workers.dev/"

# 測試檔案上傳
echo "測試檔案" > test.txt
curl -X POST -F "file=@test.txt" "https://lobster-upload-worker.example.workers.dev/upload"

# 測試 CORS
curl -I "https://lobster-upload-worker.example.workers.dev/" \
  -H "Origin: https://lobster-site-10m.pages.dev"
```

## ⚡ 效能優勢

1. **全球 CDN** - 邊緣運算，低延遲
2. **無警告頁** - 沒有 ngrok 警告頁面
3. **固定網址** - 網址不會變動
4. **自動擴展** - 根據流量自動調整
5. **免費額度** - 足夠個人使用

## 🔄 從 ngrok 遷移

### 變更需要
1. **後端網址**：從 ngrok 改為 Worker
2. **程式語言**：從 Python 改為 JavaScript
3. **部署方式**：從本地執行改為雲端部署

### 不變項目
1. **前端介面**：完全一樣
2. **使用者體驗**：完全一樣
3. **檔案上傳流程**：完全一樣

## 🆘 常見問題

### Q: 部署失敗怎麼辦？
A: 檢查：
1. 是否已登入 Cloudflare (`npx wrangler whoami`)
2. 網路連線是否正常
3. 查看錯誤訊息

### Q: 如何查看日誌？
A: 使用 wrangler：
```bash
npx wrangler tail
```

### Q: 如何更新 Worker？
A: 修改 `worker.js` 後重新部署：
```bash
npx wrangler deploy
```

### Q: 如何設定自訂網域？
A: 在 Cloudflare Dashboard 設定：
1. Workers & Pages → 你的 Worker
2. Triggers → Custom Domains
3. 新增自訂網域

## 📈 擴展功能

### 1. 加入 R2 儲存
```javascript
// 在 worker.js 中
const fileBuffer = await file.arrayBuffer();
await env.MY_BUCKET.put(fileName, fileBuffer);
```

### 2. 加入資料庫
- 使用 D1 (SQLite)
- 使用 KV (鍵值儲存)

### 3. 加入身份驗證
- 使用 Cloudflare Access
- 使用 JWT 令牌

## 📞 支援

如有問題：
1. 查看 Cloudflare 文件
2. 檢查部署日誌
3. 重新執行部署步驟

---

**部署狀態**: 等待執行  
**預計時間**: 5-10 分鐘  
**成功指標**: Worker 網址可正常存取