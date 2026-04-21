# 🦞 龔蝦米 Production-Ready 架構部署指南

## 🏗️ 架構選擇

### 方案 A：Cloudflare Worker（推薦）
- **前端**：Cloudflare Pages（已部署）
- **後端**：Cloudflare Worker（JavaScript）
- **儲存**：Cloudflare R2（可選）
- **優點**：完全在 Cloudflare 生態、無警告頁、固定網址、全球 CDN

### 方案 B：Cloudflare Tunnel
- **前端**：Cloudflare Pages（已部署）
- **後端**：Python + Cloudflare Tunnel
- **優點**：保留現有 Python 程式碼、無警告頁、固定網址

### 方案 C：混合架構（當前）
- **前端**：Cloudflare Pages（已部署）
- **後端**：ngrok + Python
- **問題**：ngrok 警告頁、網址不固定

## 🚀 部署 Cloudflare Worker（方案 A）

### 步驟 1：安裝必要工具
```bash
# 安裝 Node.js 和 npm
# 安裝 wrangler
npm install -g wrangler

# 登入 Cloudflare
wrangler login
```

### 步驟 2：部署 Worker
```bash
cd /tmp/lobster_website_cloudflare
./deploy_worker.sh
```

### 步驟 3：更新前端設定
修改前端 HTML 中的 `BACKEND_URL`：
```javascript
const BACKEND_URL = 'https://lobster-upload-worker.<你的子網域>.workers.dev';
```

## 🌐 部署 Cloudflare Tunnel（方案 B）

### 步驟 1：安裝 cloudflared
```bash
# Ubuntu/Debian
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# 或使用 Docker
docker run cloudflare/cloudflared:latest tunnel --help
```

### 步驟 2：建立 Tunnel
```bash
# 登入 Cloudflare
cloudflared tunnel login

# 建立 Tunnel
cloudflared tunnel create lobster-tunnel

# 設定 DNS（需要自有網域）
cloudflared tunnel route dns lobster-tunnel upload.lobster.yourdomain.com

# 啟動 Tunnel
cloudflared tunnel --config cloudflared.yml run lobster-tunnel
```

### 步驟 3：更新前端設定
```javascript
const BACKEND_URL = 'https://upload.lobster.yourdomain.com';
```

## 📊 架構比較

| 特性 | ngrok + Python | Cloudflare Worker | Cloudflare Tunnel |
|------|----------------|-------------------|-------------------|
| 警告頁 | ❌ 有 | ✅ 無 | ✅ 無 |
| 網址固定 | ❌ 不固定 | ✅ 固定 | ✅ 固定 |
| 部署複雜度 | ⭐ 簡單 | ⭐⭐ 中等 | ⭐⭐⭐ 複雜 |
| 程式碼修改 | 無需修改 | 需要改寫 | 無需修改 |
| 效能 | 中等 | 優秀（邊緣運算） | 良好 |
| 成本 | 免費（有限制） | 免費（有限額） | 免費 |

## 🔧 當前狀態

### 已部署
- ✅ 前端：<https://lobster-site-10m.pages.dev/>
- ✅ 後端：<https://intertergal-unfortuitous-hyon.ngrok-free.dev>
- ✅ CORS：已修正（全域 header）
- ✅ HEAD 請求：已實作

### 需要升級
- ⚠️ ngrok 警告頁問題
- ⚠️ 網址不固定問題

## 🎯 推薦升級路徑

### 短期（立即）
1. 測試當前架構功能
2. 確認檔案上傳正常

### 中期（本週）
1. 部署 Cloudflare Worker
2. 測試 Worker 功能
3. 更新前端設定

### 長期（未來）
1. 設定 R2 儲存
2. 設定自訂網域
3. 加入更多功能

## 🧪 測試指令

### 測試當前架構
```bash
# 測試 HEAD 請求
curl -I "https://intertergal-unfortuitous-hyon.ngrok-free.dev/" \
  -H "Origin: https://lobster-site-10m.pages.dev" \
  -H "ngrok-skip-browser-warning: 1"

# 測試檔案上傳
curl -X POST -F "file=@test.txt" \
  -H "ngrok-skip-browser-warning: 1" \
  "https://intertergal-unfortuitous-hyon.ngrok-free.dev/upload"
```

### 測試 Worker
```bash
# 測試 Worker 首頁
curl "https://lobster-upload-worker.<子網域>.workers.dev/"

# 測試 Worker 上傳
curl -X POST -F "file=@test.txt" \
  "https://lobster-upload-worker.<子網域>.workers.dev/upload"
```

## 📁 檔案說明

- `upload_handler.py` - Python 後端（已修正 CORS）
- `worker.js` - Cloudflare Worker 版本
- `wrangler.toml` - Worker 設定檔
- `deploy_worker.sh` - Worker 部署腳本
- `cloudflared.yml` - Tunnel 設定檔
- `PRODUCTION_DEPLOY.md` - 本文件

## 🔗 相關資源

- [Cloudflare Workers 文件](https://developers.cloudflare.com/workers/)
- [Cloudflare Tunnel 文件](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [Cloudflare Pages 文件](https://developers.cloudflare.com/pages/)
- [R2 儲存文件](https://developers.cloudflare.com/r2/)

---

**最後更新**: 2026-04-21  
**架構版本**: Production-Ready v1.0  
**狀態**: 等待升級到 Cloudflare Worker/Tunnel