const express = require('express');
const app = express();
const port = 3000;
const suggestionsRouter = require('./routes/suggestions');

app.use('/suggestions', suggestionsRouter);

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
