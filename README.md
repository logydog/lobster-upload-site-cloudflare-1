# 🦞 龔蝦米網站 - 手動啟動指南

由於系統限制，無法自動啟動伺服器。請按照以下步驟手動啟動：

## 1. 檢查檔案
所有網站檔案已準備在 `/tmp/lobster_website/` 目錄中：

```
/tmp/lobster_website/
├── index.html          # 網站首頁
├── start_server.py     # Python 伺服器腳本
├── start.sh           # 啟動腳本（需手動執行）
└── status.txt         # 狀態報告
```

## 2. 手動啟動伺服器

### 方法 A：使用 Python 直接啟動
```bash
cd /tmp/lobster_website
python3 start_server.py --port 8888
```

如果端口 8888 被佔用，嘗試其他端口：
```bash
python3 start_server.py --port 8889
python3 start_server.py --port 8890
python3 start_server.py --port 8891
```

### 方法 B：使用簡單 Python HTTP 伺服器
```bash
cd /tmp/lobster_website
python3 -m http.server 8888
```

## 3. 公開網站（可選）

### 使用 ngrok
```bash
# 在另一個終端視窗執行
ngrok http 8888
```

### 取得公開網址
ngrok 啟動後，會顯示公開網址。也可以透過 API 取得：
```bash
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])"
```

## 4. 測試網站

### 本地測試
```bash
curl http://localhost:8888/
```

### 公開網址測試
```bash
curl https://your-subdomain.ngrok-free.dev/
```

## 5. 停止伺服器

### 停止 Python 伺服器
按 `Ctrl+C` 在執行伺服器的終端視窗中

### 停止 ngrok
按 `Ctrl+C` 在執行 ngrok 的終端視窗中

## 網站功能

1. **靜態網站** - 顯示 index.html 內容
2. **檔案瀏覽** - 瀏覽網站目錄中的檔案
3. **基本 HTTP 服務** - 支援 GET 請求

## 注意事項

1. **臨時性** - 檔案儲存在 `/tmp/`，系統重啟可能消失
2. **公開性** - 使用 ngrok 公開後，任何人只要有連結都能訪問
3. **簡單性** - 這是基本靜態網站，無上傳功能

## 問題排除

### 端口被佔用
```bash
# 檢查哪些程序使用端口
sudo lsof -i :8888
# 或
sudo netstat -tlnp | grep :8888
```

### Python 錯誤
確保使用 Python 3：
```bash
python3 --version
```

### 權限問題
確保有權限讀取 `/tmp/lobster_website/` 目錄

---

**最後更新**: 網站檔案已準備就緒，等待手動啟動