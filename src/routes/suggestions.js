const express = require('express');
const router = express.Router();
const { suggestions, comments } = require('../data/db');

router.get('/:id', (req, res) => {
  const suggestionId = parseInt(req.params.id, 10);
  const suggestion = suggestions.find(s => s.id === suggestionId);

  if (!suggestion) {
    return res.status(404).send('Suggestion not found');
  }

  const suggestionComments = comments.filter(c => c.suggestionId === suggestionId);

  res.json({
    ...suggestion,
    comments: suggestionComments,
  });
});

module.exports = router;
