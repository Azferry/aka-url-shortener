
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, text, BigInteger, and_
from sqlalchemy.ext.declarative import declarative_base
# from flask_sqlalchemy import SQLAlchemy
import urllib
from sqlalchemy import MetaData
from dotenv import load_dotenv
load_dotenv()
SQL_DB_SERVER = os.getenv("SQL_DB_SERVER")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")
SQL_DB01 = os.getenv("SQL_DB01")

class sql_conn_helper():
    """sql_conn_helper - Produces connection strings and engines for connection
    """
    def __init__(self, server, userid, database, password, port="1433") -> None:
        """__init__ 

        Args:
            server (str): server host dns entry
            userid (str): username for the connection to sql
            database (str): name of the database
            password (str): password for the connection to sql
            port (str, optional): SQL Server Port. Defaults to "1433".
        """
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.port = port
        self.server = server
        self.userid = userid
        self.database = database
        self.password = password
        self.connstr = ""
        pass

    def create_pyodbcstr(self):
        """create_pyodbcstr build a connection string for pyodbc

        Returns:
            str: build out connection string
        """
        odbc_str = 'DRIVER='+ self.driver+';SERVER='+ self.server+';PORT='+self.port+';UID='+self.userid+';DATABASE='+ self.database + ';PWD='+ self.password
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        self.connstr = connect_str
        return connect_str
    
    def new_sql_engine(self):
        """new_sql_engine Create sql engine for connection

        Returns:
            sql_engine: engine for sql connection
        """
        st = self.create_pyodbcstr()
        engine = create_engine(st)
        return engine

sq = sql_conn_helper(server=SQL_DB_SERVER,userid=SQL_USER,database=SQL_DB01,password=SQL_PWD)
engine = sq.new_sql_engine()
Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)
    return

class short_urls(Base):
    __tablename__ = 'short_urls'
    snowflake_id = Column(BigInteger, primary_key = True)
    long_url = Column(String)
    sub_url = Column(String)
    domain_id = Column(Integer)
    owner_id = Column(BigInteger)
    create_date = Column(DateTime, server_default=text('GETDATE()'))
    is_deleted = Column(Boolean, server_default=text('0'))

    def __init__(self, snowflake_id, long_url, sub_url, domain_id=0, owner_id=0):
        self.snowflake_id = snowflake_id
        self.long_url = long_url
        self.sub_url = sub_url
        self.domain_id = domain_id
        self.owner_id = owner_id
    
    def to_json(self):
        return dict(snowflake_id=self.snowflake_id,
                    long_url=self.long_url, 
                    sub_url=self.sub_url,
                    domain_id = self.domain_id,
                    owner_id = self.owner_id,
                    create_date = self.create_date,
                    is_deleted = self.is_deleted)
    def __repr__(self):
        return f'<short_urls {self.sub_url}>'

    # def __eq__(self, other):
    #     return type(self) is type(other) and self.snowflake_id == other.snowflake_id

    def __ne__(self, other):
        return not self.__eq__(other)



class domains(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key = True)
    domain_name = Column(String)
    is_deleted = Column(Boolean, server_default=text('0'))

    def __init__(self, domain_name):
        self.domain_name = domain_name


class metrics(Base):
    __tablename__ = 'metrics'
    id = Column(BigInteger, primary_key = True)
    url_snowflake_id = Column(BigInteger,nullable=False)
    timestamp = Column(DateTime, server_default=text('GETDATE()'))
    operation_name = Column(String)

class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    first_name = Column(String)
    is_deleted = Column(Boolean, server_default=text('0'))

# class secs(Base):
#     __tablename__ = 'secndtble'
#     id = Column(Integer, primary_key = True)
#     invid = Column(Integer, ForeignKey('test3.id'))
#     fts = relationship("Fits", back_populates = "secndtble")
# Fits.secndtble = relationship("secs", order_by = secs.id, back_populates = "fts")

# from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation

# db = sessionmaker(bind=engine)
# # Base.query = db.query_property()
# dn = domains("He")
# # base..add(dn)
# db.commit()

# Base.