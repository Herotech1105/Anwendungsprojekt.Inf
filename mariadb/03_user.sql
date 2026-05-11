CREATE USER 'websrv_write'@'websrv.lab.local'
IDENTIFIED BY 'pass-0123-iot';

GRANT SELECT, INSERT ON myapp.sensordata
TO 'websrv_write'@'websrv.lab.local';

FLUSH PRIVILEGES;