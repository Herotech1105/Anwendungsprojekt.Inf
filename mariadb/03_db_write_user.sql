CREATE OR REPLACE USER 'websrv_write'@'%'
IDENTIFIED BY 'pass-0123-iot';

GRANT INSERT ON myapp.sensor_data
TO 'websrv_write'@'%';

FLUSH PRIVILEGES;