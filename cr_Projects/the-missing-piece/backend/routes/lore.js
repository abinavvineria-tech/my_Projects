// The Missing Piece - Lore Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/lore
  app.get('/api/lore', (req, res) => {
    const data = getData('lore.json', []);
    // Filter by category if provided
    let result = data;
    if (req.query.category) {
      const cat = sanitizeInput(req.query.category);
      result = data.filter(l => l.category && l.category.toLowerCase() === cat.toLowerCase());
    }
    res.json(result);
  });

  // GET /api/lore/:id
  app.get('/api/lore/:id', (req, res) => {
    const data = getData('lore.json', []);
    const id = sanitizeInput(req.params.id);
    const entry = data.find(l => l.id === id);
    if (!entry) {
      return res.status(404).json({ error: 'Lore entry not found' });
    }
    res.json(entry);
  });

  // POST /api/lore (admin)
  app.post('/api/lore', (req, res) => {
    const { name, description, category, relatedEntries, status, notes } = req.body;
    if (!name || !description) {
      return res.status(400).json({ error: 'Name and description are required' });
    }
    const data = getData('lore.json', []);
    const newEntry = {
      id: `lore_${Date.now()}`,
      name: sanitizeInput(name),
      description: sanitizeInput(description),
      category: sanitizeInput(category || 'general'),
      relatedEntries: Array.isArray(relatedEntries) ? relatedEntries.map(sanitizeInput) : [],
      status: sanitizeInput(status || 'confirmed'),
      notes: sanitizeInput(notes || ''),
      createdAt: new Date().toISOString()
    };
    data.push(newEntry);
    writeData('lore.json', data);
    res.status(201).json(newEntry);
  });
};
