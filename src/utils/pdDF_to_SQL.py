import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def get_engine(user, passwd, host, port, db):
    """
    Esta función genera un motor de bsae de datos de PostgreSQL
    Argumentos:
        user, passwd, host, port, db (string): Credenciales e información de la base de datos para la cual se
        quiere hacer la conexión.
    Salidas:
        engine (object): objeto para hacer la conexión con psql
    
    """
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine

# Código utilizado para leer el archivo generado por la limpieza de Bash y pasarlo a una tabla de SQL
df = pd.read_csv("ticdata2000_wh.txt", sep = "|")
# Credenciales del PostgreSQL que se generó con Docker
engine = get_engine("postgres", "rlgl09dz", "localhost", "5432", "caravanas")
df.to_sql('variables', con = engine, if_exists = 'replace')