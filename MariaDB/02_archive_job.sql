DELIMITER $$

CREATE EVENT IF NOT EXISTS archive_old_sensor_data
    ON SCHEDULE EVERY 1 DAY
    STARTS CURRENT_TIMESTAMP
    DO
    BEGIN
        INSERT INTO sensor_data_archive (id, timestamp, temperature, humidity)
            SELECT id, timestamp, temperature, humidity
            FROM sensor_data
            WHERE timestamp < NOW() - INTERVAL 7 DAY;

        DELETE FROM sensor_data
            WHERE timestamp < NOW() - INTERVAL 7 DAY;
    END$$

DELIMITER ;