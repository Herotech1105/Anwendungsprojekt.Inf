require('dotenv').config(); // use .env file
const mariadb = require('mariadb');
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json()); 


// middleware - authenticate API-key
const authenticateApiKey = (req, res, next) => {
    const apiKey = req.header('x-api-key');

    if (!apiKey || apiKey !== process.env.API_KEY) {
        return res.status(401).json({ error: "Non authorised API-key" });
    }
    
    next(); 
};

app.use(express.static('public'));

// get status of server
app.get('/api/status', (req, res) => {
    res.json({ status: 'online', timestamp: new Date() });
});

app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});

//SQL Statements // ---------------------------------------- //

// Pool configuration
const pool = mariadb.createPool({
     host: 'maria.local', 
     user: 'db_write_user', 
     password: 'password',
     database: 'password',
     connectionLimit: 5
});

// @Post: save sensordata into database
app.post('/api/internal/sensordata', authenticateApiKey, async (req, res) => {
    // validate data
    const { temperature, humidity, timestamp} = validateSensorPayload; 

    let conn;
    try {
        // connect to the database
        conn = await pool.getConnection();
        
        // Prepared Statement
        const sql = "INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)";
        const result = await conn.query(sql, [temperature, humidity, timestamp]);

        res.status(201).json({ 
            status: "ok", inserted
        });
    } catch (err) {
        res.status(400).json({ error: err.message || "invalid payload"});
    } finally {
        if (conn) conn.release();
    }
});


// @function: validating the payload for the sensor_data table
validateSensorPayload = (data) => {
    const { temperature, humidity, timestamp } = data;

    // check if temperature and humidity are numbers
    if(isNaN(temperature || isNaN(humidity))){
        return null;
    }

    // check if timestamp is valid
    const date = new Date(timestamp);
    if(!(date instanceof Date && !isNaN(date.getTime()))){
        return null;
    }

    // check if temperature and humidity are in valid ranges
    if(temperature < 0 || temperature > 60 || humidity < 10 || humidity > 70){
        return null;
    }

    // check if timestamp is still up-to-date
    const currentDate = new Date();
    const minuteDifference = Math.floor((currentDate - date) / 6000);
    if(minuteDifference < -5 || minuteDifference > 60){
        return null;
    }
    
    // return valid data
    return (temperature, humidity, temperature);
}
