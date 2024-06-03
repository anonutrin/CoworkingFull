const express = require('express');
const path = require('path');
const app = express();
const port = 8026;
const https = require('https');
const fs = require('fs');
const cors = require('cors');

const debug = true;

const privateKeyPath = '/etc/letsencrypt/live/allrenda.ru/privkey.pem';
const certificatePath = '/etc/letsencrypt/live/allrenda.ru/fullchain.pem';

app.use(cors());
app.use(express.static(path.join(__dirname, 'build')));
app.use(express.static(path.join(__dirname, 'release'), {
    setHeaders: (res, filePath) => {
        if (filePath.endsWith('.js')) {
            res.setHeader('Content-Type', 'text/javascript');
        }
    }
}));

app.get('/map', (req, res) => {
    res.sendFile(path.join(__dirname, 'release', 'map.html'));
});

app.use((req, res, next) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});


if (debug) {
    app.listen(port, () => {
        console.log(`Express app is running on port ${port}`);
    });
} else {
    https.createServer({
      key: fs.readFileSync(privateKeyPath),
      cert: fs.readFileSync(certificatePath),
    }, app).listen(port, () => {
      console.log(`Express app is running on port ${port}`);
    });
}
