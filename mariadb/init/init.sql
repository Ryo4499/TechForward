CREATE DATABASE IF NOT EXISTS kenshu CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'kenshu2021';
GRANT ALL ON kenshu.* TO 'user'@'%';

CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'kenshu2021';
GRANT ALL ON kenshu.* TO 'user'@'localhost';

FLUSH PRIVILEGES;

use kenshu;