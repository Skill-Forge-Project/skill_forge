const express = require('express');
// const { runUnitTests } = require('./unitTestRunner');

const app = express();
const PORT = 3000;

app.use(express.json());

app.post('/execute', (req, res) => {
    const { code, unitTests } = req.body;

    // Execute JavaScript code
    eval(code);

    // Run unit tests
    const testResults = runUnitTests(code, unitTests);

    res.json({ testResults });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});