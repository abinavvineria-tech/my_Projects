// The Missing Piece - Timeline Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/timeline
  app.get('/api/timeline', (req, res) => {
    const data = getData('timeline.json', []);
    // Filter by type if provided
    let result = data;
    if (req.query.type) {
      const type = sanitizeInput(req.query.type);
      result = data.filter(e => e.type && e.type.toLowerCase() === type.toLowerCase());
    }
    // Sort by date if provided
    if (req.query.sort === 'date') {
      result = [...result].sort((a, b) => {
        return new Date(a.date || '1970-01-01') - new Date(b.date || '1970-01-01');
      });
    }
    res.json(result);
  });

  // GET /api/timeline/:id
  app.get('/api/timeline/:id', (req, res) => {
    const data = getData('timeline.json', []);
    const id = sanitizeInput(req.params.id);
    const event = data.find(e => e.id === id);
    if (!event) {
      return res.status(404).json({ error: 'Timeline event not found' });
    }
    res.json(event);
  });

  // POST /api/timeline (admin)
  app.post('/api/timeline', (req, res) => {
    const { title, description, date, episode, type, characters } = req.body;
    if (!title || !description || !date) {
      return res.status(400).json({ error: 'Title, description, and date are required' });
    }
    const data = getData('timeline.json', []);
    const newEvent = {
      id: `timeline_${Date.now()}`,
      title: sanitizeInput(title),
      description: sanitizeInput(description),
      date: sanitizeInput(date),
      episode: sanitizeInput(episode || ''),
      type: sanitizeInput(type || 'event'),
      characters: Array.isArray(characters) ? characters.map(sanitizeInput) : [],
      createdAt: new Date().toISOString()
    };
    data.push(newEvent);
    writeData('timeline.json', data);
    res.status(201).json(newEvent);
  });
};