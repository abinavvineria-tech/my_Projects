// The Missing Piece - Stats Route
const fs = require('fs');
const path = require('path');
const { getData } = require('../utils/data');
const DATA_DIR = require('../utils/data').DATA_DIR;

module.exports = (app) => {
  app.get('/api/stats', (req, res) => {
    try {
      // Count files
      const files = fs.readdirSync(DATA_DIR);
      const jsonFiles = files.filter(f => f.endsWith('.json'));
      
      // Count items
      let totalItems = 0;
      const counts = {};
      
      for (const file of jsonFiles) {
        const filePath = path.join(DATA_DIR, file);
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        counts[file] = Array.isArray(data) ? data.length : Object.keys(data).length;
        totalItems += counts[file];
      }
      
      const stats = {
        server: 'online',
        storage: 'online',
        totalFiles: jsonFiles.length,
        totalItems: totalItems,
        itemsByCategory: counts,
        timestamp: new Date().toISOString()
      };
      
      res.json(stats);
    } catch (error) {
      res.status(500).json({
        error: 'Failed to get stats',
        details: error.message
      });
    }
  });
};