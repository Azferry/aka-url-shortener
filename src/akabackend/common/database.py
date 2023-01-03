from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
import urllib
from sqlalchemy import MetaData
from common.snowflake import IdWorker
from common.sqldb import domains, short_urls, sql_conn_helper
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQL_DB_SERVER = os.getenv("SQL_DB_SERVER")
SQL_DB01 = os.getenv("SQL_DB01")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")

SNOW_FLAKE_DC_ID = os.getenv("SNOW_FLAKE_DC_ID", "localhost")
SNOW_FLAKE_INSTANCE_ID = os.getenv("SNOW_FLAKE_INSTANCE_ID", "localhost")


class sqldb_ops():
    def __init__(self) -> None:
        sq = sql_conn_helper(server=SQL_DB_SERVER,userid=SQL_USER,database=SQL_DB01,password=SQL_PWD)
        self.engine = sq.new_sql_engine()
        self.meta = MetaData(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.worker = IdWorker(worker_id=SNOW_FLAKE_INSTANCE_ID, datacenter_id=SNOW_FLAKE_DC_ID, sequence=0)
        MetaData.reflect(self.meta)

    def insert_shorturl(self, long_url, sub_url):
        snow = self.worker.get_id()
        su = short_urls(long_url=long_url, sub_url=sub_url, snowflake_id=snow)
        s = self.session()
        s.add(su)
        s.commit()
        s.close()
        return

    # def insert_shorturl(self, long_url, sub_url):
    #     short_urls = self.meta.tables['short_urls']
    #     snow = self.worker.get_id()
    #     statement1 = short_urls.insert().values(snowflake_id=int(snow),long_url=long_url, sub_url=sub_url, owner_id=0, domain_id=0)
    #     self.engine.execute(statement1)
    #     return

    def insert_domain(self, domain_name):
        s = self.session()
        dn = domains(domain_name)
        s.add(dn)
        s.commit()
        s.close()
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