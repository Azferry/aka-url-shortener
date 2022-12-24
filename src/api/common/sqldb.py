

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
import urllib
from sqlalchemy import MetaData




class sqldb_ops():
    def __init__(self) -> None:
        server = "akadb.database.windows.net"
        database = "urldb"
        username = "ntcadmin"
        password = "MSFTusa!!2020"
        driver = '{ODBC Driver 17 for SQL Server}'
        odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        self.engine = create_engine(connect_str)
        self.meta = MetaData(bind=self.engine)
        MetaData.reflect(self.meta)

    def insert_shorturl(self, long_url, sub_url):
        # domain_id = Column(Integer)
        # owner_id = Column(Integer)
        short_urls = self.meta.tables['short_urls']
        statement1 = short_urls.insert().values(long_url=long_url, sub_url=sub_url)
        self.engine.execute(statement1)
        return

    def get_longurl(self, sub_url):
        with self.engine.connect() as con:
            query = "SELECT Top(1) long_url FROM short_urls where sub_url='{}'".format(sub_url)

            rs = con.execute(query)
            lu = []
            for row in rs:
                lu.append(row)

        return lu[0][0]



class sqldb_create():
    server = "akadb.database.windows.net"
    database = "urldb"
    username = "ntcadmin"
    password = "MSFTusa!!2020"

    driver = '{ODBC Driver 17 for SQL Server}'

    odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)

    engine = create_engine(connect_str)
    Base = declarative_base()

    class short_urls(Base):
        __tablename__ = 'short_urls'
        id = Column(Integer, primary_key = True)
        long_url = Column(String)
        sub_url = Column(String)
        domain_id = Column(Integer)
        owner_id = Column(Integer)
        create_date = Column(DateTime, server_default=text('GETDATE()'))
        is_deleted = Column(Boolean, server_default=text('0'))

    class domains(Base):
        __tablename__ = 'domains'
        id = Column(Integer, primary_key = True)
        domain_name = Column(String)
        is_deleted = Column(Boolean, server_default=text('0'))

    class metrics(Base):
        __tablename__ = 'metrics'
        id = Column(Integer, primary_key = True)
        url_id = Column(String)
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
    Base.metadata.create_all(engine)

sqldb_create()
# sqldb_ops().insert_shorturl(long_url='test', url_hash='test',url_vanity='ts')
# sqldb_ops().insert_shorturl(long_url='test', url_hash='test')
# sqldb_ops().get_longurl(url_hash='test')
