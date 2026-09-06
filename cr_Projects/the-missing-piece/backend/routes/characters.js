// The Missing Piece - Characters Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/characters
  app.get('/api/characters', (req, res) => {
    const data = getData('characters.json', []);
    res.json(data);
  });

  // GET /api/characters/:id
  app.get('/api/characters/:id', (req, res) => {
    const data = getData('characters.json', []);
    const id = sanitizeInput(req.params.id);
    const char = data.find(c => c.id === id || c.name === id);
    if (!char) {
      return res.status(404).json({ error: 'Character not found' });
    }
    res.json(char);
  });

  // POST /api/characters (admin)
  app.post('/api/characters', (req, res) => {
    const { name, description, category, status } = req.body;
    if (!name) {
      return res.status(400).json({ error: 'Name is required' });
    }
    const data = getData('characters.json', []);
    const newChar = {
      id: `char_${Date.now()}`,
      name: sanitizeInput(name),
      description: sanitizeInput(description || ''),
      category: sanitizeInput(category || 'character'),
      status: sanitizeInput(status || 'confirmed'),
      createdAt: new Date().toISOString()
    };
    data.push(newChar);
    writeData('characters.json', data);
    res.status(201).json(newChar);
  });
};