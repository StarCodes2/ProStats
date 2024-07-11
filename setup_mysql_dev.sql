-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS pro_stat_dev_db;
CREATE USER IF NOT EXISTS 'ps_user'@'localhost' IDENTIFIED BY 'Password';
GRANT ALL PRIVILEGES ON `pro_stat_dev_db`.* TO 'ps_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ps_user'@'localhost';
FLUSH PRIVILEGES;
