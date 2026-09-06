// The Missing Piece - Health Route
const { getData, writeData } = require('../utils/data');

module.exports = (app) => {
  // Health check endpoint
  app.get('/api/health', (req, res) => {
    try {
      // Check if server is running
      const health = {
        status: 'ok',
        server: 'online',
        storage: 'online',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      };
      res.json(health);
    } catch (error) {
      res.status(500).json({
        status: 'error',
        error: 'Health check failed',
        details: error.message
      });
    }
  });

  // Stats endpoint
  app.get('/api/stats', (req, res) => {
    try {
      const stats = {
        characters: getData('characters.json', { count: 0 }),
        events: getData('events.json', { count: 0 }),
        theories: getData('theories.json', { count: 0 }),
        clues: getData('clues.json', { count: 0 }),
        gallery: getData('gallery.json', { count: 0 }),
        messages: getData('messages.json', { count: 0 }),
        unlockedPieces: getData('puzzle.json', { count: 0 })
      };
      
      // Count total items across all JSON files
      const files = fs.readdirSync(DATA_DIR);
      const jsonFiles = files.filter(f => f.endsWith('.json'));
      
      stats.totalDataFiles = jsonFiles.length;
      
      // Count total items
      let totalItems = 0;
      for (const file of jsonFiles) {
        try {
          const data = JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'));
          if (Array.isArray(data)) {
            totalItems += data.length;
          } else if (typeof data === 'object' && data !== null) {
            totalItems += Object.keys(data).length;
          }
        } catch (e) {
          // Skip invalid files
        }
      }
      
      stats.totalItems = totalItems;
      
      res.json(stats);
    } catch (error) {
      res.status(500).json({
        error: 'Failed to get stats',
        details: error.message
      });
    }
  });

  // Admin routes (optional)
  app.use('/api/admin', require('./adminRoutes'));
  
  return app;
};