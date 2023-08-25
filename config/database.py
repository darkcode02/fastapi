# Importamos el módulo 'os' para interactuar con el sistema operativo y 'create_engine', 'sessionmaker' y 'declarative_base' desde SQLAlchemy.
import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre del archivo de la base de datos SQLite que vamos a crear o utilizar.
sqlite_file_name = "../database.sqlite"

# Obtenemos el directorio base del archivo actual (donde se encuentra este código).
base_dir = os.path.dirname(os.path.realpath(__file__))

# Creamos la URL de la base de datos concatenando el protocolo SQLite con la ruta completa al archivo de la base de datos.
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Creamos un motor SQLAlchemy que se conectará a la base de datos utilizando la URL que construimos.
# El argumento 'echo=True' significa que el motor imprimirá las declaraciones SQL que se ejecutan en la consola.
engine = create_engine(database_url, echo=True)

# Creamos una clase 'Session' utilizando 'sessionmaker' que nos permitirá crear sesiones para interactuar con la base de datos.
# La sesión se vincula al motor que creamos anteriormente.
Session = sessionmaker(bind=engine)

# Creamos una clase base declarativa utilizando 'declarative_base' de SQLAlchemy.
# Esta clase se utilizará como base para definir nuestras clases de modelo (tablas) en la base de datos.
Base = declarative_base()
