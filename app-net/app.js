const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json()); 

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.send('<h1>Hello, World!</h1>');
});

// Example API route
app.get('/api/status', (req, res) => {
    res.json({ status: 'online', timestamp: new Date() });
});

app.listen(PORT, () => {
    console.log(`🚀 Server listening at http://localhost:${PORT}`);
});