# 🌐 Cloudflare Pages Git 自動部署設定

## ✅ 已完成步驟
1. ✅ 建立 GitHub repository: `lobster-upload-site-cloudflare-1`
2. ✅ 推送所有檔案到 GitHub
3. ✅ 前端檔案已更新後端網址
4. ✅ 後端伺服器持續運行中

## 🚀 Cloudflare Pages 設定步驟

### 步驟 1：前往 Cloudflare Dashboard
1. 登入 Cloudflare Dashboard
2. 選擇 "Workers & Pages"
3. 點擊 "Create application" → "Pages"

### 步驟 2：連接 GitHub
1. 選擇 "Connect to Git"
2. 授權 Cloudflare 存取 GitHub
3. 選擇 repository: `logydog/lobster-upload-site-cloudflare-1`

### 步驟 3：設定部署選項
```
專案名稱: lobster-site-10m (或新名稱)
生產分支: main
建置指令: (留空，直接部署)
輸出目錄: / (根目錄)
```

### 步驟 4：部署設定
1. 點擊 "Save and Deploy"
2. 等待首次部署完成
3. 取得部署網址 (例如: `https://lobster-site-10m.pages.dev`)

## 🔗 重要網址

### 前端 (Git 自動部署)
- GitHub: https://github.com/logydog/lobster-upload-site-cloudflare-1
- Cloudflare Pages: `https://<專案名稱>.pages.dev`

### 後端 (Cloudflare Tunnel)
- 當前網址: `https://conference-simply-mattress-arab.trycloudflare.com`
- 本地端口: `8890`
- 程式: `upload_handler.py`

## 📁 檔案說明

### 核心檔案
- `index.html` - 網站首頁
- `simple_upload_cf.html` - 檔案上傳頁面 (已更新後端網址)
- `upload_handler.py` - 後端伺服器

### 部署檔案
- `README_GIT.md` - 專案說明
- `GIT_SETUP.md` - Git 部署指南
- `CLOUDFLARE_PAGES_SETUP.md` - 本文件

### 開發檔案
- `worker.js` - Cloudflare Worker 版本
- `worker_advanced.js` - 進階 Worker 版本
- `wrangler.toml` - Worker 設定

## 🔄 自動化流程
```
Git Push → GitHub → Cloudflare Pages → 自動部署 → 網站更新
```

## 🛠️ 維護指令

### 本地開發
```bash
# 啟動後端
python3 upload_handler.py

# 測試前端
python3 -m http.server 8000
```

### Git 操作
```bash
# 更新檔案
git add .
git commit -m "更新說明"
git push origin main

# 檢查狀態
git status
git log --oneline
```

### 後端管理
```bash
# 檢查後端狀態
curl -I https://conference-simply-mattress-arab.trycloudflare.com/

# 測試上傳
curl -X POST -F "file=@test.txt" https://conference-simply-mattress-arab.trycloudflare.com/upload
```

## ⚠️ 注意事項
1. Cloudflare Tunnel 網址可能變動，需定期檢查
2. 後端伺服器需保持運行狀態
3. 檔案儲存在本地 `uploads/` 目錄
4. 建議設定監控確保服務正常

## 🎯 測試檢查清單
- [ ] Cloudflare Pages 部署成功
- [ ] 前端網址可正常訪問
- [ ] 檔案上傳功能正常
- [ ] 下載連結正確
- [ ] 檔名顯示正常

## 🔧 故障排除
1. **502 錯誤**: 後端未運行，重啟 `upload_handler.py`
2. **CORS 錯誤**: 檢查後端 CORS header
3. **檔案上傳失敗**: 檢查 `uploads/` 目錄權限
4. **網址變更**: 更新 `simple_upload_cf.html` 中的 `BACKEND_URL`