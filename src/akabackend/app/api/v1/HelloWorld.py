from flask import Blueprint

app_name = __name__.split(".")[-1]
app = Blueprint(app_name, app_name)

@app.route('/v1/test/')
def test_page():
    return 'Hello World'
