USE myapp;

CREATE DATABASE IF NOT EXISTS myapp;

USE myapp;

CREATE TABLE IF NOT EXISTS training_data (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    timestamp   TIMESTAMP       NOT NULL,
    temperature DECIMAL(4,1)    NOT NULL,
    humidity    DECIMAL(4,1)    NOT NULL,
    heater      BOOLEAN,
    fan         BOOLEAN
);

