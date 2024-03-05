import os, pandas as pd
from datetime import datetime
from config.configuracion import MYSQL_URL, PATH_PROYECTO, V_LS_CAMPOSDF
from database.BuckerS3_conexion import AWSS3Conexion
from database.mongodb_conexion import MongoDBConexion
from database.mysql_conexion import MySQLConexion
from sqlalchemy.exc import IntegrityError

# INSTANCIO A LA CONEXION MYSQL

conexion_mysql = MySQLConexion(MYSQL_URL)
conexion_mysql.procesar_script_oltp()

aws_s3 = AWSS3Conexion()
aws_s3.listar_archivos('databricks-workspace-stack-556fd-bucket', 'data/', '.txt', PATH_PROYECTO)

# DATAFRAME QUE LEE ARCHIVOS TXT

df_unificado = aws_s3.unificar_archivos_txt()

# DATAFRAME QUE SE TRAE DEL MONGO_DB

mongodb = MongoDBConexion()
ls_mongodb = mongodb.busqueda('collection_year_2018', {})
df_mongodb = pd.DataFrame(ls_mongodb)
df_mongodb = df_mongodb[V_LS_CAMPOSDF]

# UNIFICACION DE DATOS TXT Y MONGODB
df_unificado = pd.concat([df_unificado, df_mongodb])

remove_accents = lambda x: ''.join(['U' if c in 'Ú' else 'u' if c in 'úüùû' else c for c in x])
df_unificado['Linea'] = df_unificado['Linea'].apply(lambda x: remove_accents(x))
df_unificado['Linea'] = df_unificado['Linea'].str.upper()



