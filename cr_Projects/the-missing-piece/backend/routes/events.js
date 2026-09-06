// The Missing Piece - Events Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/events
  app.get('/api/events', (req, res) => {
    const data = getData('events.json', []);
    res.json(data);
  });

  // GET /api/events/:id
  app.get('/api/events/:id', (req, res) => {
    const data = getData('events.json', []);
    const id = sanitizeInput(req.params.id);
    const event = data.find(e => e.id === id);
    if (!event) {
      return res.status(404).json({ error: 'Event not found' });
    }
    res.json(event);
  });

  // POST /api/events (admin)
  app.post('/api/events', (req, res) => {
    const { title, description, episode, date, characters } = req.body;
    if (!title) {
      return res.status(400).json({ error: 'Title is required' });
    }
    const data = getData('events.json', []);
    const newEvent = {
      id: `event_${Date.now()}`,
      title: sanitizeInput(title),
      description: sanitizeInput(description || ''),
      episode: sanitizeInput(episode || ''),
      date: sanitizeInput(date || ''),
      characters: Array.isArray(characters) ? characters.map(sanitizeInput) : [],
      createdAt: new Date().toISOString()
    };
    data.push(newEvent);
    writeData('events.json', data);
    res.status(201).json(newEvent);
  });
};