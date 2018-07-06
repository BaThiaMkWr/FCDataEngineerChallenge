-- ----------------------------
--  create user fred_user
-- ----------------------------
REASSIGN OWNED BY fred_user TO postgres;
DROP OWNED BY fred_user;
DROP USER IF EXISTS fred_user;
CREATE USER fred_user WITH PASSWORD 'fred_password';

-- ----------------------------
--  create database fred
-- ----------------------------
 \connect postgres
SELECT
 pg_terminate_backend (pg_stat_activity.pid)
FROM
 pg_stat_activity
WHERE
 pg_stat_activity.datname = 'fred';
DROP DATABASE IF EXISTS fred ;
CREATE DATABASE fred;
\connect fred;
-- ----------------------------
--  Schema  series
-- ----------------------------
DROP SCHEMA series CASCADE;
CREATE SCHEMA series AUTHORIZATION fred_user;
-- ----------------------------
--  Table us_civilian_unemployment_rate
-- ----------------------------
DROP TABLE IF EXISTS series.us_civilian_unemployment_rate;
CREATE TABLE series.us_civilian_unemployment_rate
(   observation_date date,
    unemployment_rate double precision
);
GRANT  ALL PRIVILEGES  ON TABLE series.us_civilian_unemployment_rate TO fred_user;

-- ----------------------------
--  Table university_of_michigan_customer_sentiment_index
-- ----------------------------
DROP TABLE IF EXISTS series.university_of_michigan_customer_sentiment_index;
CREATE TABLE series.university_of_michigan_customer_sentiment_index
(   observation_date date,
    sentiment_index double precision
);
GRANT  ALL PRIVILEGES  ON TABLE series.university_of_michigan_customer_sentiment_index TO fred_user;

-- ----------------------------
--  Table real_gross_domestic_product
-- ----------------------------
DROP TABLE IF EXISTS series.real_gross_domestic_product;
CREATE TABLE series.real_gross_domestic_product
(   observation_date date,
    rgdp_value double precision
) ;
GRANT  ALL PRIVILEGES  ON TABLE series.real_gross_domestic_product TO fred_user;

-- ----------------------------
--  TList all table
-- ----------------------------
\dt series.*