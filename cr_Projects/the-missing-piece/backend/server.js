// The Missing Piece - Main Server
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const path = require('path');
const fs = require('fs');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

// Import route modules (each registers routes on the express app)
const registerHealthRoutes = require('./routes/health');
const registerStatsRoutes = require('./routes/stats');
const registerCharactersRoutes = require('./routes/characters');
const registerEventsRoutes = require('./routes/events');
const registerTheoriesRoutes = require('./routes/theories');
const registerCluesRoutes = require('./routes/clues');
const registerGalleryRoutes = require('./routes/gallery');
const registerMessagesRoutes = require('./routes/messages');
const registerLoreRoutes = require('./routes/lore');
const registerTimelineRoutes = require('./routes/timeline');
const registerAdminRoutes = require('./routes/admin');

const app = express();
const HOST = process.env.HOST || '0.0.0.0';
const PORT = process.env.PORT || 8080;
const DATA_DIR = path.resolve(__dirname, '..', 'data');
const FRONTEND_DIR = path.resolve(__dirname, '..', 'frontend', 'build');
const PUBLIC_DIR = path.resolve(__dirname, '..', 'public');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Trust proxy for rate limiting behind reverse proxies
app.set('trust proxy', 1);

// Security middleware
app.use(helmet({
  contentSecurityPolicy: false, // Disabled for SPA flexibility
  crossOriginEmbedderPolicy: false
}));

// Compression
app.use(compression());

// CORS
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: false
}));

// Body parser
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));

// Logging
if (process.env.NODE_ENV !== 'production') {
  app.use(morgan('dev'));
} else {
  app.use(morgan('combined'));
}

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000,
  max: parseInt(process.env.RATE_LIMIT_MAX) || 100,
  message: { error: 'Too many requests, please try again later.' }
});
app.use('/api/', limiter);

// API Routes - register all route modules
registerCharactersRoutes(app);
registerEventsRoutes(app);
registerTheoriesRoutes(app);
registerCluesRoutes(app);
registerGalleryRoutes(app);
registerMessagesRoutes(app);
registerLoreRoutes(app);
registerTimelineRoutes(app);
registerHealthRoutes(app);
registerStatsRoutes(app);
registerAdminRoutes(app);

// Serve static files from public
app.use('/static', express.static(PUBLIC_DIR, {
  maxAge: '1d',
  setHeaders: (res) => {
    res.setHeader('Cache-Control', 'public, max-age=86400');
  }
}));

// Serve frontend build if exists
if (fs.existsSync(FRONTEND_DIR)) {
  app.use(express.static(FRONTEND_DIR, {
    maxAge: '1h'
  }));
}

// API root
app.get('/api', (req, res) => {
  res.json({
    name: 'The Missing Piece API',
    version: '1.0.0',
    endpoints: [
      '/api/characters',
      '/api/events',
      '/api/theories',
      '/api/clues',
      '/api/gallery',
      '/api/messages',
      '/api/lore',
      '/api/timeline',
      '/api/health',
      '/api/stats'
    ]
  });
});

// Catch-all: serve frontend index.html for SPA routing
app.get('*', (req, res) => {
  const indexPath = path.join(FRONTEND_DIR, 'index.html');
  if (fs.existsSync(indexPath)) {
    res.sendFile(indexPath);
  } else {
    // Fallback HTML if frontend not built
    res.send(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>The Missing Piece</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: Georgia, serif; background: linear-gradient(135deg, #2a1f3d, #4a3b5c); color: #f0e8f5; padding: 2rem; text-align: center; }
            h1 { font-size: 3rem; margin: 2rem 0; }
            .info { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 1rem; max-width: 600px; margin: 2rem auto; }
            a { color: #ffd6f5; }
          </style>
        </head>
        <body>
          <h1>🧩 The Missing Piece</h1>
          <div class="info">
            <p>"Every story has a piece that was lost…"</p>
            <p>API is running. Frontend build not found.</p>
            <p>Visit <a href="/api">/api</a> for endpoints.</p>
            <p>To build frontend: <code>cd frontend && npm install && npm run build</code></p>
          </div>
        </body>
      </html>
    `);
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found', path: req.path });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message
  });
});

// Start server
app.listen(PORT, HOST, () => {
  console.log(`\n🧩 The Missing Piece Server`);
  console.log(`   Listening on: http://${HOST}:${PORT}`);
  console.log(`   Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`   Data dir: ${DATA_DIR}`);
  console.log(`   🌸 Server online\n`);
});
