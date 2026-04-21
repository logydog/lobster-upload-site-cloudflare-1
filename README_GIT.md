# 🦞 龔蝦米檔案上傳網站

## 架構說明
- **前端**: Cloudflare Pages (Git 自動部署)
- **後端**: Python + Cloudflare Tunnel
- **儲存**: 本地檔案系統 (uploads/ 目錄)

## 功能特色
✅ 檔案上傳 (最大 10MB)
✅ 即時顯示檔名和大小
✅ 下載連結自動生成
✅ 跨域支援 (CORS)
✅ 無警告頁面 (Cloudflare Tunnel)
✅ Git 自動部署

## 檔案結構
```
.
├── index.html                    # 首頁
├── simple_upload_cf.html         # 檔案上傳頁面
├── upload_handler.py             # 後端伺服器
├── uploads/                      # 上傳檔案目錄
├── README_GIT.md                 # 本文件
└── MIGRATION_LOG.md             # 遷移記錄
```

## 部署步驟

### 1. 後端設定
```bash
# 啟動後端伺服器
python3 upload_handler.py

# 使用 Cloudflare Tunnel 公開
cloudflared tunnel --url http://localhost:8890
```

### 2. 前端部署 (Cloudflare Pages)
1. 將此 repository 連接到 Cloudflare Pages
2. 設定部署分支 (main/master)
3. 設定建置指令 (無需建置，直接部署)
4. 設定輸出目錄 (根目錄)

### 3. 環境變數
- 後端網址: `https://conference-simply-mattress-arab.trycloudflare.com`
- 前端網址: `https://lobster-site-10m.pages.dev/`

## 技術細節

### 後端 (upload_handler.py)
- 端口: 8890
- 支援: GET, POST, OPTIONS, HEAD
- CORS: 完全支援跨域
- 檔案類型: 多種常見檔案格式
- 大小限制: 10MB

### 前端 (simple_upload_cf.html)
- 使用 Fetch API 進行跨域上傳
- 即時顯示選擇的檔案資訊
- 狀態提示和錯誤處理
- 響應式設計

## 更新後端網址
如果 Cloudflare Tunnel 網址變更，需要更新：
1. `simple_upload_cf.html` 中的 `BACKEND_URL` 變數
2. `index.html` 中的相關連結

## 維護指令
```bash
# 檢查後端狀態
curl -I https://conference-simply-mattress-arab.trycloudflare.com/

# 測試檔案上傳
curl -X POST -F "file=@test.txt" https://conference-simply-mattress-arab.trycloudflare.com/upload

# 查看上傳目錄
ls -la uploads/
```

## 注意事項
1. Cloudflare Tunnel 網址可能變動，需定期檢查
2. 檔案儲存在本地，重啟伺服器不會消失 (uploads/ 目錄)
3. 建議設定監控確保後端持續運行
4. 可考慮升級到 Cloudflare Worker + R2 儲存