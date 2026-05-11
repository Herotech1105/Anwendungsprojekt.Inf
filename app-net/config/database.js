let pool;

async function getPool() {
    if (!pool) {
        // Hier ist der dynamische Import
        const mariadb = await import('mariadb');
        pool = mariadb.createPool({
            host: 'mariadb', 
            user: 'db_write_user', 
            password: 'password',
            database: 'myapp',
            connectionLimit: 5
        });
    }
    return pool;
}

module.exports = { getPool };

