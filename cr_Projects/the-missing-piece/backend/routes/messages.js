// The Missing Piece - Messages Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/messages
  app.get('/api/messages', (req, res) => {
    const data = getData('messages.json', []);
    res.json(data);
  });

  // GET /api/messages/:id
  app.get('/api/messages/:id', (req, res) => {
    const data = getData('messages.json', []);
    const id = sanitizeInput(req.params.id);
    const msg = data.find(m => m.id === id);
    if (!msg) {
      return res.status(404).json({ error: 'Message not found' });
    }
    res.json(msg);
  });

  // POST /api/messages (admin)
  app.post('/api/messages', (req, res) => {
    const { text, author, messageId } = req.body;
    if (!text || !author) {
      return res.status(400).json({ error: 'Text and author are required' });
    }
    const data = getData('messages.json', []);
    const newMsg = {
      id: `msg_${Date.now()}`,
      text: sanitizeInput(text),
      author: sanitizeInput(author),
      messageId: messageId || '',
      createdAt: new Date().toISOString()
    };
    data.push(newMsg);
    writeData('messages.json', data);
    res.status(201).json(newMsg);
  });
};
