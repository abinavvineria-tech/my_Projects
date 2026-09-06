// The Missing Piece - Theories Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/theories
  app.get('/api/theories', (req, res) => {
    const data = getData('theories.json', []);
    // Filter by status if provided
    let result = data;
    if (req.query.status) {
      const status = sanitizeInput(req.query.status);
      result = data.filter(t => t.status && t.status.toLowerCase() === status.toLowerCase());
    }
    // Filter by character if provided
    if (req.query.character) {
      const char = sanitizeInput(req.query.character);
      result = result.filter(t => t.relatedCharacters && t.relatedCharacters.includes(char));
    }
    res.json(result);
  });

  // GET /api/theories/:id
  app.get('/api/theories/:id', (req, res) => {
    const data = getData('theories.json', []);
    const id = sanitizeInput(req.params.id);
    const theory = data.find(t => t.id === id);
    if (!theory) {
      return res.status(404).json({ error: 'Theory not found' });
    }
    res.json(theory);
  });

  // POST /api/theories (admin)
  app.post('/api/theories', (req, res) => {
    const { title, description, evidence, counterpoints, relatedCharacters, relatedEpisodes, status, communityInterest } = req.body;
    if (!title || !description) {
      return res.status(400).json({ error: 'Title and description are required' });
    }
    const data = getData('theories.json', []);
    const newTheory = {
      id: `theory_${Date.now()}`,
      title: sanitizeInput(title),
      description: sanitizeInput(description),
      evidence: Array.isArray(evidence) ? evidence.map(sanitizeInput) : [],
      counterpoints: Array.isArray(counterpoints) ? counterpoints.map(sanitizeInput) : [],
      relatedCharacters: Array.isArray(relatedCharacters) ? relatedCharacters.map(sanitizeInput) : [],
      relatedEpisodes: Array.isArray(relatedEpisodes) ? relatedEpisodes.map(sanitizeInput) : [],
      status: sanitizeInput(status || 'theory'),
      communityInterest: 0,
      createdAt: new Date().toISOString()
    };
    data.push(newTheory);
    writeData('theories.json', data);
    res.status(201).json(newTheory);
  });

  // POST /api/theories/:id/like
  app.post('/api/theories/:id/like', (req, res) => {
    const data = getData('theories.json', []);
    const id = sanitizeInput(req.params.id);
    const theory = data.find(t => t.id === id);
    if (!theory) {
      return res.status(404).json({ error: 'Theory not found' });
    }
    theory.communityInterest = (theory.communityInterest || 0) + 1;
    writeData('theories.json', data);
    res.json({ id: theory.id, communityInterest: theory.communityInterest });
  });
};