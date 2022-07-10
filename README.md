# middleend

##How to run

sudo docker build -t middleend .

sudo docker run middleend:latest o sudo docker run -d -p 5000:5000 middleend:latest


Para levantar el proyecto localmente, crear un archivo .env a la altura de app.py, con las siguientes variables de entorno:
GEOSERVER_BASE_URL (ej: 'http://localhost:8080/geoserver/rest'), GEOSERVER_USERNAME, GEOSERVER_PASSWORD 
