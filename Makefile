start:
	mkdir -p ./logs ./plugins
	echo "AIRFLOW_UID=$$(id -u)" > .env
	docker-compose up airflow-init
	docker-compose up