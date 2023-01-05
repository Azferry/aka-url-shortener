import datetime
from sqlalchemy import MetaData
from common.snowflake import IdWorker
from common.sqldb import domains, short_urls, sql_conn_helper
# from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker

# load_dotenv()

SQL_DB_SERVER = os.getenv("SQL_DB_SERVER")
SQL_DB01 = os.getenv("SQL_DB01")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")

SNOW_FLAKE_DC_ID = os.getenv("DATACENTER_ID", "localhost")
if os.getenv("HOST_TYPE", "localhost").lower() == "azwebapp":
    SNOW_FLAKE_INSTANCE_ID = os.getenv("WEBSITE_INSTANCE_ID")#, "localhost")
else:
    SNOW_FLAKE_INSTANCE_ID = os.getenv("INSTANCE_ID", "localhost")


class sqldb_ops():
    def __init__(self) -> None:
        sq = sql_conn_helper(server=SQL_DB_SERVER,userid=SQL_USER,database=SQL_DB01,password=SQL_PWD)
        self.engine = sq.new_sql_engine()
        self.meta = MetaData(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.worker = IdWorker(worker_id=SNOW_FLAKE_INSTANCE_ID, datacenter_id=SNOW_FLAKE_DC_ID, sequence=0)
        MetaData.reflect(self.meta)
        self.delete_shorturl('ap')

    def insert_shorturl(self, long_url, sub_url):
        snow = self.worker.get_id()
        su = short_urls(long_url=long_url, sub_url=sub_url, snowflake_id=snow)
        s = self.session()
        s.add(su)
        s.commit()
        s.close()
        return

    def delete_shorturl(self, sub_url):
        s = self.session()
        s.query(short_urls).\
            filter(short_urls.sub_url == sub_url ).\
            update({'is_deleted': True, 'delete_date': datetime.datetime.now()})
        s.flush()
        s.commit()
        s.close()
        return

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
        """get_longurl given the sub url return the long url.

        Args:
            sub_url (str): sub url key

        Returns:
            str: returns only the first entry found or none
        """
        s = self.session()
        r  = s.query(short_urls).filter(short_urls.sub_url==sub_url).first()
        s.close()
        return r
        # session.query(User).filter(User.id == 1)