<span style="color:white; font-size:30px">Proceso ETL con MySQL, MongoDB, AWS y Análisis de Datos con Python.</span>
En este proyecto, exploraremos el proceso de Extracción, Transformación y Carga (ETL) de datos utilizando tecnologías como MySQL, MongoDB, AWS y Python. Comenzaremos descargando un conjunto de datos de una plataforma que ofrece datos gratuitos para desarrolladores. Este conjunto de datos servirá como punto de partida para nuestro análisis y procesamiento de datos.

El proceso de ETL implicará la extracción de datos de múltiples fuentes, incluidos archivos TXT, bases de datos MongoDB y archivos almacenados en Amazon S3. Utilizaremos Python para manipular y transformar los datos según sea necesario, preparándolos para su carga en nuestras bases de datos relacionales en MySQL.

Una vez que los datos estén cargados en nuestras bases de datos, realizaremos análisis de datos utilizando herramientas y bibliotecas de análisis de datos en Python.

<span style="color:white; font-size:30px">Arquitectura de flujo de datos</span>

[![Arquitectura-de-flujo-de-datos-drawio-drawio.png](https://i.postimg.cc/6pyNDNMs/Arquitectura-de-flujo-de-datos-drawio-drawio.png)](https://postimg.cc/zyZMg4mp)

<span style="color:white; font-size:30px">Estructura del Proyecto</span>

El proyecto está organizado en varios directorios, cada uno con un propósito específico:

<span style="color:white; font-size:14px">**arquitectura**: </span>
Contiene modelos de datos para la base de datos OLTP y OLAP. Aquí se definen las estructuras de tablas y relaciones para almacenar los datos de manera transaccional y analítica.

<span style="color:white; font-size:14px">**config**: </span>
En este directorio se encuentran las credenciales de acceso a servicios en la nube y la configuración de bases de datos. Es importante mantener esta información segura y separada del código fuente.

<span style="color:white; font-size:14px">**data:** </span>
A quí se almacenan los archivos de datos utilizados en el proyecto. Estos archivos pueden provenir de diversas fuentes y serán procesados y cargados en la base de datos durante el proceso ETL.

<span style="color:white; font-size:14px">**database:** </span>
Contiene clases y funciones para manejar la conexión a la base de datos MySQL y ejecutar consultas SQL, así como scripts para la creación de tablas y otros objetos de la base de datos. También incluye conexiones a los servicios de almacenamiento S3 y la base de datos NoSQL MongoDB.

<span style="color:white; font-size:14px">**log_error_proceso:** </span>
Este directorio almacena archivos de registro de errores del proceso. Es útil para identificar y solucionar problemas durante la ejecución del proceso ETL.

<span style="color:white; font-size:14px">**mysql_script:** </span>
Aquí se encuentran scripts para la creación de bases de datos en MySQL. Estos scripts son utilizados para configurar el entorno de base de datos antes de ejecutar el proceso ETL.

[![estructura-proyecto.png](https://i.postimg.cc/5y2Vrtqd/estructura-proyecto.png)](https://postimg.cc/njggjpP0)

<span style="color:white; font-size:30px">Requisitos previos:</span>

Antes de ejecutar este proyecto, asegúrese de tener instaladas las siguientes herramientas:

- Python versión 3.10.6 
- MySQL
- MongoDB

Asegúrese de tener Python 3.10.6, MySQL y MongoDB instalados y configurados correctamente antes de ejecutar el proyecto.


<span style="color:white; font-size:30px">Configuración de bases de datos:</span>

Para MongoDB, siga estos pasos de configuración:

1. Cree una base de datos llamada `importaciones` en su servidor local de MongoDB.

2. En el directorio `data` del proyecto, encontrará un archivo llamado `collection_year_2018.json`. Este archivo contiene los registros que se deben restaurar en la base de datos que acaba de crear.

Para MySQL, siga estos pasos de configuración:

1. Cree las siguientes bases de datos manualmente en su servidor MySQL:
   - `importaciones_db`
   - `importaciones_olap`

2. Una vez creadas las bases de datos, el programa leerá automáticamente los scripts de creación de tablas y dependencias ubicados en el directorio `database`. Estos scripts se utilizarán para crear las tablas y configurar las relaciones necesarias en las bases de datos recién creadas.

Este proceso de configuración garantiza que las bases de datos estén listas para ser utilizadas por el proyecto sin necesidad de realizar pasos adicionales de configuración manual.

Puede utilizar su cliente MySQL preferido o ejecutar comandos SQL directamente en la interfaz de línea de comandos.

<span style="color:white; font-size:30px">Configuración de AWS S3:</span>

Para que el programa pueda conectarse a AWS S3, siga estos pasos de configuración:

1. Asegúrese de tener una cuenta de AWS y haber creado un bucket en AWS S3. Si no tiene una cuenta de AWS, puede registrarse en [AWS](https://aws.amazon.com/).

2. En el archivo `proceso_etl_OLTP.py`, encontrará la siguiente línea de código que se encarga de la conexión con AWS S3 y la búsqueda de archivos:
   
   ```python
   aws_s3 = AWSS3Conexion()
   aws_s3.listar_archivos('nombre_del_bucket', 'ruta_del_directorio', '.extension', PATH_PROYECTO)
   
   [![s3-comentar.png](https://i.postimg.cc/N0NLbLHT/s3-comentar.png)](https://postimg.cc/McQWp6tK)
   
- El primer parámetro de la función listar_archivos es el nombre del bucket en AWS S3 que ha creado.
- El segundo parámetro es la ruta del directorio dentro del bucket donde se buscarán los archivos.
- El tercer parámetro es la extensión del formato de archivo que se buscará en el bucket.
- El cuarto parámetro PATH_PROYECTO es la ruta del directorio del proyecto en local.
- Asegúrese de reemplazar 'nombre_del_bucket', 'ruta_del_directorio' y '.extension' con los valores correspondientes según su configuración en AWS S3.

<span style="color:white; font-size:20px">Si no desea que el programa se conecte a un bucket de AWS S3, simplemente puede comentar la línea de código mostrada anteriormente en el archivo proceso_etl_OLTP.py. Por ejemplo:</span>


    #aws_s3 = AWSS3Conexion()
    #aws_s3.listar_archivos('nombre_del_bucket', 'ruta_del_directorio', '.extension', PATH_PROYECTO)


<span style="color:white; font-size:30px">Instrucciones de activación del entorno virtual</span>

Para activar el entorno virtual en su sistema, siga estos pasos:

##### 1. Navegue hasta la carpeta del proyecto utilizando la terminal o el símbolo del sistema.

		ETL con python/pythonetl/Scripts

##### 2. Dentro de la carpeta `Scripts`, ejecute el siguiente comando:

		activate

##### 3. Instrucciones para instalar dependencias:

Para instalar las dependencias del proyecto, siga estos pasos:

1. Asegúrese de haber activado el entorno virtual como se describe anteriormente.
2. Ejecute el siguiente comando en la terminal:

		pip install -r requirements.txt

<span style="color:white; font-size:30px">Configuración del archivo configuracion.py</span>

En el archivo `configuracion.py`, encontrará las siguientes variables globales que deben configurarse correctamente antes de ejecutar el proyecto:

### Para MongoDB:

- `MONGODB_URI`: La URI de conexión de MongoDB. Asegúrese de reemplazar `'grupo6_NOMBRE_USUARIO'` y `'grupo6_CONTRASEÑA'` con el nombre de usuario y contraseña respectivamente, y `'cluster0.j1dl4hp.mongodb.net'` con la URL de su clúster MongoDB.
- `MONGODB_DATABASE`: El nombre de la base de datos de MongoDB que se utilizará en el proyecto.

### Para AWS S3:

- `AWS_ACCESS_KEY_ID`: La ID de clave de acceso de AWS necesaria para autenticarse con los servicios de AWS.
- `AWS_SECRET_ACCESS_KEY`: La clave de acceso secreta de AWS necesaria para autenticarse con los servicios de AWS.

### Para la base de datos MySQL:

- `MYSQL_HOST`: La dirección IP y el puerto del servidor MySQL.
- `MYSQL_USER`: El nombre de usuario para acceder a MySQL.
- `MYSQL_PASSWORD`: La contraseña para acceder a MySQL.
- `MYSQL_DATABASE`: El nombre de la base de datos de MySQL que se utilizará en el proyecto.
- `MYSQL_DATABASE_OLAP`: El nombre de la base de datos OLAP de MySQL que se utilizará en el proyecto.

[![configuracion-py.png](https://i.postimg.cc/JhBY1H5c/configuracion-py.png)](https://postimg.cc/B84Bp6yX)

<span style="color:white; font-size:30px">Archivos de proceso ETL</span>

Los archivos `proceso_etl_OLTP.py` y `proceso_etl_OLAP.py` contienen toda la lógica necesaria para realizar el proceso ETL (Extract, Transform, Load) correspondiente en los modelos OLTP y OLAP, respectivamente. A continuación, se describe brevemente la funcionalidad de cada archivo:

<span style="color:white; font-size:18px">proceso_etl_OLTP.py</span>


Este archivo contiene la lógica para realizar el proceso ETL en el modelo OLTP. Las principales tareas que realiza son:

- Leer la información de las fuentes de datos en dataframes.
- Realizar las transformaciones necesarias en los datos según las reglas de negocio establecidas.
- Volcar la información transformada en la base de datos OLTP configurada en el archivo `config.py`.

<span style="color:white; font-size:18px">proceso_etl_OLAP.py</span>


Este archivo contiene la lógica para realizar el proceso ETL en el modelo OLAP. Las principales tareas que realiza son:

- Leer la información de las fuentes de datos en dataframes.
- Realizar las transformaciones necesarias en los datos para generar los cubos de datos para el análisis OLAP.
- Volcar la información transformada en la base de datos OLAP configurada en el archivo `config.py`.

Asegúrese de revisar y configurar adecuadamente los archivos `configuracion.py` y `proceso_etl_OLTP.py` y `proceso_etl_OLAP.py` antes de ejecutar el proyecto, ya que contienen la configuración y la lógica esencial para el proceso ETL en los modelos OLTP y OLAP.

## Modelo físico OLTP

[![Modelo-Fisico-OLTP.png](https://i.postimg.cc/gkLJcXpg/Modelo-Fisico-OLTP.png)](https://postimg.cc/xcYYtdcm)

## Modelo físico OLAP

[![Modelo-Fisico-OLAP.png](https://i.postimg.cc/jS0kx0Xn/Modelo-Fisico-OLAP.png)](https://postimg.cc/BXpCpzRJ)
