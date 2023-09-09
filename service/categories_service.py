import json
from json import JSONDecodeError

import requests
import itertools
from flask import make_response
from settings import GEOSERVER_BASE_URL, GEOSERVER_PASSWORD, GEOSERVER_USERNAME


def build_categories():
    workspaces_body = get(GEOSERVER_BASE_URL + '/workspaces')
    categories = list(
        filter(None, map(lambda workspace: build_category(workspace), workspaces_body['workspaces']['workspace'])))
    return make_response(json.dumps(categories), 200)


def build_category(workspace):
    subcategories = list(itertools.chain(
        list(filter(None, build_subcategories_from_data_stores(workspace))),
        list(filter(None, build_subcategories_from_coverage_stores(workspace))),
        list(filter(None, build_subcategories_from_wms_stores(workspace))),
        list(filter(None, build_subcategories_from_wmts_stores(workspace)))
    ))

    if len(subcategories) != 0:
        return {'name': workspace['name'], 'subcategories': subcategories}
    print("Category with name: " + workspace['name'] + " doesn't have any subcategories, discarding.")
    return


def build_subcategories_from_data_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/datastores')
    if body['dataStores'] != '':
        data_stores = body['dataStores']['dataStore']
        subcategories = list(filter(None, map(lambda data_store: build_subcategory_from_data_store(data_store,
                                                                                                   workspace['name']),
                                              data_stores)))
        return subcategories
    print("No dataStores found for category: " + workspace['name'])
    return []


def build_subcategories_from_coverage_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/coveragestores')
    if body['coverageStores'] != '':
        coverage_stores = body['coverageStores']['coverageStore']
        subcategories = list(filter(None,
                                    map(lambda coverage_store: build_subcategory_from_coverage_store(coverage_store,
                                                                                                     workspace['name']),
                                        coverage_stores)))
        if len(subcategories) != 0 and subcategories != [{}]:
            return subcategories
    print("No coverageStores found for category: " + workspace['name'])
    return []


def build_subcategories_from_wms_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/wmsstores')
    if body['wmsStores'] != '':
        wms_stores = body['wmsStores']['wmsStore']
        subcategories = list(filter(None, map(lambda wms_store: build_subcategory_from_wms_store(wms_store,
                                                                                                 workspace['name']),
                                              wms_stores)))
        if len(subcategories) != 0 and subcategories != [{}]:
            return subcategories
    print("No wmsStores found for category: " + workspace['name'])
    return []


def build_subcategories_from_wmts_stores(workspace):
    body = get(GEOSERVER_BASE_URL + '/workspaces/' + workspace['name'] + '/wmtsstores')
    if body['wmtsStores'] != '':
        data_stores = body['wmtsStores']['wmtsStore']
        subcategories = list(filter(None, map(lambda data_store: build_subcategory_from_wmts_store(data_store,
                                                                                                   workspace['name']),
                                              data_stores)))
        if len(subcategories) != 0 and subcategories != [{}]:
            return subcategories
    print("No wmtsStores found for category: " + workspace['name'])
    return []


def build_subcategory_from_data_store(data_store, workspace_name):
    feature_types_href = get(data_store['href'])['dataStore']['featureTypes']
    body = get(feature_types_href)
    if body != '' and body['featureTypes'] != '':
        data_layers = body['featureTypes']['featureType']
        layers = list(
            filter(None, map(lambda data_layer: build_layer_from_data_store(data_layer, workspace_name), data_layers)))
        return build_subcategory(data_store['name'], layers)
    print('No layers found for category: ' + workspace_name + ' and subcategory: ' + data_store['name'])
    return


def build_subcategory_from_coverage_store(coverage_store, workspace_name):
    coverage_layers_href = get(coverage_store['href'])['coverageStore']['coverages']
    body = get(coverage_layers_href)
    if body != '' and body['coverages'] != '':
        coverage_layers = body['coverages']['coverage']
        layers = list(filter(None,
                             map(lambda coverage_layer: build_layer_from_coverage_store(coverage_layer, workspace_name),
                                 coverage_layers)))
        return build_subcategory(coverage_store['name'], layers)
    print('No layers found for category: ' + workspace_name + ' and subcategory: ' + coverage_store['name'])
    return


def build_subcategory_from_wms_store(wms_store, workspace_name):
    wms_layers_href = get(wms_store['href'])['wmsStore']['wmslayers']
    body = get(wms_layers_href)
    if body != '' and body['wmsLayers'] != '':
        wms_layers = body['wmsLayers']['wmsLayer']
        layers = list(
            filter(None, map(lambda wms_layer: build_layer_from_wms_store(wms_layer, workspace_name), wms_layers)))
        return build_subcategory(wms_store['name'], layers)
    print('No layers found for category: ' + workspace_name + ' and subcategory: ' + wms_store['name'])
    return


def build_subcategory_from_wmts_store(wmts_store, workspace_name):
    wmts_layers_href = get(wmts_store['href'])['wmtsStore']['layers']
    body = get(wmts_layers_href)
    if body != '' and body['wmtsLayers'] != '':
        wmts_layers = body['wmtsLayers']['wmtsLayer']
        layers = list(
            filter(None, map(lambda wmts_layer: build_layer_from_wmts_store(wmts_layer, workspace_name), wmts_layers)))
        return build_subcategory(wmts_store['name'], layers)
    print('No layers found for category: ' + workspace_name + ' and subcategory: ' + wmts_store['name'])
    return


def get(url):
    response = requests.get(url, auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD))
    try:
        return json.loads(response.content)
    except JSONDecodeError:
        return {}


def build_subcategory(store_name, layers):
    if layers:
        return {'name': store_name, 'layers': layers}
    return {}


def build_layer_from_data_store(layer, workspace_name):
    res = get(layer['href'])
    if hasattr(res, 'featureType'):
        feature_type = res['featureType']
        if feature_type['enabled'] and (feature_type.get('advertised') is not None and feature_type['advertised']):
            response = {'name': workspace_name + ':' + feature_type['name'], 'title': feature_type['name']}
            if feature_type.get('abstract') is not None:
                response['description'] = feature_type['abstract']
            return response
        return


def build_layer_from_coverage_store(layer, workspace_name):
    coverage = get(layer['href'])['coverage']
    if coverage['enabled'] and (coverage.get('advertised') is not None and coverage['advertised']):
        response = {'name': workspace_name + ':' + coverage['name'], 'title': coverage['name']}
        if coverage.get('abstract') is not None:
            response['description'] = coverage['abstract']
        return response
    return


def build_layer_from_wms_store(layer, workspace_name):
    wmsLayer = get(layer['href'])['wmsLayer']
    if wmsLayer['enabled'] and (wmsLayer.get('advertised') is not None and wmsLayer['advertised']):
        response = {'name': workspace_name + ':' + wmsLayer['name'], 'title': wmsLayer['name']}
        if wmsLayer.get('abstract') is not None:
            response['description'] = wmsLayer['abstract']
        return response
    return


def build_layer_from_wmts_store(layer, workspace_name):
    wmtsLayer = get(layer['href'])['wmtsLayer']
    if wmtsLayer['enabled'] and (wmtsLayer.get('advertised') is not None and wmtsLayer['advertised']):
        response = {'name': workspace_name + ':' + wmtsLayer['name'], 'title': wmtsLayer['name']}
        if wmtsLayer.get('abstract') is not None:
            response['description'] = wmtsLayer['abstract']
        return response
    return
