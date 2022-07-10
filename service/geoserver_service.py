import json
import requests
import itertools
from flask import make_response
from settings import GEOSERVER_BASE_URL, GEOSERVER_PASSWORD, GEOSERVER_USERNAME


def get_categories():
    body = get(GEOSERVER_BASE_URL + '/workspaces')
    categories_by_workspace = list(map(lambda workspace: list(process_workspace(workspace)), body['workspaces']['workspace']))
    filtered_categories = [category for category in categories_by_workspace if category != []]
    flattened_categories = list(itertools.chain(*filtered_categories))
    return make_response(json.dumps(flattened_categories), 200)


def process_workspace(workspace):
    return list(itertools.chain(
        # get_data_stores(workspace),
        get_coverage_stores(workspace),
        get_wms_stores(workspace),
        get_wmts_stores(workspace))
    )


def get_data_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/datastores')
    if body['dataStores'] != '':
        data_stores = body['dataStores']['dataStore']
        return list(map(lambda data_store: process_data_store(data_store, workspace['name']), data_stores))
    else:
        print("No dataStores found for workspace " + workspace['name'])
        return []


def get_coverage_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/coveragestores')
    if body['coverageStores'] != '':
        coverage_stores = body['coverageStores']['coverageStore']
        return list(map(lambda coverage_store: process_coverage_store(coverage_store, workspace['name']), coverage_stores))
    else:
        print("No coverageStores found for workspace " + workspace['name'])
        return []


def get_wms_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/wmsstores')
    if body['wmsStores'] != '':
        wms_stores = body['wmsStores']['wmsStore']
        return list(map(lambda wms_store: process_wms_store(wms_store, workspace['name']), wms_stores))
    else:
        print("No wmsStores found for workspace " + workspace['name'])
        return []


def get_wmts_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/wmtsstores')
    if body['wmtsStores'] != '':
        data_stores = body['wmtsStores']['wmtsStore']
        return list(map(lambda data_store: process_wmts_store(data_store, workspace['name']), data_stores))
    else:
        print("No wmtsStores found for workspace " + workspace['name'])
        return []


def process_data_store(data_store, workspace_name):
    category_name = data_store['name']
    feature_types_href = get(data_store['href'])['dataStore']['featureTypes']
    body = get(feature_types_href)
    data_layers = body['dataLayers']['dataLayer']
    subcategories = list(map(lambda data_layer: process_data_layer(data_layer, workspace_name), data_layers))
    return {'category_name': category_name, 'subcategories': subcategories}


def process_coverage_store(coverage_store, workspace_name):
    category_name = coverage_store['name']
    coverage_layers_href = get(coverage_store['href'])['coverageStore']['coverages']
    body = get(coverage_layers_href)
    coverage_layers = body['coverages']['coverage']
    subcategories = list(map(lambda coverage_layer: process_coverage_layer(coverage_layer, workspace_name), coverage_layers))
    return {'category_name': category_name, 'subcategories': subcategories}


def process_wms_store(wms_store, workspace_name):
    category_name = wms_store['name']
    wms_layers_href = get(wms_store['href'])['wmsStore']['wmslayers']
    body = get(wms_layers_href)
    wms_layers = body['wmsLayers']['wmsLayer']
    subcategories = list(map(lambda wms_layer: process_wms_layer(wms_layer, workspace_name), wms_layers))
    return {'category_name': category_name, 'subcategories': subcategories}


def process_wmts_store(wmts_store, workspace_name):
    category_name = wmts_store['name']
    wmts_layers_href = get(wmts_store['href'])['wmtsStore']['layers']
    body = get(wmts_layers_href)
    wmts_layers = body['wmtsLayers']['wmtsLayer']
    subcategories = list(map(lambda wmts_layer: process_wmts_layer(wmts_layer, workspace_name), wmts_layers))
    return {'category_name': category_name, 'subcategories': subcategories}


def process_data_layer(layer, workspace_name):
    layer_response = get(layer['href'])
    return {'name': layer_response['dataLayer']['title'], 'layer_name': workspace_name + ':' + layer['name']}


def process_coverage_layer(layer, workspace_name):
    layer_response = get(layer['href'])
    return {'name': layer_response['coverage']['title'], 'layer_name': workspace_name + ':' + layer['name']}


def process_wms_layer(layer, workspace_name):
    layer_response = get(layer['href'])
    return {'name': layer_response['wmsLayer']['title'], 'layer_name': workspace_name + ':' + layer['name']}


def process_wmts_layer(layer, workspace_name):
    layer_response = get(layer['href'])
    return {'name': layer_response['wmtsLayer']['title'], 'layer_name': workspace_name + ':' + layer['name']}


def get(url):
    response = requests.get(url, auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD))
    return json.loads(response.content)
