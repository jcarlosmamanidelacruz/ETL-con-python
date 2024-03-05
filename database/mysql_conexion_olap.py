from sqlalchemy import Column, Integer, UniqueConstraint, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import logging
import os
from datetime import datetime

Base = declarative_base()

class dim_paisorigen(Base):
    __tablename__ = 'dim_paisorigen'
    
    IdPaisOrigen = Column(Integer, primary_key=True)
    NombrePaisOrigen = Column(String(45), nullable=False)
  
class dim_aduanaingreso(Base):
    __tablename__ = 'dim_aduanaingreso'
    
    IdAduanaIngreso = Column(Integer, primary_key=True)
    NombreAduanaIngreso = Column(String(45), nullable=False)

class dim_paisaduana(Base):
    __tablename__ = 'dim_paisaduana'
    
    IdPais_IdAduana = Column(Integer, primary_key=True)
    IdPaisOrigen = Column(Integer, nullable=False)
    IdAduanaIngreso = Column(Integer, nullable=False)

class dim_fecha(Base):
    __tablename__ = 'dim_fecha'
    
    IdFecha = Column(Integer, primary_key=True)
    FechaImportacion = Column(Date, nullable=False)
    Anio = Column(Integer, nullable=False)
    Mes = Column(Integer, nullable=False)
    Mes_nombre = Column(String(45), nullable=False)

class fac_importaciones(Base):
    __tablename__ = 'fac_importacion'
    
    IdPais_IdAduana = Column(Integer, primary_key=True)
    IdFecha = Column(Integer, primary_key=True)
    ValorCIF = Column(Float, nullable=False)
    Impuesto = Column(Float, nullable=False)
  
class MySQLConexion_olap:

    def __init__(self, db_url):        
        self.engine = create_engine(db_url) # crea un motor SQLAlchemy  pasando como argumento la url de la base de datos
        self.Session = sessionmaker(bind=self.engine) # crear sesion ORM con la base de datos
        self.session = self.Session() # sesión utilizada para realizar operaciones de base de datos

        log_directory = "log_error_proceso"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_file = os.path.join(log_directory, f"error_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

        # Configurar el registro de errores
        logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
          
    def insert_dim_paisorigen(self, IdPaisOrigen, NombrePaisOrigen):
        try:
            existing_record = self.session.query(dim_paisorigen.IdPaisOrigen, dim_paisorigen.NombrePaisOrigen).filter_by(IdPaisOrigen=IdPaisOrigen, NombrePaisOrigen=NombrePaisOrigen).first()
            nuevo_dim_paisorigen = dim_paisorigen(IdPaisOrigen=IdPaisOrigen, NombrePaisOrigen=NombrePaisOrigen)  # Instanciar un nuevo objeto ModeloLanzamiento
            self.session.add(nuevo_dim_paisorigen)  # Agregar el nuevo objeto a la sesión
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
        finally:
            self.session.close()
            
    def select_dim_paisorigen(self):
        try:
            result = self.session.execute(text("SELECT * FROM dim_paisorigen"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_dim_aduanaingreso(self, IdAduanaIngreso, NombreAduanaIngreso):
        try:
            existing_record = self.session.query(dim_aduanaingreso.IdAduanaIngreso, dim_aduanaingreso.NombreAduanaIngreso).filter_by(IdAduanaIngreso=IdAduanaIngreso, NombreAduanaIngreso=NombreAduanaIngreso).first()
            nuevo_dim_aduanaingreso = dim_aduanaingreso(IdAduanaIngreso=IdAduanaIngreso, NombreAduanaIngreso=NombreAduanaIngreso)  # Instanciar un nuevo objeto ModeloLanzamiento
            self.session.add(nuevo_dim_aduanaingreso)  # Agregar el nuevo objeto a la sesión
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
        finally:
            self.session.close()

    def select_dim_aduanaingreso(self):
        try:
            result = self.session.execute(text("SELECT * FROM dim_aduanaingreso"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()
            
    def insert_dim_paisaduana(self, IdPais_IdAduana, IdPaisOrigen, IdAduanaIngreso):
        try:
            existing_record = self.session.query(dim_paisaduana.IdPais_IdAduana, dim_paisaduana.IdPaisOrigen, dim_paisaduana.IdAduanaIngreso).filter_by(IdPais_IdAduana=IdPais_IdAduana, IdPaisOrigen=IdPaisOrigen, IdAduanaIngreso=IdAduanaIngreso).first()
            nuevo_dim_paisaduana = dim_paisaduana(IdPais_IdAduana=IdPais_IdAduana, IdPaisOrigen=IdPaisOrigen, IdAduanaIngreso=IdAduanaIngreso)
            self.session.add(nuevo_dim_paisaduana)  # Agregar el nuevo objeto a la sesión
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
        finally:
            self.session.close()

    def select_dim_paisaduana(self):
        try:
            result = self.session.execute(text("SELECT * FROM dim_paisaduana"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()

    def insert_dim_fecha(self, IdFecha, FechaImportacion, Anio, Mes, Mes_nombre):
        try:
            existing_record = self.session.query(dim_fecha.IdFecha).filter_by(IdFecha=IdFecha).first()
            nuevo_dim_fecha = dim_fecha(IdFecha=IdFecha, FechaImportacion=FechaImportacion, Anio=Anio, Mes=Mes, Mes_nombre=Mes_nombre)
            self.session.add(nuevo_dim_fecha)  # Agregar el nuevo objeto a la sesión
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
        finally:
            self.session.close()

    def select_dim_fecha(self):
        try:
            result = self.session.execute(text("SELECT * FROM dim_fecha"))
            marcas = result.fetchall()
            return marcas
        except Exception as e:
            print(f"Error al ejecutar la consulta SELECT: {e}")
            return None
        finally:
            # Cerrar la sesión para liberar recursos
            self.session.close()

    def insert_fac_importaciones(self, nuevos_registros):
        try:
            # Realizar la inserción masiva
            self.session.bulk_insert_mappings(fac_importaciones, nuevos_registros)

            # Confirmar la transacción
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
        finally:
            self.session.close()
            
    def procesar_script_olap(self):
            
        # Abrir el archivo SQL
        with open('mysql_script/importaciones_OLAP.sql', 'r') as archivo_sql:
            sql_script = archivo_sql.read()

        # Ejecutar el script SQL utilizando la sesión de SQLAlchemy
        try:
            self.session.execute(text(sql_script))
            self.session.commit()
            print("Script SQL ejecutado correctamente.")
        except Exception as e:
            logging.error(f"Error al ejecutar la consulta SELECT: {e}", exc_info=True)
            self.session.rollback()  # En caso de error, deshacer los cambios
            print(f"Error al ejecutar el script SQL: {e}")
        finally:
            # Cerrar la sesión de SQLAlchemy
            self.session.close()