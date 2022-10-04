from flask import Flask
import os
from flask_ngrok import run_with_ngrok
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
run_with_ngrok(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024