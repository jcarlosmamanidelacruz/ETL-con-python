import os, boto3, pandas as pd
from config import configuracion


class AWSS3Conexion:
    
    def __init__(self): # Constructor que se inicializa automaticamente
        
        self.s3 = boto3.client(
            's3',
            aws_access_key_id = configuracion.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = configuracion.AWS_SECRET_ACCESS_KEY
        )
        
    def listar_archivos(self, bucket_name, prefix, formato, ruta_local):
        
        response = self.s3.list_objects_v2(
            Bucket = bucket_name,
            Prefix = prefix
        )
        
        archivos = []
        
        for obj in response.get('Contents', []):
            
            key = obj['Key']
            
            if key.endswith(formato):
                
                ruta_archivo_local = os.path.join(ruta_local, key.split('/')[-1])
                
                if os.path.exists(ruta_archivo_local):
                    
                    os.remove(ruta_archivo_local)
                    
                self.s3.download_file(bucket_name, key, ruta_archivo_local)
                archivos.append(key)
                
        return archivos
    
    def unificar_archivos_txt(self):
        
        path_folder = (os.getcwd()).replace('\\', '/') + '/data'
        df_primero = pd.read_csv(path_folder + '/web_imp_08012019.txt', sep= "|", encoding= "latin1", index_col= False)
        df_unificado = pd.DataFrame(columns= df_primero.columns)
        df_unificado = df_unificado.dropna(axis=1, how='all')
        dfs = []  # Lista para almacenar los dataframes de cada archivo
     
        for nombre_archivo in os.listdir(path_folder):
            if nombre_archivo.endswith('2017.txt'):  # Solo procesa archivos que terminen en '2017.txt'

                filepath = os.path.join(path_folder, nombre_archivo)
                df = pd.read_csv(filepath, sep= "|", encoding= "latin1", index_col= False)
                df = df.dropna(axis=1, how='all')
                df_unificado = pd.concat([df_unificado, df])
        
        return df_unificado

