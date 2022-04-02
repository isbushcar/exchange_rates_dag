import logging
from datetime import datetime, timedelta

import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowSkipException


BASE_TIMESERIES_API_URL = 'https://api.exchangerate.host/timeseries'
BASE_LATEST_API_URL = 'https://api.exchangerate.host/latest'
BASE_REQUEST_PARAMS = {'base': 'BTC', 'source': 'crypto', 'symbols': 'USD'}
DB_CONN = PostgresHook('exchange_rates_db')
TABLE_NAME = 'public.exchangerate_host_api'


def get_btc_usd_history(dag_start_date: datetime, **context) -> None:
    """
    Get rates' history if last execution date was earlier than yesterday.
    Args:
        dag_start_date - first day to get data if it's DAG's first run
    """
    execution_date = context.get('logical_date')
    start_date = dag_start_date.strftime('%Y-%m-%d')
    last_updated = DB_CONN.get_records(
        f"""
        SELECT
            coalesce(
                max(exchange_rate_timestamp),
                '{start_date}'::timestamp
                )
        FROM {TABLE_NAME}
        WHERE pair = 'BTC/USD'
        """,
    ).pop()[0]

    if last_updated.date() >= (datetime.today() - timedelta(days=1)).date():
        raise AirflowSkipException

    dates_dict = {
        'start_date': last_updated.strftime('%Y-%m-%d'),
        'end_date': (execution_date - timedelta(days=1)).strftime('%Y-%m-%d'),
    }
    request_params = BASE_REQUEST_PARAMS.copy()
    request_params.update(dates_dict)

    response = requests.get(BASE_TIMESERIES_API_URL, request_params)
    for day, rates_dict in response.json()['rates'].items():
        for _, rate in rates_dict.items():
            DB_CONN.run(
                f"""
                INSERT INTO {TABLE_NAME}
                    (pair, exchange_rate_timestamp, exchange_rate, is_history)
                VALUES ('BTC/USD', '{day}', {rate}, TRUE)
                ON CONFLICT DO NOTHING
                """
            )


def get_current_btc_usd_rate(**context) -> None:
    """Get latest rate."""
    response = requests.get(BASE_LATEST_API_URL, BASE_REQUEST_PARAMS)
    execution_date = context.get('logical_date')
    logging.warning(response.json()['rates'])
    rate = response.json()['rates']['USD']
    DB_CONN.run(
        f"""
        INSERT INTO {TABLE_NAME} (pair, exchange_rate_timestamp, exchange_rate)
            VALUES ('BTC/USD', '{execution_date}', {rate})
        """
    )
