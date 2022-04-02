from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from BTC_USD_exchange_rates_package.main import get_btc_usd_history, \
    get_current_btc_usd_rate


DEFAULT_ARGS = {
    'owner': 'isbushcar',
    'depends_on_past': False,
    'email': ['bardthebowman@de3at.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
        'BTC_USD',
        default_args=DEFAULT_ARGS,
        description='Save BTC/USD exchange rates.',
        schedule_interval='0 */3 * * *',
        start_date=datetime(2022, 3, 1, 0, 0, 0),
        catchup=False,
) as dag:

    history_rates = PythonOperator(
        task_id='get_history_rates',
        doc='doc_example',
        op_args=[dag.start_date],
        python_callable=get_btc_usd_history,
    )

    current_rate = PythonOperator(
        task_id='get_current_rate',
        python_callable=get_current_btc_usd_rate,
        trigger_rule='none_failed',
    )

    history_rates >> current_rate
