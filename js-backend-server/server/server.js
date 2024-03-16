const http = require('http');
const { exec } = require('child_process');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();

// Use body-parser middleware to parse JSON requests
app.use(bodyParser.json());

// Endpoint to execute JavaScript code
app.post('/execute', (req, res) => {
  const { code } = req.body;

  // Execute the JavaScript code
  exec(`node -e "${code}"`, (error, stdout, stderr) => {
    if (error) {
      res.status(500).json({ error: error.message });
      return;
    }
    if (stderr) {
      res.status(400).json({ error: stderr });
      return;
    }
    res.json({ result: stdout });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});