# Here, we add a secret key:

from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecf6e975838a2f7bf3c5dbe7d55ebe5b'  ###

# from flask_sqlalchemy import SQLAlchemy
# flask.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
# db = SQLAlchemy(flask)
