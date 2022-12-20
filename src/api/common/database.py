
class database():
    def __init__(self) -> None:
        pass

    def get_shorturl(hashKey):
        return NotImplemented

    def get_vanityurl(vanityKey):
        return NotImplemented

    def add_shorturl(hashKey, userId):
        return NotImplemented

    def add_vanityurl(hashKey, vanityName, userId):
        return NotImplemented

    def check_hash_exists(hashKey):
        return NotImplemented

    def check_vanity_exists(vanityKey):
        return NotImplemented

    def add_metric(url_id, operationName="hitcount"):
        return NotImplemented
