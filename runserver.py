from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("config.config.BaseConfig")


app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS')
db = SQLAlchemy(app)

from views.views import *


if __name__ == "__main__":
  app.run(host='localhost')
