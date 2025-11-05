import express from 'express';
import pino from 'pino';
import os from 'node:os';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development' ? { target: 'pino-pretty' } : undefined,
});

const app = express();

// ========== 固定端口（优先环境，默认为 14273） ==========
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 14273;
logger.info(`✅ Fixed port: ${PORT} (set PORT env to override)`);

const kv = new Map();

app.use(express.json({ limit: '1mb' }));

app.use((req, res, next) => {
  logger.info({ method: req.method, url: req.url, ip: req.ip });
  next();
});

app.get('/healthz', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    loadavg: os.loadavg(),
    port: PORT,
  });
});

app.get('/kv/:key', (req, res) => {
  const { key } = req.params;
  const value = kv.get(key);
  if (value === undefined) return res.status(404).json({ error: 'Not found' });
  res.json({ key, value });
});

app.put('/kv/:key', (req, res) => {
  const { key } = req.params;
  const { value } = req.body;
  if (value === undefined) return res.status(400).json({ error: 'value required' });
  kv.set(key, value);
  res.json({ key, value });
});

app.delete('/kv/:key', (req, res) => {
  const { key } = req.params;
  kv.delete(key);
  res.json({ deleted: key });
});

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wispbyte Node.js Service</title>
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
            <h1>🚀 Wispbyte Node.js Service</h1>
            <p>Running smoothly on Port ${PORT}!</p>
            
            <div class="info-grid">
            <div class="info-card">
                    <h3>Username</h3>
                    <p>ys1234</p>
                </div>
                <div class="info-card">
                    <h3>Email</h3>
                    <p>ys@163418.xyz</p>
                </div>
                <div class="info-card">
                    <h3>Password</h3>
                    <p>fgh134528</p>
                </div>
                <div class="info-card">
                    <h3>Language</h3>
                    <p>Node.js</p>
                </div>
            </div>
            
            <div class="docs">
                <h3>📖 API Documentation</h3>
                <div class="api-list">
                    <div class="api-item">
                        <h4><a href="/healthz" class="api-link">GET /healthz</a></h4>
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
                Built with ❤️ using Express.js
            </footer>
        </div>
    </body>
    </html>
  `);
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.use((err, req, res, next) => {
  logger.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, '0.0.0.0', () => {
  logger.info(`🚀 Server listening on http://0.0.0.0:${PORT}`);
});
