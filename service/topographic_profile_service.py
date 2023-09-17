import requests
import json
from geopy.distance import geodesic
from settings import GEOSERVER_OWS_URL, GEOSERVER_PASSWORD, GEOSERVER_USERNAME

DIFFERENCE = 0.00000001


def get_elevation_data(start_x, start_y, end_x, end_y, points):
    url = GEOSERVER_OWS_URL + "?service=WMS&version =1.1.1&REQUEST=GetFeatureInfo&" \
                              "QUERY_LAYERS=Dep.Informatica:argentina&LAYERS=Dep.Informatica:argentina&" \
                              "INFO_FORMAT=application%2Fjson&FEATURE_COUNT=1&X=1&Y=1&SRS=EPSG%3A4326&WIDTH=1&" \
                              "HEIGHT=1&BBOX={},{},{},{}"

    start = (start_x, start_y)
    end = (end_x, end_y)

    coordinates = []

    total_distance = geodesic(start, end).kilometers

    for i in range(points + 1):
        frac = i / points
        point = (
            start[0] + (end[0] - start[0]) * frac,
            start[1] + (end[1] - start[1]) * frac
        )
        response = requests.post(
            url=url.format(point[0], point[1], point[0] + DIFFERENCE, point[1] + DIFFERENCE),
            auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD),
            headers=[])
        distance_to_point = geodesic(start, point).kilometers
        coordinates.append({'distance': distance_to_point, 'elevation': json.loads(response.content)['features'][0]['properties']['GRAY_INDEX']})

    return {
        'coordinates': coordinates,
        'total_distance': total_distance
    }
