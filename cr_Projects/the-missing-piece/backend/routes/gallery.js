// The Missing Piece - Gallery Route
const { getData, writeData, sanitizeInput } = require('../utils/data');

module.exports = (app) => {
  // GET /api/gallery
  app.get('/api/gallery', (req, res) => {
    const data = getData('gallery.json', []);
    res.json(data);
  });

  // GET /api/gallery/:id
  app.get('/api/gallery/:id', (req, res) => {
    const data = getData('gallery.json', []);
    const id = sanitizeInput(req.params.id);
    const galleryItem = data.find(g => g.id === id);
    if (!galleryItem) {
      return res.status(404).json({ error: 'Gallery item not found' });
    }
    res.json(galleryItem);
  });

  // POST /api/gallery (admin)
  app.post('/api/gallery', (req, res) => {
    const { title, description, category, tags, imageUrl } = req.body;
    if (!title || !imageUrl) {
      return res.status(400).json({ error: 'Title and image URL are required' });
    }
    const data = getData('gallery.json', []);
    const newItem = {
      id: `gallery_${Date.now()}`,
      title: sanitizeInput(title),
      description: sanitizeInput(description || ''),
      category: sanitizeInput(category || 'art'),
      tags: Array.isArray(tags) ? tags.map(sanitizeInput) : [],
      imageUrl: sanitizeInput(imageUrl),
      createdAt: new Date().toISOString()
    };
    data.push(newItem);
    writeData('gallery.json', data);
    res.status(201).json(newItem);
  });

  // POST /api/gallery/:id/like
  app.post('/api/gallery/:id/like', (req, res) => {
    const data = getData('gallery.json', []);
    const id = sanitizeInput(req.params.id);
    const item = data.find(g => g.id === id);
    if (!item) {
      return res.status(404).json({ error: 'Gallery item not found' });
    }
    item.likeCount = (item.likeCount || 0) + 1;
    writeData('gallery.json', data);
    res.json({ id: item.id, likeCount: item.likeCount });
  });
};