def procesar_dataframe(df_unificado, MYSQL_URL):
    
    # INSERTA TABLA MARCAS
    
    print('====PROCESO DE INSERCION DE MARCAS====')
    
    df_marcas = df_unificado['Marca'].unique()
    df_unificado1 = df_unificado
    
    for marcas in df_marcas:
        conexion_mysql.insert_marca(marcas)

    # INSERTA TABLA MODELO_LANZAMIENTO

    print('====PROCESO DE INSERCION DE MODELO_LANZAMIENTO====')
    
    df_modelo_lanzamiento = df_unificado['Modelo del Vehiculo'].unique()

    for anios in df_modelo_lanzamiento:
        conexion_mysql.insert_modelo_lanzamiento(anios)

    # INSERTA TABLA TIPO DE COMBUSTIBLE
    
    print('====PROCESO DE INSERCION DE TIPO DE COMBUSTIBLE====')
    
    df_tipo_combustible = df_unificado['Tipo Combustible'].unique()

    for NombreTipoCombustible in df_tipo_combustible:
        conexion_mysql.insert_tipo_combustible(NombreTipoCombustible)
        
    # INSERTA TABLA TIPO DE VEHICULO
    
    print('====PROCESO DE INSERCION DE TIPO DE VEHICULO====')
    
    df_tipo_vehiculo = df_unificado['Tipo de Vehiculo'].unique()

    for NombreTipoVehiculo in df_tipo_vehiculo:
        conexion_mysql.insert_tipo_vehiculo(NombreTipoVehiculo)

    # INSERTA TABLA TIPO DE IMPORTADOR
    
    print('====INSERTA TABLA TIPO DE IMPORTADOR====')
    
    df_tipo_importador = df_unificado['Tipo de Importador'].unique()

    for NombreTipoImportador in df_tipo_importador:
        conexion_mysql.insert_tipo_importador(NombreTipoImportador)
       
    # INSERTA TABLA PAIS_ORIGEN
    
    print('====INSERTA TABLA PAIS_ORIGEN====')
    
    df_pais_origen = df_unificado['Pais de Proveniencia'].unique()

    for NombrePaisOrigen in df_pais_origen:
        conexion_mysql.insert_pais_origen(NombrePaisOrigen)  
    
    # INSERTA TABLA ADUANA_INGRESO
    
    print('====INSERTA TABLA ADUANA_INGRESO====')
    
    df_aduana_ingreso = df_unificado['Aduana de Ingreso'].unique()

    for NombreAduanaIngreso in df_aduana_ingreso:
        conexion_mysql.insert_aduana_ingreso(NombreAduanaIngreso) 
    
    # INSERTA TABLA LINEA
    
    print('====INSERTA TABLA LINEA====')
    
    
    
    #df_linea  = df_unificado['Linea'].drop_duplicates()
    #for NombreLinea in df_linea:        
    #    conexion_mysql.insert_linea(NombreLinea)
    
    

    df_linea  = df_unificado['Linea'].drop_duplicates()
    
    try:
        # Lista de diccionarios con los datos para los nuevos registros
        nuevos_registros = []
        
        for linea in df_linea:
            #print(linea)
            nuevo_registro = {
                'NombreLinea': linea
            }
            nuevos_registros.append(nuevo_registro)
        
        # Realizar la inserción masiva
        conexion_mysql.insert_linea(nuevos_registros)
        
    except IntegrityError as e:
        # Manejar la excepción si hay algún error de integridad
        print("Error de integridad:", e)
    
     # INSERTA TABLA PAIS_ADUANA
    
    print('====INSERTA TABLA PAIS_ADUANA====')

    df_pais_aduana  = df_unificado[['Pais de Proveniencia', 'Aduana de Ingreso']].drop_duplicates()
    
    df_pais_origen = conexion_mysql.select_pais_origen() 
    df_pais_origen = pd.DataFrame(df_pais_origen)
    
    df_paisorigen_new = pd.merge(df_pais_aduana, df_pais_origen, left_on='Pais de Proveniencia', right_on='NombrePaisOrigen')
    
    df_aduana_ingreso = conexion_mysql.select_aduana_ingreso() 
    df_aduana_ingreso = pd.DataFrame(df_aduana_ingreso)
    
    df_pais_aduana_new = pd.merge(df_paisorigen_new, df_aduana_ingreso, left_on='Aduana de Ingreso', right_on='NombreAduanaIngreso')
    df_pais_aduana_new  = df_pais_aduana_new[['IdPaisOrigen', 'IdAduanaIngreso']].drop_duplicates()
    
    for row in df_pais_aduana_new.itertuples(index=False):
        IdPaisOrigen = row.IdPaisOrigen
        IdAduanaIngreso = row.IdAduanaIngreso
        
        conexion_mysql.insert_pais_aduana(IdPaisOrigen, IdAduanaIngreso)
    
    
    # INSERTA TABLA LINEA_MODELO
    
    print('====INSERTA TABLA LINEA_MODELO====')
        
    df_linea_modelo  = df_unificado[['Linea', 'Modelo del Vehiculo', 'Marca']].drop_duplicates()
    
    df_select_linea = conexion_mysql.select_linea() 
    df_select_linea = pd.DataFrame(df_select_linea)
    
    
    df_linea_modelo_new = pd.merge(df_linea_modelo, df_select_linea, left_on='Linea', right_on='NombreLinea')
    
    df_select_modelo_lanzamiento = conexion_mysql.select_modelo_lanzamiento() 
    df_select_modelo_lanzamiento = pd.DataFrame(df_select_modelo_lanzamiento)
    
    df_linea_modelo_insert = pd.merge(df_linea_modelo_new, df_select_modelo_lanzamiento, left_on='Modelo del Vehiculo', right_on='anio')
    
    df_select_marcas = conexion_mysql.select_marca() 
    df_select_marcas = pd.DataFrame(df_select_marcas)
    
    df_linea_modelo_insert_new = pd.merge(df_linea_modelo_insert, df_select_marcas, left_on='Marca', right_on='NombreMarca')
    
    df_linea_modelo_final  = df_linea_modelo_insert_new[['IdLinea', 'IdModeloLanzamiento', 'IdMarca']].drop_duplicates()
    
    try:
        # Lista de diccionarios con los datos para los nuevos registros
        nuevos_registros = []
        
        for row in df_linea_modelo_final.itertuples(index=False):
            nuevo_registro = {
                'IdLinea': row.IdLinea,
                'IdModeloLanzamiento': row.IdModeloLanzamiento,
                'IdMarca': row.IdMarca
            }
            nuevos_registros.append(nuevo_registro)
        
        # Realizar la inserción masiva
        conexion_mysql.insert_linea_modelo(nuevos_registros)
        
    except IntegrityError as e:
        # Manejar la excepción si hay algún error de integridad
        print("Error de integridad:", e)
        
    # INSERTA TABLA IMPORTACIONES
    
    print('====PROCESO DE INSERCION DE IMPORTACIONES====')
    
    df_pais_origen1 = conexion_mysql.select_pais_origen()
    df_pais_origen1 = pd.DataFrame(df_pais_origen1)

    df_unificado1 = pd.merge(df_unificado1, df_pais_origen1, left_on='Pais de Proveniencia', right_on='NombrePaisOrigen')

    df_aduana_ingreso1 = conexion_mysql.select_aduana_ingreso() 
    df_aduana_ingreso1 = pd.DataFrame(df_aduana_ingreso1)
    #df_aduana_ingreso1
    df_unificado1 = pd.merge(df_unificado1, df_aduana_ingreso1, left_on='Aduana de Ingreso', right_on='NombreAduanaIngreso')

    df_select_modelo_lanzamiento1 = conexion_mysql.select_modelo_lanzamiento() 
    df_select_modelo_lanzamiento1 = pd.DataFrame(df_select_modelo_lanzamiento1)

    #df_select_modelo_lanzamiento1.head(5)
    df_unificado1 = pd.merge(df_unificado1, df_select_modelo_lanzamiento1, left_on='Modelo del Vehiculo', right_on='anio')

    df_select_marcas1 = conexion_mysql.select_marca() 
    df_select_marcas1 = pd.DataFrame(df_select_marcas1)

    df_unificado1 = pd.merge(df_unificado1, df_select_marcas1, left_on='Marca', right_on='NombreMarca')

    df_select_linea1 = conexion_mysql.select_linea() 
    df_select_linea1 = pd.DataFrame(df_select_linea1)

    df_unificado1 = pd.merge(df_unificado1, df_select_linea1, left_on='Linea', right_on='NombreLinea')

    df_select_tipo_vehiculo = conexion_mysql.select_tipo_vehiculo() 
    df_select_tipo_vehiculo = pd.DataFrame(df_select_tipo_vehiculo)

    df_unificado1 = pd.merge(df_unificado1, df_select_tipo_vehiculo, left_on='Tipo de Vehiculo', right_on='NombreTipoVehiculo')

    df_select_tipo_importador = conexion_mysql.select_tipo_importador() 
    df_select_tipo_importador = pd.DataFrame(df_select_tipo_importador)

    df_unificado1 = pd.merge(df_unificado1, df_select_tipo_importador, left_on='Tipo de Importador', right_on='NombreTipoImportador')

    df_select_tipo_combustible = conexion_mysql.select_tipo_combustible() 
    df_select_tipo_combustible = pd.DataFrame(df_select_tipo_combustible)

    df_unificado1 = pd.merge(df_unificado1, df_select_tipo_combustible, left_on='Tipo Combustible', right_on='NombreTipoCombustible')

    df_unificado1 = df_unificado1[['IdPaisOrigen', ' Fecha de la Poliza', 'IdAduanaIngreso', 'IdModeloLanzamiento', 'IdMarca', 'IdLinea', 'IdTipoVehiculo', 'IdTipoImportador', 'IdTipoCombustible', 'Asientos', 'Puertas', 'Tonelaje', 'Valor CIF', 'Impuesto']]
    df_select_pais_aduana = conexion_mysql.select_pais_aduana() 
    df_select_pais_aduana = pd.DataFrame(df_select_pais_aduana)

    df_unificado1 = pd.merge(df_unificado1, df_select_pais_aduana, on=['IdPaisOrigen', 'IdAduanaIngreso'])
    df_unificado1 = df_unificado1[['IdPais_IdAduana', 'IdTipoVehiculo', 'IdTipoCombustible', 'IdTipoImportador',' Fecha de la Poliza', 'Valor CIF', 'Impuesto', 'Puertas', 'Tonelaje', 'Asientos', 'IdModeloLanzamiento', 'IdMarca', 'IdLinea' ]]

    df_select_linea_modelo = conexion_mysql.select_linea_modelo() 
    df_select_linea_modelo = pd.DataFrame(df_select_linea_modelo)

    df_unificado1 = pd.merge(df_unificado1, df_select_linea_modelo, on=['IdModeloLanzamiento', 'IdMarca', 'IdLinea'])
    df_unificado1 = df_unificado1[['IdPais_IdAduana', 'IdLinea_Modelo', 'IdTipoVehiculo', 'IdTipoCombustible', 'IdTipoImportador',' Fecha de la Poliza', 'Valor CIF', 'Impuesto', 'Puertas', 'Tonelaje', 'Asientos']]
            
    try:
        # Lista de diccionarios con los datos para los nuevos registros
        nuevos_registros = []
        
        for row in df_unificado1.itertuples(index=False):
            nuevo_registro = {
                'IdPais_IdAduana': row.IdPais_IdAduana,
                'IdLinea_Modelo': row.IdLinea_Modelo,
                'IdTipoVehiculoFk': row.IdTipoVehiculo,
                'IdTipoCombustibleFk': row.IdTipoCombustible,
                'IdTipoImportadorFk': row.IdTipoImportador,
                'FechaImportacion': row._5,
                'ValorCIF': row._6,
                'Impuesto': row.Impuesto,
                'Puertas': row.Puertas,
                'Tonelaje': row.Tonelaje,
                'Asientos': row.Asientos
            }
            nuevos_registros.append(nuevo_registro)
        
        # Realizar la inserción masiva
        conexion_mysql.insert_importacion(nuevos_registros)
        
    except IntegrityError as e:
        # Manejar la excepción si hay algún error de integridad
        print("Error de integridad:", e)
    
procesar_dataframe(df_unificado, MYSQL_URL)
