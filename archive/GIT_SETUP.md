# 🚀 Git 自動部署設定指南

## 步驟 1：初始化 Git repository
```bash
cd /tmp/lobster_website_cloudflare

# 初始化 Git
git init

# 設定使用者資訊
git config user.email "your-email@example.com"
git config user.name "Your Name"

# 新增所有檔案
git add .

# 提交初始版本
git commit -m "初始提交：龔蝦米檔案上傳網站"
```

## 步驟 2：建立 GitHub repository
1. 前往 GitHub.com
2. 點擊 "New repository"
3. 輸入 repository 名稱 (例如: `lobster-upload-site`)
4. 選擇公開或私有
5. **不要**初始化 README、.gitignore 或 license
6. 點擊 "Create repository"

## 步驟 3：推送到 GitHub
```bash
# 新增遠端 repository
git remote add origin https://github.com/你的帳號/lobster-upload-site.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 步驟 4：設定 Cloudflare Pages Git 整合
1. 前往 Cloudflare Dashboard
2. 選擇 "Workers & Pages"
3. 點擊 "Create application" → "Pages"
4. 選擇 "Connect to Git"
5. 選擇你的 GitHub repository
6. 設定部署選項：
   - 專案名稱: `lobster-site-10m` (或新名稱)
   - 生產分支: `main`
   - 建置指令: (留空，直接部署)
   - 輸出目錄: `/` (根目錄)
7. 點擊 "Save and Deploy"

## 步驟 5：更新後端網址 (如果需要)
如果 Cloudflare Tunnel 網址變更：
1. 編輯 `simple_upload_cf.html`
2. 更新 `BACKEND_URL` 變數
3. 提交並推送更新
```bash
git add simple_upload_cf.html
git commit -m "更新後端網址"
git push origin main
```

## 步驟 6：測試部署
1. 等待 Cloudflare Pages 自動部署完成
2. 訪問部署網址 (例如: `https://lobster-site-10m.pages.dev`)
3. 測試檔案上傳功能

## 重要檔案說明
- `index.html` - 網站首頁
- `simple_upload_cf.html` - 檔案上傳頁面
- `upload_handler.py` - 後端伺服器
- `README_GIT.md` - 專案說明
- `.gitignore` - Git 忽略規則
- `MIGRATION_LOG.md` - 遷移記錄

## 自動化流程
```
GitHub Push → Cloudflare Pages → 自動部署 → 網站更新
```

## 注意事項
1. 確保後端伺服器持續運行
2. Cloudflare Tunnel 網址可能變動
3. 定期檢查部署狀態
4. 監控網站功能正常