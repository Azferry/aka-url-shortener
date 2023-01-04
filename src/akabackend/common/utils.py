import validators

def check_valid_url(url):
    """check_valid_url validates url

    Args:
        url (str): URL to verify

    Returns:
        bool: true or false if the site is valid
    """
    try:
        if ("https://" or "http://") not in url:
            url = ("https://" + url)
        vu = validators.url(url)
        if vu == True:
            return True
        return False
    except:
        return False
    