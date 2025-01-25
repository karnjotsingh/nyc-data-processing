FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py", "--user=${DB_USER}", "--password=${DB_PASSWORD}", "--host=${DB_HOST}", "--port=${DB_PORT}", "--db=${DB_NAME}", "--table_name=${DB_TABLE_TRIPS}", "--url=${API_URL_TRIPS}" ]