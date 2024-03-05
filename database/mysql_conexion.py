from sqlalchemy import Column, Integer, UniqueConstraint, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import logging
import os
from datetime import datetime
from sqlalchemy import text

Base = declarative_base()

class Marca(Base):
    __tablename__ = 'marca'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    NombreMarca = Column(String(45), nullable=False, unique=True)
    
class ModeloLanzamiento(Base):
    __tablename__ = 'modelo_lanzamiento'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    anio = Column(Integer, unique=True)

class TipoCombustible(Base):
    __tablename__ = 'tipo_combustible'

    id = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipoCombustible = Column(String(45), nullable=False, unique=True)

class TipoVehiculo(Base):
    __tablename__ = 'tipo_vehiculo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipoVehiculo = Column(String(45), nullable=False, unique=True)

class TipoImportador(Base):
    __tablename__ = 'tipo_importador'

    id = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipoImportador = Column(String(45), nullable=False, unique=True)
    
class PaisOrigen(Base):
    __tablename__ = 'pais_origen'

    id = Column(Integer, primary_key=True, autoincrement=True)
    NombrePaisOrigen = Column(String(45), nullable=False, unique=True)

class AduanaIngreso(Base):
    __tablename__ = 'aduana_ingreso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    NombreAduanaIngreso = Column(String(45), nullable=False, unique=True)

class PaisAduana(Base):
    __tablename__ = 'pais_aduana'

    id = Column(Integer, primary_key=True, autoincrement=True)
    IdPaisOrigen = Column(Integer, nullable=False)
    IdAduanaIngreso = Column(Integer, nullable=False)
    
class Linea(Base):
    __tablename__ = 'linea'

    id = Column(Integer, primary_key=True, autoincrement=True)
    NombreLinea = Column(String(45), nullable=False, unique=True)

class Linea_Modelo(Base):
    __tablename__ = 'linea_modelo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    IdLinea = Column(Integer, nullable=False)
    IdModeloLanzamiento = Column(Integer, nullable=False)
    IdMarca = Column(Integer, nullable=False)

class Importacion(Base):
    __tablename__ = 'importacion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    IdPais_IdAduana = Column(Integer, nullable=False)
    IdLinea_Modelo = Column(Integer, nullable=False)
    IdTipoVehiculoFk = Column(Integer, nullable=False)
    IdTipoCombustibleFk = Column(Integer, nullable=False)
    IdTipoImportadorFk = Column(Integer, nullable=False)
    FechaImportacion = Column(String(45), nullable=False)
    ValorCIF = Column(Float, nullable=False)
    Impuesto = Column(Float, nullable=False)
    Puertas = Column(Integer, nullable=False)
    Tonelaje = Column(Float, nullable=False)
    Asientos = Column(Integer, nullable=False)
  
