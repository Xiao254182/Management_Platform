from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:000000@127.0.0.1/database'
app.config['SECRET_KEY'] = '000000'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)
