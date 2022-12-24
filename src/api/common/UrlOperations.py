import hashlib
import os
from os.path import join, dirname
from dotenv import load_dotenv
from common.database import sqldb_ops
from common.cache import cache
import time

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


class UrlOperations():

    def __init__(self) -> None:
        self.db_ops = sqldb_ops()
        self.url_cache = cache(db_id=1)
        pass

    def getLongUrl(self, sub_url):
        lu = self.url_cache.getKey(sub_url)
        if lu == None:
            lu = self.db_ops.get_longurl(sub_url)
            self.url_cache.insert(sub_url, lu)
        if ("https://" or "http://") in lu:
            return lu
        else:
            return ("https://" + lu)

    def hashfx(self, value):
        """hashfx Generate hash from string value

        Args:
            value (str): string value to hash

        Returns:
            str: full hash from value
        """
        hash = hashlib.sha1(value.encode("UTF-8")).hexdigest()
        return hash

    def createShortUrl(self, longUrl, hashlen=6):
        """createShortUrl creates a short url give the long url

        Args:
            longUrl (_type_): url to be shorten
            hashlen (int, optional): length of hash chars in short url. Defaults to 6.

        Returns:
            str: short url string
        """
        url = longUrl + str(int(time.time()))
        if "https://" in url:
            url = longUrl.replace("https://", "")
        if "http://" in url:
            url = longUrl.replace("http://", "")

        url_hash = self.hashfx(url)
        # ul = self.db_ops.exists_shorturl(url_hash[:hashlen])
        shorturl = BASE_URL + '/' + url_hash[:hashlen]
        self.db_ops.insert_shorturl(longUrl, url_hash[:hashlen])

        return shorturl
