-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS prostat_test_db;
CREATE USER IF NOT EXISTS 'prostat_test'@'localhost' IDENTIFIED BY 'prostat_test_pwd';
GRANT ALL PRIVILEGES ON `prostat_test_db`.* TO 'prostat_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'prostat_test'@'localhost';
FLUSH PRIVILEGES;
