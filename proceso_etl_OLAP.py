import pandas as pd
from config.configuracion import MYSQL_URL, MYSQL_URL_OLAP, PATH_PROYECTO
from database.mysql_conexion import MySQLConexion
from database.mysql_conexion_olap import MySQLConexion_olap
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# INSTANCIO A LA CONEXION MYSQL

conexion_mysql = MySQLConexion(MYSQL_URL)
conexion_mysql_olap = MySQLConexion_olap(MYSQL_URL_OLAP)

conexion_mysql_olap.procesar_script_olap()

def procesar_olap(MYSQL_URL, MYSQL_URL_OLAP):
    
    # INSERTA TABLA DIMENSION PAIS_ORIGEN
    
    print('====PROCESO DE INSERCION DE DIMENSION PAIS_ORIGEN ====')
    
    df_pais_origen = conexion_mysql.select_pais_origen() 
    df_pais_origen = pd.DataFrame(df_pais_origen)

    for row in df_pais_origen.itertuples(index=False):
        IdPaisOrigen = row.IdPaisOrigen
        NombrePaisOrigen = row.NombrePaisOrigen
            
        conexion_mysql_olap.insert_dim_paisorigen(IdPaisOrigen, NombrePaisOrigen)

    df_select_dim_paisorigen = conexion_mysql_olap.select_dim_paisorigen()
    df_select_dim_paisorigen = pd.DataFrame(df_select_dim_paisorigen)

    
    # INSERTA TABLA DIMENSION PAIS_ORIGEN
    
    print('====PROCESO DE INSERCION DE DIMENSION DIM_ADUANAINGRESO ====')
    
    df_aduana_ingreso = conexion_mysql.select_aduana_ingreso() 
    df_aduana_ingreso = pd.DataFrame(df_aduana_ingreso)

    for row in df_aduana_ingreso.itertuples(index=False):
        IdAduanaIngreso = row.IdAduanaIngreso
        NombreAduanaIngreso = row.NombreAduanaIngreso
            
        conexion_mysql_olap.insert_dim_aduanaingreso(IdAduanaIngreso, NombreAduanaIngreso)

    df_select_aduana_ingreso = conexion_mysql_olap.select_dim_aduanaingreso()
    df_select_aduana_ingreso = pd.DataFrame(df_select_aduana_ingreso)
    
    # INSERTA TABLA DIMENSION PAIS_ADUANA

    print('====PROCESO DE INSERCION DE DIMENSION DIM_PAIS_ADUANA ====')
    
    df_select_pais_aduana = conexion_mysql.select_pais_aduana() 
    df_select_pais_aduana = pd.DataFrame(df_select_pais_aduana)
    
    for row in df_select_pais_aduana.itertuples(index=False):
        
        IdPais_IdAduana = row.IdPais_IdAduana
        IdPaisOrigen = row.IdPaisOrigen
        IdAduanaIngreso = row.IdAduanaIngreso
            
        conexion_mysql_olap.insert_dim_paisaduana(IdPais_IdAduana, IdPaisOrigen, IdAduanaIngreso)
        
    df_select_dim_paisaduana = conexion_mysql_olap.select_dim_paisaduana()
    df_select_dim_paisaduana = pd.DataFrame(df_select_dim_paisaduana)
    
    
    # INSERTA TABLA DIMENSION DIM_FECHA
    
    df_select_importacion_fechas = conexion_mysql.select_importacion_fechas() 
    df_select_importacion_fechas = pd.DataFrame(df_select_importacion_fechas)
    df_select_importacion_fechas['Fecha'] = pd.to_datetime(df_select_importacion_fechas['FechaImportacion'])
    df_select_importacion_fechas['anio'] = df_select_importacion_fechas['Fecha'].dt.year
    df_select_importacion_fechas['Mes'] = df_select_importacion_fechas['Fecha'].dt.month
    df_select_importacion_fechas['Mes_nombre'] = df_select_importacion_fechas['Fecha'].dt.month_name()
    df_select_importacion_fechas['FechaEntero'] = df_select_importacion_fechas['Fecha'].dt.strftime('%Y%m%d').astype(int)
    
    for row in df_select_importacion_fechas.itertuples(index=False):
        
        IdFecha = row.FechaEntero
        FechaImportacion = row.Fecha
        Anio = row.anio
        Mes = row.Mes
        Mes_nombre = row.Mes_nombre
            
        conexion_mysql_olap.insert_dim_fecha(IdFecha, FechaImportacion, Anio, Mes, Mes_nombre)
    
    
    df_select_importacion = conexion_mysql.select_importacion()
    df_select_importacion = pd.DataFrame(df_select_importacion)
    df_select_importacion['FechaImportacion'] = pd.to_datetime(df_select_importacion['FechaImportacion'])
    
    df_select_dim_fecha = conexion_mysql_olap.select_dim_fecha()
    df_select_dim_fecha = pd.DataFrame(df_select_dim_fecha)
    df_select_dim_fecha['FechaImportacion'] = pd.to_datetime(df_select_dim_fecha['FechaImportacion'])
    
    
    df_select_importacion = pd.merge(df_select_importacion, df_select_dim_fecha, left_on='FechaImportacion', right_on='FechaImportacion')
    df_select_importacion = df_select_importacion[['IdPais_IdAduana', 'IdFecha', 'ValorCIF', 'Impuesto']]
    
    try:
        # Lista de diccionarios con los datos para los nuevos registros
        nuevos_registros = []
        
        for row in df_select_importacion.itertuples(index=False):
            nuevo_registro = {
                'IdPais_IdAduana': row.IdPais_IdAduana,
                'IdFecha': row.IdFecha,
                'ValorCIF': row.ValorCIF,
                'Impuesto': row.Impuesto
            }
            nuevos_registros.append(nuevo_registro)
        
        # Realizar la inserción masiva
        conexion_mysql_olap.insert_fac_importaciones(nuevos_registros)
        
    except IntegrityError as e:
        # Manejar la excepción si hay algún error de integridad
        print("Error de integridad:", e)
    
procesar_olap(MYSQL_URL, MYSQL_URL_OLAP)
