// 🦞 龔蝦米檔案上傳 Worker（進階版）
// 支援記憶體暫存檔案和下載功能

// 記憶體儲存（暫存，Worker 重啟會消失）
const fileStorage = new Map();

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, HEAD',
      'Access-Control-Allow-Headers': 'Content-Type, ngrok-skip-browser-warning',
    };
    
    // 處理 OPTIONS 預檢請求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          ...corsHeaders,
          'Access-Control-Max-Age': '86400',
        },
      });
    }
    
    // 處理 HEAD 請求
    if (request.method === 'HEAD') {
      return new Response(null, {
        headers: {
          ...corsHeaders,
          'Content-Type': 'text/html; charset=utf-8',
        },
      });
    }
    
    // 處理 GET 請求
    if (request.method === 'GET') {
      // 根目錄
      if (url.pathname === '/') {
        const html = `<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦞 龔蝦米 Worker 網站</title>
    <style>
        body {
            font-family: 'Microsoft JhengHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .info {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px auto;
            max-width: 600px;
        }
        .upload-form {
            border: 3px dashed rgba(255, 255, 255, 0.3);
            padding: 30px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            margin: 30px auto;
            max-width: 500px;
        }
        input[type="file"] {
            padding: 10px;
            margin: 10px 0;
            background: white;
            border-radius: 5px;
            width: 100%;
            max-width: 300px;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
        }
        .success { background: rgba(76, 175, 80, 0.2); }
        .error { background: rgba(244, 67, 54, 0.2); }
    </style>
</head>
<body>
    <h1>🦞 龔蝦米檔案上傳</h1>
    <div class="info">
        <h3>🏗️ Cloudflare Worker 架構</h3>
        <p>此網站完全運行在 <strong>Cloudflare Workers</strong> 上</p>
        <p>✅ 無 ngrok 警告頁</p>
        <p>✅ 固定網址</p>
        <p>✅ 全球 CDN 加速</p>
        <p>⚠️ 檔案暫存記憶體（Worker 重啟會消失）</p>
    </div>
    
    <div class="upload-form">
        <h3>選擇要上傳的檔案：</h3>
        <input type="file" id="fileInput">
        <div id="selectedFileName" style="margin-top:10px; color:white;"></div>
        <br><br>
        <button onclick="uploadFile()">📤 上傳檔案</button>
    </div>
    
    <div id="status" class="status"></div>
    
    <script>
        const BACKEND_URL = '${url.origin}';
        
        // 檔案選擇顯示
        document.getElementById('fileInput').addEventListener('change', function () {
            const file = this.files[0];
            const display = document.getElementById('selectedFileName');
            
            if (file) {
                display.textContent = \`已選擇：\${file.name} (\${(file.size / 1024).toFixed(1)} KB)\`;
                display.style.color = '#4CAF50';
                display.style.fontWeight = 'bold';
            } else {
                display.textContent = '';
            }
        });
        
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            const statusDiv = document.getElementById('status');
            
            if (!file) {
                statusDiv.className = 'status error';
                statusDiv.innerHTML = '<h3>❌ 請選擇檔案</h3>';
                return;
            }
            
            if (file.size > 10 * 1024 * 1024) {
                statusDiv.className = 'status error';
                statusDiv.innerHTML = '<h3>❌ 檔案太大（最大 10MB）</h3>';
                return;
            }
            
            statusDiv.className = 'status';
            statusDiv.innerHTML = '<h3>⏳ 上傳中...</h3>';
            
            try {
                const formData = new FormData();
                formData.append('file', file);
                
                const response = await fetch(BACKEND_URL + '/upload', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'ngrok-skip-browser-warning': '1'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    
                    statusDiv.className = 'status success';
                    statusDiv.innerHTML = \`
                        <h3>✅ 上傳成功！</h3>
                        <p>檔案：\${data.filename}</p>
                        <p>大小：\${data.size_kb} KB</p>
                        <p>時間：\${data.timestamp}</p>
                        <p><a href="\${data.download_url}" target="_blank" style="color: #4CAF50;">下載連結</a></p>
                    \`;
                    
                    // 清空檔案選擇
                    fileInput.value = '';
                    document.getElementById('selectedFileName').textContent = '';
                } else {
                    const errorText = await response.text();
                    statusDiv.className = 'status error';
                    statusDiv.innerHTML = \`<h3>❌ 上傳失敗</h3><p>狀態碼：\${response.status}</p><p>錯誤：\${errorText}</p>\`;
                }
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.innerHTML = \`<h3>❌ 網路錯誤</h3><p>\${error.message}</p>\`;
            }
        }
    </script>
</body>
</html>`;
        
        return new Response(html, {
          headers: {
            ...corsHeaders,
            'Content-Type': 'text/html; charset=utf-8',
          },
        });
      }
      
      // 下載檔案
      if (url.pathname.startsWith('/download/')) {
        const fileId = url.pathname.split('/')[2];
        const fileData = fileStorage.get(fileId);
        
        if (!fileData) {
          return new Response('檔案不存在', {
            status: 404,
            headers: corsHeaders,
          });
        }
        
        return new Response(fileData.content, {
          headers: {
            ...corsHeaders,
            'Content-Type': fileData.type || 'application/octet-stream',
            'Content-Disposition': \`attachment; filename="\${fileData.filename}"\`,
          },
        });
      }
      
      // 其他 GET 請求
      return new Response('Not Found', {
        status: 404,
        headers: corsHeaders,
      });
    }
    
    // 處理 POST 請求（檔案上傳）
    if (request.method === 'POST' && url.pathname === '/upload') {
      try {
        const formData = await request.formData();
        const file = formData.get('file');
        
        if (!file) {
          return new Response(JSON.stringify({
            success: false,
            error: '請選擇檔案'
          }), {
            status: 400,
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json; charset=utf-8',
            },
          });
        }
        
        // 檢查檔案大小（10MB）
        if (file.size > 10 * 1024 * 1024) {
          return new Response(JSON.stringify({
            success: false,
            error: '檔案太大（最大 10MB）'
          }), {
            status: 400,
            headers: {
              ...corsHeaders,
              'Content-Type': 'application/json; charset=utf-8',
            },
          });
        }
        
        // 讀取檔案內容
        const fileBuffer = await file.arrayBuffer();
        const fileName = file.name || 'uploaded_file';
        const fileId = Date.now().toString(36) + Math.random().toString(36).substr(2);
        
        // 儲存到記憶體
        fileStorage.set(fileId, {
          filename: fileName,
          content: fileBuffer,
          type: file.type,
          size: file.size,
          uploaded: new Date().toISOString(),
        });
        
        // 建立下載網址
        const downloadUrl = \`\${url.origin}/download/\${fileId}\`;
        
        // 回傳 JSON 成功訊息
        const responseData = {
          success: true,
          filename: fileName,
          size_bytes: file.size,
          size_kb: Math.round(file.size / 1024 * 100) / 100,
          download_url: downloadUrl,
          message: '檔案上傳成功',
          timestamp: new Date().toLocaleString('zh-TW'),
        };
        
        return new Response(JSON.stringify(responseData), {
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json; charset=utf-8',
            'ngrok-skip-browser-warning': 'true',
          },
        });
        
      } catch (error) {
        return new Response(JSON.stringify({
          success: false,
          error: error.message
        }), {
          status: 500,
          headers: {
            ...corsHeaders,
            'Content-Type': 'application/json; charset=utf-8',
          },
        });
      }
    }
    
    // 其他請求
    return new Response('Not Found', {
      status: 404,
      headers: corsHeaders,
    });
  },
};