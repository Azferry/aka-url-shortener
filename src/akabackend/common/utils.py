
import validators

# url='https://microsoft-my.sharepoint.com/:w:/p/ryanferry/EeXUlRrL_llDh2YrAaJ6tjUBMOBEe20dchuVUXPtSKZ1Tg?e=aJnhKs'
def check_valid_url(url):
    try:
        vu = validators.url(url)
        if vu == True:
            return True
        return False
    except:
        return False
    