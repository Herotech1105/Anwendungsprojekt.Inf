require('dotenv').config(); // use .env file
const express = require('express');
const app = express();
const {getPool} = require('./config/database');
const PORT = process.env.PORT || 3000;

app.use(express.json());


// middleware - authenticate API-key
const authenticateApiKey = (req, res, next) => {
    const apiKey = req.header('x-api-key');

    if (!apiKey || apiKey !== process.env.API_KEY) {
        return res.status(401).json({error: "Non authorised API-key"});
    }

    next();
};

app.use(express.static('public'));

app.set('trust proxy', true);

// get status of server
app.get('/api/status', (req, res) => {
    res.json({status: 'online', timestamp: new Date()});
});

app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});

//SQL Statements // ------------------------------------------------------------- //

// @Post: save sensordata into database
app.post('/api/internal/sensordata', authenticateApiKey, async (req, res) => {
    // validate data
    const {temperature, humidity, timestamp} = validateSensorPayload(req.body);

    let conn;
    try {
        const pool = await getPool();
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


// @function: validating the payload for the sensor_data table
validateSensorPayload = (data) => {
    const {temperature, humidity, timestamp} = data;

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
    if (temperature < 0 || temperature > 100 || humidity < 0 || humidsity > 100) {
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
        temperature, humidity, formated_timestamp
    };
}
