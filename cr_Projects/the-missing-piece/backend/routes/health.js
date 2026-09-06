// The Missing Piece - Health Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // Health check endpoint
  app.get('/api/health', (req, res) => {
    res.json({
      status: 'ok',
      server: 'online',
      storage: 'online',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      uptime: process.uptime()
    });
  });
};