# Simple DAG example for Apache Airflow

## Description
Repository contains docker-compose.yaml based on file from 
[official documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) 
(with a little modification) and simple DAG example.

DAG collects BTC/USD exchange rate from [exchangerate.host](https://exchangerate.host)
and records it to PostgreSQL in another Docker container.
DAG runs every 3 hours and collects history data for passed days.
## Installing (requires Docker)
1. Clone repository: `git clone https://github.com/isbushcar/exchange_rates_dag.git`
2. Go to directory exchange_rates_dag `cd exchange_rates_dag`
3. Use command `make start`
4. Go get a cup of tea - it takes a while to start all the containers.

## How to use
Web interface to control Apache Airflow should become available on [localhost:8080](localhost:8080) -
default login is `airflow` and default password is `airflow`.

PostgreSQL should become available on `localhost:5437`. Default username for Airflow is `airflow` and
password is (surprise!) `airflow`.

Further instructions can be found in 
[official documentation.](https://airflow.apache.org/docs/apache-airflow/stable/index.html)