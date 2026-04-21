#!/usr/bin/env python3
"""
龔蝦米網站伺服器啟動腳本
啟動 Python HTTP 伺服器在指定端口
"""

import http.server
import socketserver
import sys
import os
import signal
import time

PORT = 8888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        # 自訂日誌格式
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")
    
    def end_headers(self):
        # 添加 CORS 標頭
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server(port=PORT):
    """啟動 HTTP 伺服器"""
    os.chdir(DIRECTORY)
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🦞 龔蝦米網站伺服器啟動成功！")
            print(f"📁 目錄: {DIRECTORY}")
            print(f"🌐 網址: http://localhost:{port}")
            print(f"📄 首頁: http://localhost:{port}/index.html")
            print("\n按 Ctrl+C 停止伺服器")
            
            # 設定信號處理
            def signal_handler(sig, frame):
                print("\n\n🛑 收到停止信號，正在關閉伺服器...")
                httpd.shutdown()
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 錯誤: Port {port} 已被佔用")
            print("請嘗試以下解決方案：")
            print(f"1. 使用其他端口: python3 {sys.argv[0]} --port 8889")
            print("2. 停止佔用該端口的程序")
            print("3. 等待幾分鐘後重試")
            return 1
        else:
            print(f"❌ 伺服器啟動失敗: {e}")
            return 1
    except Exception as e:
        print(f"❌ 伺服器錯誤: {e}")
        return 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='啟動龔蝦米網站伺服器')
    parser.add_argument('--port', type=int, default=PORT, 
                       help=f'伺服器端口 (預設: {PORT})')
    parser.add_argument('--directory', type=str, default=DIRECTORY,
                       help=f'網站目錄 (預設: {DIRECTORY})')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🦞 龔蝦米網站伺服器")
    print("=" * 50)
    
    # 檢查目錄是否存在
    if not os.path.exists(args.directory):
        print(f"❌ 錯誤: 目錄不存在 - {args.directory}")
        sys.exit(1)
    
    # 檢查 index.html 是否存在
    index_path = os.path.join(args.directory, "index.html")
    if not os.path.exists(index_path):
        print(f"⚠️  警告: index.html 不存在於 {args.directory}")
        print("將顯示目錄列表")
    
    # 啟動伺服器
    sys.exit(start_server(args.port))