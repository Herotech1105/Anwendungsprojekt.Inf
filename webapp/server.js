// server.js

require('dotenv').config(); // use .env file
const express = require('express');
const app = express();
const {getReadPool, getWritePool, getAdminPool} = require('./config/database');
const PORT = process.env.PORT || 3000;
const https = require('https');

app.use(express.json());

const cors = require("cors");

app.use(cors({
    origin: [
        "https://192.168.4.18",
        "https://www.lab.local",
        "https://local.kleber.data"
    ],
    credentials: true
}));

const {authenticateToken, authenticateApiKey} = require("./service/authentication")

app.use(express.static("public"));

app.set('trust proxy', true);

// get status of server
app.get('/api/status', (req, res) => {
    console.log("Getting Status ...")
    res.json({status: 'online', timestamp: new Date()});
});

const fs = require('fs');
const {validateSensorPayload} = require("./service/validateSensorPayload");

const privateKey = fs.readFileSync('certs/server.key');
const certificate = fs.readFileSync('certs/server.crt');

const credentials = {key: privateKey, cert: certificate};

https.createServer(credentials, app).listen(PORT)

//SQL Statements // ------------------------------------------------------------- //

// @Post: save sensordata into database
app.post('/api/internal/sensordata', authenticateApiKey, async (req, res) => {
    // validate data
    console.log("Receiving sensor data ...")
    const {temperature, humidity, timestamp} = validateSensorPayload(req.body);

    let conn;
    try {
        if (!temperature) throw Error("Denied: ")
        const pool = await getWritePool();
        conn = await pool.getConnection();
        console.log("Connection to mariaDB established")

        // Prepared Statement
        const sql = "INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)";
        const result = await conn.query(sql, [temperature, humidity, timestamp]);

        console.log("Execution: ", result)
        res.status(201).json({
            status: "ok"
        });
    } catch (err) {
        res.status(400).json({error: err.message || "invalid payload"});
    } finally {
        if (conn) conn.release();
    }
});


// For dashboard chart
app.get('/api/sensordata', authenticateToken("dashboard-client", "dashboard-user"), async (req, res) => {
    let conn;
    try {
        const pool = await getReadPool();
        conn = await pool.getConnection();

        // Fetch the most recent sensor entry
        const sql = "SELECT * FROM sensor_data ORDER BY timestamp DESC";
        const rows = await conn.query(sql);

        if (rows.length === 0) {
            return res.status(200).json({message: "No data available."});
        }
        res.status(200).json(rows[0]);
    } catch (err) {
        res.status(500).json({error: err.message});
    } finally {
        if (conn) conn.release();
    }
});

// For dashboard chart
app.get('/api/sensordata/range', authenticateToken("dashboard-client", "dashboard-user"), async (req, res) => {
    const { from, to } = req.query;

    if (!from || !to) {
        return res.status(400).json({ error: "from and to parameters required" });
    }

    const fromStamp = new Date(from).toISOString().slice(0, 19).replace('T', ' ')
    const toStamp = new Date(to).toISOString().slice(0, 19).replace('T', ' ')

    let conn;
    try {
        const pool = await getReadPool();
        conn = await pool.getConnection();

        const sql = `
            SELECT timestamp, temperature, humidity
            FROM sensor_data
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        `;
        const rows = await conn.query(sql, [fromStamp, toStamp]);

        const labels = rows.map(r => r.timestamp);
        const temperatures = rows.map(r => r.temperature);
        const humidities = rows.map(r => r.humidity);

        res.json({ labels, temperatures, humidities });

    } catch (err) {
        res.status(500).json({ error: err.message });
    } finally {
        if (conn) conn.release();
    }
});

// Formatting for csv
function toCsvField(v) {
    if (v === null || v === undefined) return '';
    if (v instanceof Date) v = v.toISOString().slice(0, 19).replace('T', ' ');
    const s = String(v);
    // Fields with Comma, Apostrophes or linebreaks have to be quoted
    if (/[",\n\r]/.test(s)) {
        return `"${s.replace(/"/g, '""')}"`;
    }
    return s;
}

// For dashboard data export
app.get('/api/admin/export',
    authenticateToken("dashboard-client", "admin-user"),
    async (req, res) => {
        let conn;
        try {
            const pool = await getAdminPool();
            conn = await pool.getConnection();

            const filename = `myapp_export_${new Date().toISOString().slice(0, 10)}.csv`;
            res.setHeader('Content-Type', 'text/csv; charset=utf-8');
            res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);

            const tables = ['sensor_data', 'sensor_data_archive'];
            const columns = ['id', 'timestamp', 'temperature', 'humidity'];

            // Header: columns + origin table
            res.write(['source_table', ...columns].map(toCsvField).join(',') + '\r\n');

            for (const table of tables) {
                const rows = await conn.query(
                    `SELECT ${columns.join(', ')} FROM \`${table}\` ORDER BY id ASC`
                );
                for (const row of rows) {
                    const fields = [table, ...columns.map(c => row[c])];
                    res.write(fields.map(toCsvField).join(',') + '\r\n');
                }
            }
            res.end();
        } catch (err) {
            if (!res.headersSent) res.status(500).json({error: err.message});
            else res.end();
        } finally {
            if (conn) conn.release();
        }
    });