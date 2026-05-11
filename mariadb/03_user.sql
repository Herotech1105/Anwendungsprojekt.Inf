CREATE OR REPLACE USER 'websrv_write'@'websrv.lab.local'
IDENTIFIED BY 'pass-0123-iot';

GRANT SELECT, INSERT ON myapp.sensor_data
TO 'websrv_write'@'websrv.lab.local';

FLUSH PRIVILEGES;