import json
from flask import make_response


def get_base_layers_info():
    base_layers = [
        {
            'id': "argenmap-base",
            'title': "Argenmap Base",
            'image': "https://mapa.ign.gob.ar/src/styles/images/argenmap.png",
            'layer': "https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png"
        },
        {
            'id': "satelital-esri",
            'title': "Imagenes Satelitales ESRI",
            'image': "https://mapa.ign.gob.ar/src/styles/images/esri.png",
            'layer': "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png"
        }
    ]

    return make_response(json.dumps(base_layers), 200)
