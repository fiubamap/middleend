import json
import requests
import itertools
from flask import make_response
from settings import GEOSERVER_BASE_URL, GEOSERVER_PASSWORD, GEOSERVER_USERNAME


def get_categories():
    body = get(GEOSERVER_BASE_URL + '/workspaces')
    categories_by_workspace = list(
        map(lambda workspace: process_workspace(workspace), body['workspaces']['workspace']))
    filtered_categories = [category for category in categories_by_workspace if category != {}]
    return make_response(json.dumps(filtered_categories), 200)


def process_workspace(workspace):
    subcategories = list(itertools.chain(
        get_data_stores(workspace),
        get_coverage_stores(workspace),
        get_wms_stores(workspace),
        get_wmts_stores(workspace)
    ))

    if len(subcategories) != 0:
        return {'category_name': workspace['name'], 'subcategories': subcategories}
    return {}


def get_data_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/datastores')
    if body['dataStores'] != '':
        data_stores = body['dataStores']['dataStore']
        subcategories = list(itertools.chain(*list(map(lambda data_store: process_data_store(data_store, workspace['name']), data_stores))))
        if len(subcategories) != 0:
            return subcategories
    print("No dataStores found for workspace " + workspace['name'])
    return []


def get_coverage_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/coveragestores')
    if body['coverageStores'] != '':
        coverage_stores = body['coverageStores']['coverageStore']
        subcategories = list(itertools.chain(*list(map(lambda coverage_store: process_coverage_store(coverage_store, workspace['name']), coverage_stores))))
        if len(subcategories) != 0:
            return subcategories
    print("No coverageStores found for workspace " + workspace['name'])
    return []


def get_wms_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/wmsstores')
    if body['wmsStores'] != '':
        wms_stores = body['wmsStores']['wmsStore']
        subcategories = list(itertools.chain(*list(map(lambda wms_store: process_wms_store(wms_store, workspace['name']), wms_stores))))
        if len(subcategories) != 0:
            return subcategories
    print("No wmsStores found for workspace " + workspace['name'])
    return []


def get_wmts_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/wmtsstores')
    if body['wmtsStores'] != '':
        data_stores = body['wmtsStores']['wmtsStore']
        subcategories = list(itertools.chain(*list(map(lambda data_store: process_wmts_store(data_store, workspace['name']), data_stores))))
        if len(subcategories) != 0:
            return subcategories
    print("No wmtsStores found for workspace " + workspace['name'])
    return []


def process_data_store(data_store, workspace_name):
    feature_types_href = get(data_store['href'])['dataStore']['featureTypes']
    body = get(feature_types_href)
    if body != '' and body['featureTypes'] != '':
        data_layers = body['featureTypes']['featureType']
        subcategories = list(map(lambda data_layer: build_subcategory(data_store['name'], data_layer, workspace_name), data_layers))
        return subcategories
    print('Cannot process data store from workspace ' + workspace_name)
    return []


def process_coverage_store(coverage_store, workspace_name):
    coverage_layers_href = get(coverage_store['href'])['coverageStore']['coverages']
    body = get(coverage_layers_href)
    if body != '' and body['coverages'] != '':
        coverage_layers = body['coverages']['coverage']
        subcategories = list(
            map(lambda coverage_layer: build_subcategory(coverage_store['name'], coverage_layer, workspace_name), coverage_layers))
        return subcategories
    print('Cannot process coverage store from workspace ' + workspace_name)
    return []


def process_wms_store(wms_store, workspace_name):
    wms_layers_href = get(wms_store['href'])['wmsStore']['wmslayers']
    body = get(wms_layers_href)
    if body != '' and body['wmsLayers'] != '':
        wms_layers = body['wmsLayers']['wmsLayer']
        subcategories = list(map(lambda wms_layer: build_subcategory(wms_store['name'], wms_layer, workspace_name), wms_layers))
        return subcategories
    print('Cannot process wms store from workspace ' + workspace_name)
    return []


def process_wmts_store(wmts_store, workspace_name):
    wmts_layers_href = get(wmts_store['href'])['wmtsStore']['layers']
    body = get(wmts_layers_href)
    if body != '' and body['wmtsLayers'] != '':
        wmts_layers = body['wmtsLayers']['wmtsLayer']
        subcategories = list(map(lambda wmts_layer: build_subcategory(wmts_store['name'], wmts_layer, workspace_name), wmts_layers))
        return subcategories
    print('Cannot process wmts store from workspace ' + workspace_name)
    return []


def get(url):
    response = requests.get(url, auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD))
    return json.loads(response.content)


def build_subcategory(store_name, layer, workspace_name):
    return {'name': store_name, 'layer_name': workspace_name + ':' + layer['name']}
