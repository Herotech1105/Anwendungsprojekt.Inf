require('dotenv').config(); // use .env file
const DB_HOST = process.env.DB_HOST
const DB_WRITE_USER = process.env.DB_WRITE_USER
const DB_WRITE_PASSWORD = process.env.DB_WRITE_PASSWORD
const DB_READ_USER = process.env.DB_READ_USER
const DB_READ_PASSWORD = process.env.DB_READ_PASSWORD
const DB_NAME = process.env.DB_NAME
let readPool;
let writePool;

async function getWritePool() {
    if (!writePool) {
        const mariadb = await import('mariadb');
        pool = mariadb.createPool({
            host: DB_HOST,
            user: DB_WRITE_USER,
            password: DB_WRITE_PASSWORD,
            database: DB_NAME,
            connectionLimit: 5
        });
    }
    return writePool;
}

async function getReadPool() {
    if (!readPool) {
        const mariadb = await import('mariadb');
        pool = mariadb.createPool({
            host: DB_HOST,
            user: DB_READ_USER,
            password: DB_READ_PASSWORD,
            database: DB_NAME,
            connectionLimit: 5
        });
    }
    return readPool;
}

module.exports = { getWritePool, getReadPool };

