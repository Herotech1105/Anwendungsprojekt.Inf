// config/database.js

require('dotenv').config(); // use .env file
const DB_HOST = process.env.DB_HOST
const DB_WRITE_USER = process.env.DB_WRITE_USER
const DB_WRITE_PASSWORD = process.env.DB_WRITE_PASSWORD
const DB_READ_USER = process.env.DB_READ_USER
const DB_READ_PASSWORD = process.env.DB_READ_PASSWORD
const DB_ADMIN_USER = process.env.DB_ADMIN_USER
const DB_ADMIN_PASSWORD = process.env.DB_ADMIN_PASSWORD
const DB_NAME = process.env.DB_NAME
let readPool;
let writePool;
let adminPool;

// Lazy Initialization (Only creates when needed) for writePool
async function getWritePool() {
    if (!writePool) {
        const mariadb = await import('mariadb');
        writePool = mariadb.createPool({
            host: DB_HOST,
            user: DB_WRITE_USER,
            password: DB_WRITE_PASSWORD,
            database: DB_NAME,
            connectionLimit: 5
        });
    }
    return writePool;
}

// Lazy Initialization for readPool
async function getReadPool() {
    if (!readPool) {
        const mariadb = await import('mariadb');
        readPool = mariadb.createPool({
            host: DB_HOST,
            user: DB_READ_USER,
            password: DB_READ_PASSWORD,
            database: DB_NAME,
            connectionLimit: 5
        });
    }
    return readPool;
}

// Lazy Initialization for adminPool
async function getAdminPool() {
    if (!adminPool) {
        const mariadb = await import('mariadb');
        adminPool = mariadb.createPool({
            host: DB_HOST,
            user: DB_ADMIN_USER,
            password: DB_ADMIN_PASSWORD,
            database: DB_NAME,
            connectionLimit: 2
        });
    }
    return adminPool;
}

module.exports = { getWritePool, getReadPool, getAdminPool };

