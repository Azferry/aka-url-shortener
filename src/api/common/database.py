from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
import urllib
from sqlalchemy import MetaData
from dotenv import load_dotenv
import os


load_dotenv()

# Database
SQL_DB_SERVER = os.getenv("SQL_DB_SERVER")
SQL_DB = os.getenv("SQL_DB")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")


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
        short_urls = self.meta.tables['short_urls']
        statement1 = short_urls.insert().values(long_url=long_url, sub_url=sub_url, owner_id=0, domain_id=0)
        self.engine.execute(statement1)
        return

    def exists_shorturl(self, shorturl):
        with self.engine.connect() as con:
            query = "SELECT (CASE WHEN EXISTS(SELECT 1 FROM [dbo].[short_urls] WITH(NOLOCK) WHERE sub_url = '{}' and is_deleted = 0) THEN 1 ELSE 0 END) AS [short_url]".format(shorturl)
            rs = con.execute(query)
            lu = []
            for row in rs:
                lu.append(row)
            if 1 == lu[0][0]:
                return True
        return False


    def get_longurl(self, sub_url):
        with self.engine.connect() as con:
            query = "SELECT Top(1) long_url FROM short_urls where sub_url='{}' and is_deleted = 0".format(sub_url)

            rs = con.execute(query)
            lu = []
            for row in rs:
                lu.append(row)
            if len(lu)>0:
                return lu[0][0]
        return None



# class database():
#     def __init__(self) -> None:
#         pass

#     def get_shorturl(hashKey):
#         return NotImplemented

#     def get_vanityurl(vanityKey):
#         return NotImplemented

#     def add_shorturl(hashKey, userId):
#         return NotImplemented

#     def add_vanityurl(hashKey, vanityName, userId):
#         return NotImplemented

#     def check_hash_exists(hashKey):
#         return NotImplemented

#     def check_vanity_exists(vanityKey):
#         return NotImplemented

#     def add_metric(url_id, operationName="hitcount"):
#         return NotImplemented
