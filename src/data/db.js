const suggestions = [
  { id: 1, title: 'Add a dark mode', body: 'It would be great to have a dark mode for the app.' },
  { id: 2, title: 'Improve search functionality', body: 'The search is a bit slow and could be improved.' },
  { id: 3, title: 'Export to PDF', body: 'Users should be able to export their data to PDF.' },
];

const comments = [
  { id: 1, suggestionId: 1, text: 'Yes, please! My eyes hurt at night.' },
  { id: 2, suggestionId: 1, text: 'I agree, this is a must-have feature.' },
  { id: 3, suggestionId: 2, text: 'I have also noticed the search is slow.' },
];

module.exports = {
  suggestions,
  comments,
};
