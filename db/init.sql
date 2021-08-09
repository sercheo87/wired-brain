CREATE DATABASE IF NOT EXISTS products;

USE products;

CREATE TABLE IF NOT EXISTS products
(
    id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
) ENGINE = INNODB;

ALTER USER root@localhost IDENTIFIED WITH mysql_native_password BY 'password';
