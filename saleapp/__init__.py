from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
from flask_socketio import SocketIO
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from joblib import dump, load

app = Flask(__name__)

app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/quanlythoigian?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


cloudinary.config(
    cloud_name = "dhffue7d7",
    api_key = "215425482852391",
    api_secret = "a9xaGBMJr7KgKhJa-1RpSpx_AmU"
)

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
socketio = SocketIO(app)
