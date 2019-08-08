import tweepy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'I drink and I know things'
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///j_mikes_bar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Twitter API - Variables for user credentials
ACCESS_TOKEN = '2895347772-W3Zt38VsyKxbo89qhZQ4py1ZVUVojghEA66e3b8'
ACCESS_SECRET = '4Rb1n3kl5pduXoc3tdQefA6QfKsqrxLa3av522CAvB3hx'
CONSUMER_KEY = 'yrTkyVCop7SXd8RL2qeALS5sR'
CONSUMER_SECRET = 'hiifkqG1a0Pi87Jww4dyD0VBokREinn0xtQM0pkmSpOAFJDQRr'
# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)