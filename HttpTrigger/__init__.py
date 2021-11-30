import json
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    with open("credentials.json", "r") as f:
        envs = json.load(f)

    for key, value in envs.items():
        os.environ[key] = value

    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    images_container = blob_service_client.get_container_client("images")
    image_list = images_container.list_blobs()
    html = ""
    image_list = sorted(image_list, key=lambda x: x.last_modified, reverse=True)
    for image in image_list:
        image_client = images_container.get_blob_client(image.name)
        html += f"<h3>{image_client.blob_name}</h3> &nbsp <i> Last Modified on </i> {image.last_modified}<br/>"
        html += f"<img src='{image_client.url}'/><br>"
    return func.HttpResponse(html, mimetype="text/html")
