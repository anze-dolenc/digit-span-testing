const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const morgan = require('morgan');
const helmet = require('helmet');
const { v4: uuidv4 } = require('uuid');
const fileUpload = require('express-fileupload');
const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3');
const archiver = require('archiver');
const basicAuth = require('express-basic-auth');
require('dotenv').config();


const app = express();
const PORT = process.env.PORT || 3000;
const ENV = process.env.NODE_ENV || 'development';

// Middleware setup 
//app.use(helmet());
//app.use(cors());
app.use(bodyParser.json());
app.use(morgan(ENV === 'development' ? 'dev' : 'combined'));
app.use(fileUpload());

// Initialize SQLite database
const db = new sqlite3.Database('./database.sqlite', (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        db.run(`CREATE TABLE IF NOT EXISTS uploads (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            ip TEXT,
            username TEXT,
            group_name TEXT,
            file_name TEXT
        )`);
    }
});


app.post('/', (req, res) => {
    try{
    const file = req.files?.file;
    const username = req.body.username;
    const group = req.body.group;

    if (!file || !username || !group) {
        return res.status(400).json({ error: 'File, username and group are required' });
    }

    const id = uuidv4();
    const timestamp = new Date().toISOString().replace(/[:]/g, '-');
    const ip = req.ip;

    const uploadDir = path.join(__dirname, 'uploads');
    fs.mkdirSync(uploadDir, { recursive: true });

    const filePath = path.join(uploadDir, `${timestamp}-${file.name}`);
    console.log(`Saving file to: ${filePath}`);
    file.mv(filePath, (err) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to save file' });
        }

        db.run(
            `INSERT INTO uploads (id, timestamp, ip, username, group_name,file_name) VALUES (?, ?, ?, ?,?,?)`,
            [id, timestamp, ip, username, group, file.name],
            (err) => {
                if (err) {
                    console.error('Error inserting record into database:', err.message);
                    return res.status(500).json({ error: 'Failed to save record' });
                }

                res.json({ message: 'File uploaded successfully', id });
            }
        );
    });
}catch(error){
    console.error('Error handling upload:', error);
    res.status(500).json({ error: 'Internal server error' });   
}
});


app.use(basicAuth({
    users: { [process.env.LOGIN_USERNAME]: process.env.LOGIN_PASSWORD },
    challenge: true,
    unauthorizedResponse: (req) => 'Unauthorized'
}));

app.get('/', (req, res) => {
    const filePath = path.join(__dirname, 'index.html');
    res.sendFile(filePath, (err) => {
        if (err) {
            res.status(500).send('Error loading the HTML file');
        }
    });
});

app.get('/groups', (req, res) => {
    db.all(`SELECT DISTINCT group_name FROM uploads`, [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to fetch groups' });
        }
        res.json(rows.map(r => r.group_name));
    });
});

app.get('/download/:group', (req, res) => {
    const group = req.params.group;

    db.all(`SELECT id,timestamp,file_name FROM uploads WHERE group_name = ?`, [group], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to retrieve records' });
        }

        if (rows.length === 0) {
            return res.status(404).json({ error: 'No files found for the specified group' });
        }
        //console.log(`Preparing to download files for group: ${group}, number of files: ${rows.length}`);
        const archive = archiver('zip', { zlib: { level: 9 } });
        res.attachment(`${group}-files.zip`);

        archive.on('error', (err) => {
            res.status(500).send({ error: 'Failed to create archive' });
        });

        archive.pipe(res);

        rows.forEach((row) => {
            const filePath = path.join(__dirname, 'uploads', `${row.timestamp}-${row.file_name}`);
            //console.log(`Adding file to archive: ${filePath}-${row.file_name}`);
            if (fs.existsSync(filePath)) {
                archive.file(filePath, { name: path.basename(filePath) });
            }
        });

        archive.finalize();
    });
});



app.listen(PORT, () => {
    console.log(`Server is running in ${ENV} mode on port ${PORT}`);
});

