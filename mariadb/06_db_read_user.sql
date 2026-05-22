CREATE OR REPLACE USER 'websrv_read'@'%'
IDENTIFIED BY 'pass-0123-iot';

GRANT SELECT ON myapp.sensor_data
TO 'websrv_read'@'%';

FLUSH PRIVILEGES;