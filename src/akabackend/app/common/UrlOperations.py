import hashlib
import os
from os.path import join, dirname
from dotenv import load_dotenv
from app.common.database import sqldb_ops
from app.common.cache import cache
import app.common.utils as util
import time

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


class UrlOperations():

    def __init__(self) -> None:
        self.db_ops = sqldb_ops()
        self.url_cache = cache(db_id=1)
        pass
    
    def checkIfShortUrlExists(self, short_key):
        ch = self.db_ops.exists_shorturl(short_key)
        if ch:
            return True
        return False

    def getLongUrl(self, sub_url):
        lu = self.url_cache.getKey(sub_url)
        longurl = lu
        if lu == None:
            lu = self.db_ops.get_longurl(sub_url)
            longurl = lu.long_url
            if lu == None:
                return None
            self.url_cache.insert(sub_url, lu.long_url)
        if ("https://" or "http://") in longurl:
            return longurl
        else:
            return ("https://" + longurl)

    def hashfx(self, value):
        """hashfx Generate hash from string value

        Args:
            value (str): string value to hash

        Returns:
            str: full hash from value
        """
        hash = hashlib.sha1(value.encode("UTF-8")).hexdigest()
        return hash

    def createShortUrl(self, longUrl, vaniety=None, hashlen=6):
        """createShortUrl creates a short url give the long url

        Args:
            longUrl (_type_): url to be shorten
            hashlen (int, optional): length of hash chars in short url. Defaults to 6.

        Returns:
            str: short url string
        """
        check = util.check_valid_url(longUrl)
        if check == False: 
            return
        if vaniety:
            shorturl = BASE_URL + '/' + vaniety
            self.db_ops.insert_shorturl(longUrl, vaniety)
        else:
            url = longUrl + str(int(time.time()))
            url_hash = self.hashfx(url)
            # ul = self.db_ops.exists_shorturl(url_hash[:hashlen])
            shorturl = BASE_URL + '/' + url_hash[:hashlen]
            self.db_ops.insert_shorturl(longUrl, url_hash[:hashlen])

        return shorturl
