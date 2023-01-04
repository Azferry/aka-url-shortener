import validators

def check_valid_url(url):
    try:
        vu = validators.url(url)
        if vu == True:
            return True
        return False
    except:
        return False
    