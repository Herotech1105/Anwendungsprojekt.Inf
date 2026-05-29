require('dotenv').config(); // use .env file
const express = require('express');
const app = express();
const {getReadPool, getWritePool} = require('./config/database');
const PORT = process.env.PORT || 3000;
const https = require('https');

app.use(express.json());

// middleware - JWKS client configuration
const jwksClient = require('jwks-rsa');
const jwt = require('jsonwebtoken');

const KC_JWKS_URI = process.env.KC_JWKS_URI;
const KC_BASE_URL = process.env.KC_BASE_URL;

const client = jwksClient({
    jwksUri: KC_JWKS_URI,
    requestAgent: new https.Agent({
    ca: undefined, // to do: add CA certificate
    rejectUnauthorized: true,
    }),
});
// retrieve signing key for JWT verification
const getKey = (header, callback) => {
    client.getSigningKey(header.kid, (err, key) => {
        if (err) {
            return callback(err);
        }
        const signingKey = key.getPublicKey();
        callback(null, signingKey);
    });
};

// middleware - authenticate token
const authenticateToken = (expectedAudience, requiredRole) => 
    { return (req, res, next) => {
        const authHeader = req.headers.authorization || "";
        // check if the authorization header is present and starts with "Bearer "
        if (!authHeader.startsWith("Bearer ")) {
            return res.sendStatus(401);
        }

        // extract the token from the header
        const token = authHeader.split(" ")[1];
        // check if the token is provided
        if (!token) {
            return res.status(401).json({ error: "No token provided" });
        }

        // options for token validation
        const validationOptions = {
            algorithms: ["RS256"],
            issuer: `${KC_BASE_URL}/realms/iot`,
        }
        // verify provided token
        jwt.verify(token, getKey, validationOptions, (err, decodedPayload) => {
            // if token verification fails, return 403 Forbidden
            if (err) {
                console.error("token verification failed");
                return res.status(403).json({ 
                    error: "Forbidden", 
                    message: "Token verification failed (signature, expiration date or issuer invalid)." 
                });
            }

            // retrieve the audience and authorized party from payload
            const aud = decodedPayload.aud;
            const azp = decodedPayload.azp;

            // check if the audience matches the expected audience
            const audienceOk = 
                (azp === expectedAudience) || 
                (typeof aud === 'string' && aud === expectedAudience) || 
                (Array.isArray(aud) && aud.includes(expectedAudience));

            // if required audience is missing, return 403 Forbidden
            if (!audienceOk) {
                console.error(`Audience"${expectedAudience}" is missing`);
                return res.status(403).json({ error: `Audience"${expectedAudience}" is missing` });
            }

            // retrieve roles from payload
            const roles = decodedPayload.realm_access?.roles || [];
            // check if required user role is provided
            if (requiredRole && !roles.includes(requiredRole)) {
                console.error(`Role ${requiredRole} is required`);
                return res.status(403).json({ error: `Role ${requiredRole} is required` });
            }


            // continue if token is valid
            req.user = decodedPayload;
            next();
        });
    }
}

// middleware - authenticate API-key
const authenticateApiKey = (req, res, next) => {
    const apiKey = req.header('x-api-key');

    if (!apiKey || apiKey !== process.env.API_KEY) {
        return res.status(401).json({error: "Non authorised API-key"});
    }

    next();
};

app.use(express.static("public"));

app.set('trust proxy', true);

// get status of server
app.get('/api/status', (req, res) => {
    console.log("Getting Status ...")
    res.json({status: 'online', timestamp: new Date()});
});

const fs = require('fs');

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

app.post('/api/internal/trainingdata', authenticateApiKey, async (req, res) => {
    // validate data
    console.log("Saving training_data")
    const {temperature, humidity, timestamp, heater, fan} = validateSensorPayload(req.body);

    let conn;
    try {
        if (!temperature) throw Error("Denied: ")
        const pool = await getWritePool();
        conn = await pool.getConnection();
        console.log("Connection to mariaDB established")

        // Prepared Statement
        const sql = "INSERT INTO training_data (temperature, humidity, timestamp, heater, fan) VALUES (?, ?, ?, ?, ?)";
        const result = await conn.query(sql, [temperature, humidity, timestamp, heater, fan]);

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

// For Controller Warmstart
app.get('/api/internal/sensordata/latest', 
    authenticateApiKey, 
    authenticateToken("here the audience", "controller-access"), 
    async (req, res) => {
        let conn;
        try {
            const pool = await getReadPool();
            conn = await pool.getConnection();

            // Fetch the most recent sensor entry
            const sql = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1";
            const rows = await conn.query(sql);

            if (rows.length === 0) {
                return res.status(200).json({message: "No data available yet."});
            }
            res.status(200).json(rows[0]);
        } catch (err) {
            res.status(500).json({error: err.message});
        } finally {
            if (conn) conn.release();
        }
});


// For Dashboard chart
app.get('/api/sensordata', authenticateToken("dashboard-audience", "dashboard-user"), async (req, res) => {
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


app.get('/api/sensordata/range', authenticateToken, async (req, res) => {
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


// @function: validating the payload for the sensor_data table
validateSensorPayload = (data) => {
    const {temperature, humidity, timestamp, heater, fan} = data;

    // check if temperature and humidity are numbers
    if (isNaN(temperature) || isNaN(humidity)) {
        console.error("Temperature and humidity must be numbers");
        return null;
    }

    // check if timestamp is valid
    const date = new Date(timestamp);
    if (!(date instanceof Date && !isNaN(date.getTime()))) {
        console.error("Invalid timestamp");
        return null;
    }

    // check if temperature and humidity are in valid ranges
    if (temperature < 0 || temperature > 60 || humidity < 10 || humidity > 70) {
        console.error("Temperature or humidity out of valid range");
        return null;
    }

    // check if timestamp is up-to-date
    const currentDate = new Date();
    const minuteDifference = Math.floor((currentDate - date) / 60000);
    if (minuteDifference < -5 || minuteDifference > 60) {
        console.error("Timestamp is not up-to-date");
        return null;
    }


    // Source - https://stackoverflow.com/a/11150727
    const formated_timestamp = date.toISOString().slice(0, 19).replace('T', ' ')

    // return valid data
    return {
        temperature,
        humidity,
        timestamp: formated_timestamp,
        heater,
        fan
    };
}
