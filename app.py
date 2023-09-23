from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os

from service.base_layers_service import get_base_layers_info
from service.categories_service import build_categories
from service.contour_lines_service import create_contour_lines
from service.topographic_profile_service import get_elevation_data

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/categories')
def get_categories():
    response = build_categories()
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/layers/base')
def get_base_layers():
    response = get_base_layers_info()
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/contour-lines', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify({'message': 'Preflight request successful'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET')
    return response


@app.route('/contour-lines', methods=['POST'])
def create_contour_lines_layer():
    request_body = request.get_json()
    try:
        layer = create_contour_lines(
            request_body.get('lower_corner').get('x'),
            request_body.get('lower_corner').get('y'),
            request_body.get('upper_corner').get('x'),
            request_body.get('upper_corner').get('y'),
            request_body.get('distance'))

        response_body = {
            'category': 'Geoprocesos',
            'layer_name': 'curva_de_nivel',
            'layer': layer
        }
        response = jsonify(response_body)

        return make_response(response, 200)
    except:
        return make_response({
            'message': 'Error al crear curvas de nivel'
        }, 500)

@app.route('/topographic-profile', methods=['POST'])
def get_elevation_data_from_line():
    request_body = request.get_json()
    elevation_data = get_elevation_data(
        request_body.get('start').get('x'),
        request_body.get('start').get('y'),
        request_body.get('end').get('x'),
        request_body.get('end').get('y'),
        request_body.get('points'))

    response = jsonify(elevation_data)

    return make_response(response, 200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
