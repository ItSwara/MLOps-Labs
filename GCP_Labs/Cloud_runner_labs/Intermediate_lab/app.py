from flask import Flask
from google.cloud import storage, bigquery
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello from lab5 Cloud Run!"

@app.route('/upload')
def upload_file():
    storage_client = storage.Client()
    bucket_name = os.environ.get('BUCKET_NAME')
    if not bucket_name:
        return 'BUCKET_NAME environment variable not set', 500
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('hello.txt')
    blob.upload_from_string('Hello from Cloud Run lab5')
    return f'Uploaded hello.txt to {bucket_name}'


@app.route('/query')
def query_bigquery():
    client = bigquery.Client()
    query = """
        SELECT name, SUM(number) as total
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = 'TX'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 5
    """
    query_job = client.query(query)
    results = query_job.result()
    names = []

    for row in results:
        names.append(row.name)
    return f'Top Texas names: {", ".join(names)}'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)