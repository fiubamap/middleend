import requests
from settings import GEOSERVER_WPS_URL, GEOSERVER_PASSWORD, GEOSERVER_USERNAME


def create_contour_lines(lower_corner_x, lower_corner_y, upper_corner_x, upper_corner_y, distance):
    body = """<?xml version="1.0" encoding="UTF-8"?>
<wps:Execute version="1.0.0" service="WPS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://www.opengis.net/wps/1.0.0" xmlns:wfs="http://www.opengis.net/wfs"
            xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1"
            xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc"
            xmlns:wcs="http://www.opengis.net/wcs/1.1.1" xmlns:xlink="http://www.w3.org/1999/xlink"
            xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
   <ows:Identifier>
       gs:Contour
   </ows:Identifier>
   <wps:DataInputs>
       <wps:Input>
           <ows:Identifier>data</ows:Identifier>
           <wps:Reference mimeType="image/tiff" xlink:href="http://geoserver/wcs" method="POST">
               <wps:Body>
                   <wcs:GetCoverage service="WCS" version="1.1.1">
                       <ows:Identifier>
                           Dep.Informatica:argentina
                       </ows:Identifier>
                       <wcs:DomainSubset>
                           <ows:BoundingBox crs="http://www.opengis.net/gml/srs/epsg.xml#4326">
                               <ows:LowerCorner>{lower_corner_x} {lower_corner_y}</ows:LowerCorner>
                               <ows:UpperCorner>{upper_corner_x} {upper_corner_y}</ows:UpperCorner>
                           </ows:BoundingBox>
                       </wcs:DomainSubset>
                       <wcs:Output format="image/tiff"/>
                   </wcs:GetCoverage>
               </wps:Body>
           </wps:Reference>
       </wps:Input>
       <wps:Input>
           <ows:Identifier>band</ows:Identifier>
           <wps:Data>
               <wps:LiteralData>0</wps:LiteralData>
           </wps:Data>
       </wps:Input>
       <wps:Input>
           <ows:Identifier>simplify</ows:Identifier>
           <wps:Data>
               <wps:LiteralData>true</wps:LiteralData>
           </wps:Data>
       </wps:Input>
       <wps:Input>
           <ows:Identifier>smooth</ows:Identifier>
           <wps:Data>
               <wps:LiteralData>false</wps:LiteralData>
           </wps:Data>
       </wps:Input>
       <wps:Input>
           <ows:Identifier>interval</ows:Identifier>
           <wps:Data>
               <wps:LiteralData>{distance}</wps:LiteralData>
           </wps:Data>
       </wps:Input>
   </wps:DataInputs>
   <wps:ResponseForm>
       <wps:RawDataOutput mimeType="application/json">
           <ows:Identifier>result</ows:Identifier>
       </wps:RawDataOutput>
   </wps:ResponseForm>
</wps:Execute>
    """.format(lower_corner_x=lower_corner_x, lower_corner_y=lower_corner_y, upper_corner_x=upper_corner_x,
               upper_corner_y=upper_corner_y, distance=distance)
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(
        GEOSERVER_WPS_URL,
        body,
        auth=(GEOSERVER_USERNAME, GEOSERVER_PASSWORD),
        headers=headers,
        timeout=5)
    return response.json()


