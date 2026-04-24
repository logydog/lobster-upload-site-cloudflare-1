# 🦞 重新部署指南

## 修正內容
1. ✅ **前端顯示檔名**：選擇檔案時顯示檔名和大小
2. ✅ **CORS 修正**：解決 header 重複問題
3. ✅ **檔名保留**：後端正確取得原始檔名
4. ✅ **完整下載網址**：回傳完整 HTTPS 網址

## 重新部署步驟

### 方法 1：直接上傳到 Cloudflare Pages
1. 前往 Cloudflare Pages 控制台
2. 選擇 `lobster-site-10m` 專案
3. 點擊「上傳資產」
4. 上傳 `/tmp/lobster_fixed.zip` 檔案
5. 等待部署完成

### 方法 2：使用 wrangler CLI
```bash
# 解壓縮
unzip /tmp/lobster_fixed.zip -d /tmp/lobster_fixed

# 部署到 Cloudflare Pages
cd /tmp/lobster_fixed
npx wrangler pages deploy . --project-name=lobster-site-10m
```

### 方法 3：手動更新檔案
如果只想更新特定檔案：
1. 上傳 `/tmp/lobster_website_cloudflare/simple_upload_cf.html`
2. 上傳 `/tmp/lobster_website_cloudflare/index.html`

## 測試連結
- 首頁：<https://lobster-site-10m.pages.dev/>
- 檔案上傳：<https://lobster-site-10m.pages.dev/simple_upload_cf.html>

## 預期結果
✅ 選擇檔案時顯示「已選擇：檔名 (大小 KB)」
✅ 上傳成功顯示完整資訊
✅ 下載連結可直接點擊
✅ 連線狀態正常顯示

## 備註
- 後端已修正完成，不需重新啟動
- 前端修正需重新部署才會生效
- 打包檔案：`/tmp/lobster_fixed.zip` (47MB)