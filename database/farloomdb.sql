CREATE DATABASE IF NOT EXISTS farloomdb ENCODING 'utf-8' ;

CREATE TABLE IF NOT EXISTS advertisements (
    id BIGINT PRIMARY KEY,
    description VARCHAR(255),
    created_at TIMESTAMP,
    character_advertised VARCHAR(50)
);

COPY advertisements FROM '/tmp/farloom_ads.csv' DELIMITER ',' CSV HEADER;

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.ad_clicks_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ad_id BIGINT, -- not sure if this will be a foreign key
    created_at TIMESTAMP,
    FOREIGN KEY (ad_id) REFERENCES public.advertisements (id)
);
