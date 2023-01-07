from flask import Blueprint, redirect
from app.common.UrlOperations import UrlOperations
app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)


@app.route('/<string:shortcode>')
def baseRedirect(shortcode):
    urlOps = UrlOperations()
    ul = urlOps.getLongUrl(shortcode)
    if ul == None:
        return
    return redirect(ul)
