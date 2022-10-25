from mimetypes import init
import pandas as pd
from sqlalchemy import create_engine


DATABASE = 'PostgreSQL'



class ModifyDatabase():
    def __init__(self) -> None:
        pass
    
    def engine(self, user:str='admin', password:str='', host:str='localhost', company:str='Andolina'):
        '''
        https://mariadb.com/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/
        Define the MariaDB engine using MariaDB Connector/Python
        
        https://docs.sqlalchemy.org/en/14/core/engines.html#postgresql
        The PostgreSQL dialect uses psycopg2 as the default DBAPI. Other PostgreSQL DBAPIs include pg8000 and asyncpg:
        psycopg2
        '''
        database_dict = {'MariaDB': 'mariadb+mariadbconnector',
                         'PostgreSQL': 'postgresql+psycopg2'}
        
        engine = create_engine(f'{database_dict[DATABASE]}://{user}:{password}@{host}/{company}')
        
    
    # Write DataFrame to SQL
    
    '''
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()
    '''