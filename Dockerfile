FROM apache/airflow:2.8.2-python3.9

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

USER root

RUN apt-get update && apt-get install -y \
    wget

COPY start.sh /start.sh
RUN chmod +x /start.sh
USER airflow

ENTRYPOINT ["/bin/bash","/start.sh"]
