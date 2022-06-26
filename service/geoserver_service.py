import json
import requests
from flask import make_response
from settings import GEOSERVER_BASE_URL, GEOSERVER_PASSWORD, GEOSERVER_USERNAME


def get_layers():
    response = requests.get(GEOSERVER_BASE_URL + '/layers', auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD))
    body = json.loads(response.content)
    layer_names = map(lambda layer: layer['name'], body['layers']['layer'])
    result = map(lambda name: {'category_name': name.split(':')[0], 'subcategory_name': name.split(':')[1]}, layer_names)

    return make_response(json.dumps(list(result)), response.status_code)