class MySQLConexion:

    def __init__(self, db_url):        
        self.engine = create_engine(db_url) # crea un motor SQLAlchemy  pasando como argumento la url de la base de datos
        self.Session = sessionmaker(bind=self.engine) # crear sesion ORM con la base de datos
        self.session = self.Session() # sesión utilizada para realizar operaciones de base de datos
        '''
        # Configurar la ruta del archivo de registro
        log_directory = "log_error_proceso"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_file = os.path.join(log_directory, f"error_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

        # Configurar el registro de errores
        logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        '''

    def insert_marca(self, NombreMarca):

        try:
            existing_record = self.session.query(Marca.NombreMarca).filter_by(NombreMarca=NombreMarca).first()
            if not existing_record:
                nuevo_Marca = Marca(NombreMarca=NombreMarca)  # Instanciar un nuevo objeto ModeloLanzamiento
                self.session.add(nuevo_Marca)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()
            
    def select_marca(self):
        try:
            result = self.session.execute(text("SELECT * FROM marca"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_modelo_lanzamiento(self, anio):
        try:
            existing_record = self.session.query(ModeloLanzamiento.anio).filter_by(anio=anio).first()
            if not existing_record:
                nuevo_modelo = ModeloLanzamiento(anio=anio)  # Instanciar un nuevo objeto ModeloLanzamiento
                self.session.add(nuevo_modelo)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()
            
    def select_modelo_lanzamiento(self):
        try:
            result = self.session.execute(text("SELECT * FROM modelo_lanzamiento"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()

    def insert_tipo_combustible(self, NombreTipoCombustible):
        try:
            existing_record = self.session.query(TipoCombustible.NombreTipoCombustible).filter_by(NombreTipoCombustible=NombreTipoCombustible).first()
            if not existing_record:
                nuevo_TipoCombustible = TipoCombustible(NombreTipoCombustible=NombreTipoCombustible)  # Instanciar un nuevo objeto ModeloLanzamiento
                self.session.add(nuevo_TipoCombustible)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_tipo_combustible(self):
        try:
            result = self.session.execute(text("SELECT * FROM tipo_combustible"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_tipo_vehiculo(self, NombreTipoVehiculo):
        try:
            existing_record = self.session.query(TipoVehiculo.NombreTipoVehiculo).filter_by(NombreTipoVehiculo=NombreTipoVehiculo).first()
            if not existing_record:
                nuevo_TipoVehiculo = TipoVehiculo(NombreTipoVehiculo=NombreTipoVehiculo)  # Instanciar un nuevo objeto ModeloLanzamiento
                self.session.add(nuevo_TipoVehiculo)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_tipo_vehiculo(self):
        try:
            result = self.session.execute(text("SELECT * FROM tipo_vehiculo"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_tipo_importador(self, NombreTipoImportador):
        try:
            existing_record = self.session.query(TipoImportador.NombreTipoImportador).filter_by(NombreTipoImportador=NombreTipoImportador).first()
            if not existing_record:
                nuevo_TipoImportador = TipoImportador(NombreTipoImportador=NombreTipoImportador)  # Instanciar un nuevo objeto ModeloLanzamiento
                self.session.add(nuevo_TipoImportador)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_tipo_importador(self):
        try:
            result = self.session.execute(text("SELECT * FROM tipo_importador"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_pais_origen(self, NombrePaisOrigen):
        try:
            existing_record = self.session.query(PaisOrigen.NombrePaisOrigen).filter_by(NombrePaisOrigen=NombrePaisOrigen).first()
            if not existing_record:
                nuevo_PaisOrigen = PaisOrigen(NombrePaisOrigen=NombrePaisOrigen)  # Instanciar un nuevo objeto ModeloLanzamiento
                self.session.add(nuevo_PaisOrigen)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_pais_origen(self):
        try:
            result = self.session.execute(text("SELECT * FROM pais_origen"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_aduana_ingreso(self, NombreAduanaIngreso):
        try:
            existing_record = self.session.query(AduanaIngreso.NombreAduanaIngreso).filter_by(NombreAduanaIngreso=NombreAduanaIngreso).first()
            if not existing_record:
                nuevo_AduanaIngreso = AduanaIngreso(NombreAduanaIngreso=NombreAduanaIngreso)
                self.session.add(nuevo_AduanaIngreso)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_aduana_ingreso(self):
        try:
            result = self.session.execute(text("SELECT * FROM aduana_ingreso"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_pais_aduana(self, IdPaisOrigen, IdAduanaIngreso):
        try:
            existing_record = self.session.query(PaisAduana.IdPaisOrigen, PaisAduana.IdAduanaIngreso).filter_by(IdPaisOrigen=IdPaisOrigen, IdAduanaIngreso = IdAduanaIngreso).first()
            if not existing_record:
                nuevo_PaisAduana = PaisAduana(IdPaisOrigen=IdPaisOrigen, IdAduanaIngreso = IdAduanaIngreso)
                self.session.add(nuevo_PaisAduana)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_pais_aduana(self):
        try:
            result = self.session.execute(text("SELECT * FROM pais_aduana"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def close_session(self):
        self.session.close()
    
    def insert_linea(
            self, 
           nuevos_registros
        ):
        try:
      
            # Realizar la inserción masiva
            self.session.bulk_insert_mappings(Linea, nuevos_registros)

            # Confirmar la transacción
            self.session.commit()
        except IntegrityError as e:
            print(f'Error al insertar linea {e}')
            self.session.rollback()
        finally:
            self.session.close()
            
    def select_linea(self):
        try:
            result = self.session.execute(text("SELECT * FROM linea"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
    '''
    def insert_linea_modelo(self, IdLinea, IdModeloLanzamiento, IdMarca):
        try:
            existing_record = self.session.query(Linea_Modelo.IdLinea, Linea_Modelo.IdModeloLanzamiento, Linea_Modelo.IdMarca).filter_by(IdLinea=IdLinea, IdModeloLanzamiento = IdModeloLanzamiento, IdMarca = IdMarca).first()
            if not existing_record:
                nuevo_linea_modelo = Linea_Modelo(IdLinea=IdLinea, IdModeloLanzamiento = IdModeloLanzamiento, IdMarca = IdMarca)
                self.session.add(nuevo_linea_modelo)  # Agregar el nuevo objeto a la sesión
                self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()
    '''
    def insert_linea_modelo(
            self, 
           nuevos_registros
        ):
        try:
      
            # Realizar la inserción masiva
            self.session.bulk_insert_mappings(Linea_Modelo, nuevos_registros)

            # Confirmar la transacción
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()
            
    def select_linea_modelo(self):
        try:
            result = self.session.execute(text("SELECT * FROM linea_modelo"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_importacion(
            self, 
           nuevos_registros
        ):
        try:
      
            # Realizar la inserción masiva
            self.session.bulk_insert_mappings(Importacion, nuevos_registros)

            # Confirmar la transacción
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()

    def select_importacion(self):
        try:
            result = self.session.execute(text("SELECT * FROM importacion"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()

    def select_importacion_fechas(self):
        try:
            result = self.session.execute(text("SELECT distinct FechaImportacion FROM importacion"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def select_linea_modelo(self):
        try:
            result = self.session.execute(text("SELECT * FROM linea_modelo"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            #logging.error(f"Error al ejecutar la consulta SELECT: {e}", exc_info=True)
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def procesar_script_oltp(self):
        try:
            # Abrir el archivo SQL
            with open('mysql_script/importaciones_db.sql', 'r') as archivo_sql:
                sql_script = archivo_sql.read()

            # Ejecutar el script SQL utilizando la sesión de SQLAlchemy
            try:
                self.session.execute(text(sql_script))
                self.session.commit()
                print("Script SQL ejecutado correctamente.")
            except Exception as e:
                self.session.rollback()  # En caso de error, deshacer los cambios
                print(f"Error al ejecutar el script SQL: {e}")
        finally:
            # Cerrar la sesión de SQLAlchemy
            self.session.close()
        
    def close_session(self):
        self.session.close()
    