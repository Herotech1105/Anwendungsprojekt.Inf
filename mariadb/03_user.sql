CREATE OR REPLACE USER 'websrv_write'@'localhost'
IDENTIFIED BY 'pass-0123-iot';

GRANT SELECT, INSERT ON myapp.sensor_data
TO 'websrv_write'@'localhost';

FLUSH PRIVILEGES;