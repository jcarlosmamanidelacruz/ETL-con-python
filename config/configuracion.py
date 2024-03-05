import os
# CONEXION A LA BASE DE DATOS DE ONGODB

MONGODB_URI = 'mongodb+srv://grupo6_dep18:grupo6_dep18@cluster0.j1dl4hp.mongodb.net/'
MONGODB_DATABASE = 'importaciones'

# CREDENCIALES DE ACCESO - AWS-S3

AWS_ACCESS_KEY_ID = 'AKIAYKVVOPB5C2KG3HX2'
AWS_SECRET_ACCESS_KEY = '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'

# CREDENCIALES DE ACCESO A LA BASE DE DATOS MYSQL

MYSQL_HOST = 'localhost:3306'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'acceso123'
MYSQL_DATABASE = 'importaciones_db'
MYSQL_DATABASE_OLAP = 'importaciones_olap'

MYSQL_URL = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DATABASE
MYSQL_URL_OLAP = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DATABASE_OLAP
PATH_PROYECTO = (os.getcwd()).replace('\\', '/') + '/data'

# CAMPOS DEL DATAFRAME

V_LS_CAMPOSDF = ['Pais de Proveniencia', 'Aduana de Ingreso', ' Fecha de la Poliza', 'Partida Arancelaria', 'Modelo del Vehiculo', 'Marca', 'Linea', 'Centimetros Cubicos', 'Distintivo', 'Tipo de Vehiculo', 'Tipo de Importador', 'Tipo Combustible', 'Asientos', 'Puertas', 'Tonelaje', 'Valor CIF', 'Impuesto']