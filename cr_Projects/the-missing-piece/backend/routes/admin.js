// The Missing Piece - Admin Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

const ADMIN_TOKEN = process.env.ADMIN_TOKEN || 'default-admin-token';

// Middleware to check admin auth
function adminAuth(req, res, next) {
  const token = req.headers['authorization'] || req.query.token || '';
  if (token !== ADMIN_TOKEN) {
    return res.status(403).json({ error: 'Access denied' });
  }
  next();
}

module.exports = (app) => {
  // DELETE /api/admin/messages/:id
  app.delete('/api/admin/messages/:id', adminAuth, (req, res) => {
    const data = getData('messages.json', []);
    const id = sanitizeInput(req.params.id);
    const filtered = data.filter(m => m.id !== id);
    if (filtered.length === data.length) {
      return res.status(404).json({ error: 'Message not found' });
    }
    writeData('messages.json', filtered);
    res.json({ ok: true });
  });

  // DELETE /api/admin/theories/:id
  app.delete('/api/admin/theories/:id', adminAuth, (req, res) => {
    const data = getData('theories.json', []);
    const id = sanitizeInput(req.params.id);
    const filtered = data.filter(t => t.id !== id);
    if (filtered.length === data.length) {
      return res.status(404).json({ error: 'Theory not found' });
    }
    writeData('theories.json', filtered);
    res.json({ ok: true });
  });

  // DELETE /api/admin/clues/:id
  app.delete('/api/admin/clues/:id', adminAuth, (req, res) => {
    const data = getData('clues.json', []);
    const id = sanitizeInput(req.params.id);
    const filtered = data.filter(c => c.id !== id);
    if (filtered.length === data.length) {
      return res.status(404).json({ error: 'Clue not found' });
    }
    writeData('clues.json', filtered);
    res.json({ ok: true });
  });

  // GET /api/admin/dashboard
  app.get('/api/admin/dashboard', adminAuth, (req, res) => {
    const stats = {
      messages: getData('messages.json', []).length,
      theories: getData('theories.json', []).length,
      clues: getData('clues.json', []).length,
      gallery: getData('gallery.json', []).length,
      lore: getData('lore.json', []).length,
      timeline: getData('timeline.json', []).length,
      characters: getData('characters.json', []).length,
      events: getData('events.json', []).length
    };
    res.json(stats);
  });
};