import os
import logging
from datetime import datetime
import time  # 新增：用于计算 uptime
from flask import Flask, jsonify, request, render_template_string
import psutil  # For memory and loadavg

# Logging setup similar to pino
logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO').upper(),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ========== Fixed port (env PORT or default 14659) ==========
PORT = int(os.environ.get('PORT', 14659))
logger.info(f'✅ Fixed port: {PORT} (set PORT env to override)')

# KV store
kv = {}

@app.before_request
def log_request():
    logger.info(f'{request.method} {request.url} - {request.remote_addr}')

@app.route('/healthy', methods=['GET'])
def healthy():
    process = psutil.Process()  # 获取当前进程
    memory_info = process.memory_info()  # 获取内存信息
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'uptime': time.time() - process.create_time(),  # 进程运行时间（秒）
        'memory': {
            'rss': memory_info.rss,  # 驻留集大小
            'vms': memory_info.vms   # 虚拟内存大小
        },
        'loadavg': psutil.getloadavg(),
        'port': PORT,
    })

@app.route('/kv/<key>', methods=['GET'])
def get_kv(key):
    if key not in kv:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'key': key, 'value': kv[key]})

@app.route('/kv/<key>', methods=['PUT'])
def put_kv(key):
    data = request.get_json()
    if 'value' not in data:
        return jsonify({'error': 'value required'}), 400
    kv[key] = data['value']
    return jsonify({'key': key, 'value': data['value']})

@app.route('/kv/<key>', methods=['DELETE'])
def delete_kv(key):
    if key in kv:
        del kv[key]
    return jsonify({'deleted': key})

@app.route('/', methods=['GET'])
def index():
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wispbyte Python Service</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            flex-direction: column;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
        }
        h1 {
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        p {
            font-size: 1.2em;
            margin-bottom: 20px;
            color: #718096;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .info-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        .info-card h3 {
            margin: 0 0 10px 0;
            font-size: 1.1em;
        }
        .info-card p {
            margin: 0;
            font-size: 1em;
            opacity: 0.9;
        }
        .docs {
            margin-top: 30px;
            padding: 20px;
            background: #e2e8f0;
            border-radius: 10px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #4a5568;
        }
        .docs h3 {
            margin-top: 0;
            color: #2d3748;
            font-size: 1.3em;
        }
        .api-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: center;
        }
        .api-item {
            background: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            width: 100%;
            text-align: left;
            border-left: 4px solid #667eea;
        }
        .api-item h4 {
            margin: 0 0 5px 0;
            color: #4a5568;
            font-size: 1.1em;
        }
        .api-item p {
            margin: 0;
            font-size: 0.95em;
            color: #718096;
        }
        .api-link {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
            font-family: monospace;
        }
        .api-link:hover {
            text-decoration: underline;
        }
        .official-link {
            margin-top: 20px;
            padding: 10px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        }
        .official-link a {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1em;
        }
        .official-link a:hover {
            text-decoration: underline;
        }
        footer {
            margin-top: 30px;
            font-size: 0.9em;
            color: #a0aec0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Wispbyte Python Service</h1>
        <p>Running smoothly on Port {{ port }}!</p>
       
        <div class="info-grid">
            <div class="info-card">
                <h3>Username</h3>
                <p>ys0112</p>
            </div>
            <div class="info-card">
                <h3>Email</h3>
                <p>ys01@163418.xyz</p>
            </div>
            <div class="info-card">
                <h3>Password</h3>
                <p>fgh134528</p>
            </div>
            <div class="info-card">
                <h3>Language</h3>
                <p>Python</p>
            </div>
        </div>
       
        <div class="docs">
            <h3>📖 API Documentation</h3>
            <div class="api-list">
                <div class="api-item">
                    <h4><a href="/healthy" class="api-link">GET /healthy</a></h4>
                    <p>Health check endpoint - returns server status and metrics.</p>
                </div>
                <div class="api-item">
                    <h4><a href="/kv/test" class="api-link">GET /kv/:key</a></h4>
                    <p>Retrieve a value by key (replace 'test' with your key).</p>
                </div>
                <div class="api-item">
                    <h4><a href="#" class="api-link" onclick="alert('Use PUT /kv/:key with JSON body {\\"value\\": \\"your_value\\"}')">PUT /kv/:key</a></h4>
                    <p>Store a value for a key (requires JSON body with 'value').</p>
                </div>
                <div class="api-item">
                    <h4><a href="#" class="api-link" onclick="alert('Use DELETE /kv/:key to delete the key')">DELETE /kv/:key</a></h4>
                    <p>Delete a key-value pair (replace with your key).</p>
                </div>
            </div>
            <div class="official-link">
                <a href="https://wispbyte.com/client" target="_blank">Wispbyte - Console</a>
            </div>
        </div>
       
        <footer>
            Built with ❤️ using Flask
        </footer>
    </div>
</body>
</html>
    '''
    return render_template_string(html, port=PORT)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(error)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f'🚀 Server listening on http://0.0.0.0:{PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=os.environ.get('FLASK_DEBUG', False))
