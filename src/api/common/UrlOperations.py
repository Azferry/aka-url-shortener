import hashlib
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


class UrlOperations():

    def __init__(self) -> None:
        pass
    # @staticmethod
    def hashfx(self, value):
        hash = hashlib.sha1(value.encode("UTF-8")).hexdigest()
        return hash

    # @staticmethod
    def createVanityUrl(self, longUrl, vanityName, hashlen=6):
        url = longUrl
        if "https://" in url:
            url = longUrl.replace("https://", "")
        if "http://" in url:
            url = longUrl.replace("http://", "")

        url_hash = self.hashfx(url)
        shorturl = BASE_URL + '/' + vanityName
        return shorturl

    # @staticmethod
    def createShortUrl(self, longUrl, hashlen=6):
        """createShortUrl creates a short url give the long url

        Args:
            longUrl (_type_): url to be shorten
            hashlen (int, optional): length of hash chars in short url. Defaults to 6.

        Returns:
            str: short url string
        """
        url = longUrl
        if "https://" in url:
            url = longUrl.replace("https://", "")
        if "http://" in url:
            url = longUrl.replace("http://", "")

        url_hash = self.hashfx(url)
        shorturl = BASE_URL + '/' + url_hash[:hashlen]
        return shorturl
