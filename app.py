from flask import Flask
import os

from service.geoserver_service import build_categories

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/categories')
def get_categories():
    response = build_categories()
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
