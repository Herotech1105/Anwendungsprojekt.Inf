let pool;

async function getPool() {
    if (!pool) {
        // Hier ist der dynamische Import
        const mariadb = await import('mariadb');
        pool = mariadb.createPool({
            host: 'maria.local', 
            user: 'db_write_user', 
            password: 'password',
            database: 'password',
            connectionLimit: 5
        });
    }
    return pool;
}

module.exports = { getPool };

