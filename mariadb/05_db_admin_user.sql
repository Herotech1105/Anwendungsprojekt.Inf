CREATE OR REPLACE USER 'websrv_admin'@'%'
IDENTIFIED BY 'pass-0123-admin';

GRANT SELECT ON myapp.sensor_data         TO 'websrv_admin'@'%';
GRANT SELECT ON myapp.sensor_data_archive TO 'websrv_admin'@'%';

FLUSH PRIVILEGES;