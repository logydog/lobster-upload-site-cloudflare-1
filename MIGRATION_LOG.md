# 🦞 網站遷移記錄

## 遷移時間
2026-04-22 00:46 GMT+8

## 當前架構狀態

### 前端（Cloudflare Pages）
- 網址：https://lobster-site-10m.pages.dev/
- 檔案位置：/tmp/lobster_website_cloudflare/
- 主要檔案：
  - index.html (首頁)
  - simple_upload_cf.html (檔案上傳頁面)
- 後端網址：https://conference-simply-mattress-arab.trycloudflare.com

### 後端（Python + Cloudflare Tunnel）
- 網址：https://conference-simply-mattress-arab.trycloudflare.com
- 程式：upload_handler.py (運行在端口 8890)
- 檔案儲存：/tmp/lobster_website_cloudflare/uploads/

### 已完成修正
1. ✅ CORS header 重複問題
2. ✅ 檔名丟失問題 (cgi.FieldStorage)
3. ✅ 下載網址重複問題
4. ✅ 上傳目錄路徑問題 (BASE_DIR)
5. ✅ 前端顯示檔名功能
6. ✅ Cloudflare Tunnel 設定

## 遷移任務清單

### 任務 1：修改上傳頁文案
- 檔案：simple_upload_cf.html
- 修改：更新說明文字，反映 Git 自動部署架構

### 任務 2：更換後端網址
- 檔案：simple_upload_cf.html
- 修改：更新 BACKEND_URL 變數

### 任務 3：推送到 GitHub
- 建立 GitHub repository
- 設定 Git 自動部署到 Cloudflare Pages

## 注意事項
1. Cloudflare Tunnel 網址可能變動
2. 需要設定 GitHub Actions 或 Cloudflare Pages Git 整合
3. 後端程式需保持運行狀態

## 檔案清單（需要推送到 GitHub）
- index.html
- simple_upload_cf.html
- upload_handler.py
- 其他相關檔案

## 部署指令參考
```bash
# 本地測試
python3 upload_handler.py

# Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8890

# Git 部署
git add .
git commit -m "部署龔蝦米網站"
git push origin main
```