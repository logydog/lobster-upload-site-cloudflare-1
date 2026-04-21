// 🦞 龔蝦米檔案上傳 Worker
// 部署到 Cloudflare Workers

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, HEAD',
      'Access-Control-Allow-Headers': 'Content-Type',
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
            font-size: 3em;
            margin-bottom: 20px;
        }
        .lobster {
            font-size: 5em;
            margin: 30px 0;
        }
        .status {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 30px auto;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <div class="lobster">🦞</div>
    <h1>龔蝦米 Worker 網站</h1>
    <div class="status">
        <h3>✅ 部署成功</h3>
        <p>Cloudflare Worker 已正常運行</p>
        <p>檔案上傳功能準備就緒</p>
    </div>
    <p>架構：Cloudflare Worker + R2 儲存</p>
</body>
</html>`;
        
        return new Response(html, {
          headers: {
            ...corsHeaders,
            'Content-Type': 'text/html; charset=utf-8',
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
          return new Response('請選擇檔案', {
            status: 400,
            headers: corsHeaders,
          });
        }
        
        // 檢查檔案大小（10MB）
        if (file.size > 10 * 1024 * 1024) {
          return new Response('檔案太大（最大 10MB）', {
            status: 400,
            headers: corsHeaders,
          });
        }
        
        // 讀取檔案內容
        const fileBuffer = await file.arrayBuffer();
        const fileName = file.name || 'uploaded_file';
        
        // 如果有 R2 bucket，儲存檔案
        // if (env.MY_BUCKET) {
        //   await env.MY_BUCKET.put(fileName, fileBuffer);
        // }
        
        // 回傳成功訊息
        const successHtml = `<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✅ 上傳成功</title>
    <style>
        body {
            font-family: 'Microsoft JhengHei', sans-serif;
            padding: 40px;
            text-align: center;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .file-info {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px auto;
            max-width: 500px;
        }
    </style>
</head>
<body>
    <h1>✅ 檔案上傳成功</h1>
    <div class="file-info">
        <p><strong>檔案名稱：</strong>${fileName}</p>
        <p><strong>檔案大小：</strong>${(file.size / 1024).toFixed(2)} KB</p>
        <p><strong>檔案類型：</strong>${file.type || '未知'}</p>
    </div>
    <p>檔案已成功接收，如需永久儲存請設定 R2 bucket。</p>
    <p><a href="/" style="color: white; text-decoration: underline;">返回首頁</a></p>
</body>
</html>`;
        
        return new Response(successHtml, {
          headers: {
            ...corsHeaders,
            'Content-Type': 'text/html; charset=utf-8',
          },
        });
        
      } catch (error) {
        return new Response(`上傳錯誤：${error.message}`, {
          status: 500,
          headers: corsHeaders,
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