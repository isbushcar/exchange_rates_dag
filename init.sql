CREATE TABLE public.exchangerate_host_api (
    pair VARCHAR (255),
    exchange_rate_timestamp TIMESTAMP,
    exchange_rate FLOAT,
    is_history bool DEFAULT FALSE,
    load_timestamp TIMESTAMP DEFAULT now(),
    PRIMARY KEY (pair, exchange_rate_timestamp, is_history)
);
CREATE DATABASE exchange_rates TEMPLATE airflow;
DROP TABLE public.exchangerate_host_api;
