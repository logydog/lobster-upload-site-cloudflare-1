#!/usr/bin/env python3
"""
🦞 龔蝦米檔案上傳處理器（CORS 修正版）
處理來自網頁的表單檔案上傳
"""

import os
import json
import shutil
import cgi
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import mimetypes
import time

# 設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    '.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.zip', 
    '.rar', '.mp3', '.mp4', '.doc', '.docx', '.xls', '.xlsx',
    '.ppt', '.pptx', '.html', '.css', '.js', '.json', '.xml',
    '.md', '.csv', '.py', '.sh', '.yml', '.yaml'
}

class UploadHandler(BaseHTTPRequestHandler):
    
    def end_headers(self):
        """在所有回應中都加入 CORS header（只在這裡加）"""
        # 加入 CORS header
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, ngrok-skip-browser-warning')
        super().end_headers()
    
    def do_OPTIONS(self):
        """處理 CORS 預檢請求 (OPTIONS)"""
        self.send_response(200)
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def do_HEAD(self):
        """處理 HEAD 請求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            filepath = 'index.html'
        else:
            filepath = parsed_path.path[1:] or 'index.html'
        
        # 建立完整路徑
        full_filepath = os.path.join(BASE_DIR, filepath)
        
        if os.path.exists(full_filepath) and os.path.isfile(full_filepath):
            self.send_response(200)
            
            if filepath.endswith('.html'):
                self.send_header('Content-type', 'text/html; charset=utf-8')
            elif filepath.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif filepath.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            else:
                mime_type, _ = mimetypes.guess_type(filepath)
                self.send_header('Content-type', mime_type or 'application/octet-stream')
            
            self.end_headers()
        else:
            self.send_error(404, "File not found")
    
    def do_GET(self):
        """處理 GET 請求"""
        parsed_path = urlparse(self.path)
        
        # 根目錄
        if parsed_path.path == '/':
            filepath = 'index.html'
        else:
            filepath = parsed_path.path[1:] or 'index.html'
        
        # 建立完整路徑
        full_filepath = os.path.join(BASE_DIR, filepath)
        
        # 檢查檔案是否存在
        if os.path.exists(full_filepath) and os.path.isfile(full_filepath):
            self.send_response(200)
            
            # 設定正確的 Content-Type
            if filepath.endswith('.html'):
                self.send_header('Content-type', 'text/html; charset=utf-8')
            elif filepath.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif filepath.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            else:
                mime_type, _ = mimetypes.guess_type(filepath)
                self.send_header('Content-type', mime_type or 'application/octet-stream')
            
            self.end_headers()
            
            # 讀取並傳送檔案
            with open(full_filepath, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
        
        # 上傳檔案下載
        elif parsed_path.path.startswith('/uploads/'):
            filename = parsed_path.path[8:]  # 移除 '/uploads/'
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            if os.path.exists(filepath) and os.path.isfile(filepath):
                self.send_response(200)
                
                mime_type, _ = mimetypes.guess_type(filepath)
                # ⭐ 修正 encoding
                if mime_type and mime_type.startswith('text'):
                    self.send_header('Content-type', f'{mime_type}; charset=utf-8')
                elif mime_type == 'application/json':
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                else:
                    self.send_header('Content-type', mime_type or 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                
                with open(filepath, 'rb') as f:
                    shutil.copyfileobj(f, self.wfile)
            else:
                self.send_error(404, "File not found")
        
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """處理 POST 請求（檔案上傳）"""
        if self.path != '/upload':
            self.send_error(404, "Not Found")
            return
        
        # 檢查 Content-Type
        content_type, pdict = cgi.parse_header(self.headers.get('content-type', ''))
        
        if content_type != 'multipart/form-data':
            self.send_error(400, "Only multipart/form-data supported")
            return
        
        try:
            # 解析 multipart/form-data，保留檔名
            content_length = int(self.headers.get('content-length', '0'))
            if content_length > MAX_FILE_SIZE:
                self.send_error(413, f"File too large (max {MAX_FILE_SIZE//1024//1024}MB)")
                return
            
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers.get('content-type', ''),
                'CONTENT_LENGTH': str(content_length),
            }
            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ=environ,
                keep_blank_values=True,
            )
            
            if 'file' not in form:
                self.send_error(400, "No file field")
                return
            
            file_item = form['file']
            
            if not getattr(file_item, 'filename', None):
                self.send_error(400, "No filename provided")
                return
            
            filename = os.path.basename(str(file_item.filename)).strip()
            
            if not file_item.file:
                self.send_error(400, "No file uploaded")
                return
            
            file_data = file_item.file.read()
            
            if not file_data:
                self.send_error(400, "No file uploaded")
                return
            
            if not filename or not file_data:
                self.send_error(400, "No file uploaded")
                return
            
            # 檢查檔案大小
            if len(file_data) > MAX_FILE_SIZE:
                self.send_error(413, f"File too large (max {MAX_FILE_SIZE//1024//1024}MB)")
                return
            
            # 檢查副檔名
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                self.send_error(400, f"File type not allowed: {ext}")
                return
            
            # 確保上傳目錄存在
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)
            
            # 產生安全檔名
            safe_filename = os.path.basename(filename)
            filepath = os.path.join(UPLOAD_DIR, safe_filename)
            
            # 避免檔名衝突
            counter = 1
            while os.path.exists(filepath):
                name, ext = os.path.splitext(safe_filename)
                safe_filename = f"{name}_{counter}{ext}"
                filepath = os.path.join(UPLOAD_DIR, safe_filename)
                counter += 1
            
            # 儲存檔案
            with open(filepath, 'wb') as f:
                f.write(file_data)
            
            # 檢查請求是否來自 JavaScript (有 Origin header)
            origin = self.headers.get('Origin', '')
            is_js_request = origin and ('pages.dev' in origin or 'localhost' in origin)
            
            if is_js_request:
                # 回傳 JSON 給 JavaScript
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('ngrok-skip-browser-warning', 'true')
                self.end_headers()
                
                # 建立完整的下載網址
                backend_base = self.headers.get('Host', 'localhost:8890')
                if 'ngrok-free.dev' in backend_base:
                    download_url = f'https://{backend_base}/uploads/{safe_filename}'
                elif 'trycloudflare.com' in backend_base:
                    download_url = f'https://{backend_base}/uploads/{safe_filename}'
                else:
                    download_url = f'/uploads/{safe_filename}'
                
                response_json = {
                    'success': True,
                    'filename': safe_filename,
                    'size_bytes': len(file_data),
                    'size_kb': round(len(file_data) / 1024, 2),
                    'download_url': download_url,
                    'message': '檔案上傳成功',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                self.wfile.write(json.dumps(response_json, ensure_ascii=False).encode('utf-8'))
                return
            else:
                # 回傳 HTML 成功頁面（讓傳統表單可以正常顯示）
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('ngrok-skip-browser-warning', 'true')
                self.end_headers()
                
                html_response = f'''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦞 檔案上傳成功</title>
    <style>
        body {{ font-family: 'Microsoft JhengHei', sans-serif; padding: 20px; }}
        .success {{ color: green; font-size: 1.2em; }}
        .info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .button {{ background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }}
    </style>
</head>
<body>
    <h1>✅ 檔案上傳成功！</h1>
    
    <div class="info">
        <p><strong>檔名：</strong> {safe_filename}</p>
        <p><strong>大小：</strong> {len(file_data)} bytes</p>
        <p><strong>下載連結：</strong> <a href="/uploads/{safe_filename}" target="_blank">/uploads/{safe_filename}</a></p>
        <p><strong>時間：</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h3>下一步：</h3>
    <p>
        <a href="/simple_upload.html" class="button">繼續上傳檔案</a>
        <a href="/" class="button" style="background: #2196F3;">回到主頁</a>
        <a href="/uploads/{safe_filename}" class="button" style="background: #FF9800;">下載檔案</a>
    </p>
    
    <hr>
    <p style="font-size: 0.9em; color: #666;">
        技術架構：前端 Cloudflare Pages + 後端 ngrok + Python<br>
        檔案儲存：本地伺服器 /tmp/lobster_website_cloudflare/uploads/
    </p>
</body>
</html>
'''
                self.wfile.write(html_response.encode('utf-8'))
        
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

def run_server(port=8890):
    """啟動伺服器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, UploadHandler)
    print(f"🦞 伺服器啟動在 http://localhost:{port}")
    print(f"📁 上傳目錄: {os.path.abspath(UPLOAD_DIR)}")
    print(f"🌐 等待 ngrok 轉發...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
