require('dotenv').config(); // use .env file
const HOST = process.env.PORT || 3000;
const DB_HOST = process.env.DB_HOST
const DB_USER = process.env.DB_USER
const DB_PASSWORD = process.env.DB_PASSWORD
const DB_NAME = process.env.DB_NAME
let pool;

async function getPool() {
    if (!pool) {
        // Hier ist der dynamische Import
        const mariadb = await import('mariadb');
        pool = mariadb.createPool({
            host: DB_HOST,
            user: DB_USER,
            password: DB_PASSWORD,
            database: DB_NAME,
            connectionLimit: 5
        });
    }
    return pool;
}

module.exports = { getPool };

