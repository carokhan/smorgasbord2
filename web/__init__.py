from flask import Flask

app = Flask(__name__)
app.config["STATIC_FOLDER"] = 'static'
app.config["TEMPLATES_FOLDER"] = 'templates'

from web import routes



