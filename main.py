import functions_framework
from google.cloud import storage
from flask import Request


@functions_framework.cloud_event
def process_file(cloud_event):
    """Triggered when a file is uploaded to Cloud Storage."""
    event = cloud_event.data
    file_name = event['name']
    bucket_name = event['bucket']

    print(f"File {file_name} uploaded to {bucket_name}. Processing...")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Leer contenido (solo si es un archivo de texto)
    if file_name.endswith('.txt'):
        content = blob.download_as_text()
        print(f"File content: {content}")


@functions_framework.http
def http_hello_world(request: Request):
    """HTTP Function that responds with a greeting."""
    request_json = request.get_json(silent=True)
    name = request_json.get('name', 'World') if request_json else 'World'

    return f"Hello, {name} from Cloud Functions!", 200
