// The Missing Piece - Clues Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/clues
  app.get('/api/clues', (req, res) => {
    const data = getData('clues.json', []);
    // Filter by status if provided
    let result = data;
    if (req.query.status) {
      const status = sanitizeInput(req.query.status);
      result = data.filter(c => c.status && c.status.toLowerCase() === status.toLowerCase());
    }
    res.json(result);
  });

  // GET /api/clues/:id
  app.get('/api/clues/:id', (req, res) => {
    const data = getData('clues.json', []);
    const id = sanitizeInput(req.params.id);
    const clue = data.find(c => c.id === id);
    if (!clue) {
      return res.status(404).json({ error: 'Clue not found' });
    }
    res.json(clue);
  });

  // POST /api/clues (admin)
  app.post('/api/clues', (req, res) => {
    const { title, description, evidence, status, relatedCharacter, relatedEvent, number } = req.body;
    if (!title || !description) {
      return res.status(400).json({ error: 'Title and description are required' });
    }
    const data = getData('clues.json', []);
    const newClue = {
      id: `clue_${Date.now()}`,
      title: sanitizeInput(title),
      description: sanitizeInput(description),
      evidence: Array.isArray(evidence) ? evidence.map(sanitizeInput) : [],
      status: sanitizeInput(status || 'unknown'),
      relatedCharacter: sanitizeInput(relatedCharacter || ''),
      relatedEvent: sanitizeInput(relatedEvent || ''),
      number: sanitizeInput(number || ''),
      createdAt: new Date().toISOString()
    };
    data.push(newClue);
    writeData('clues.json', data);
    res.status(201).json(newClue);
  });

  // POST /api/clues/:id/like
  app.post('/api/clues/:id/like', (req, res) => {
    const data = getData('clues.json', []);
    const id = sanitizeInput(req.params.id);
    const clue = data.find(c => c.id === id);
    if (!clue) {
      return res.status(404).json({ error: 'Clue not found' });
    }
    clue.likeCount = (clue.likeCount || 0) + 1;
    writeData('clues.json', data);
    res.json({ id: clue.id, likeCount: clue.likeCount });
  });
};