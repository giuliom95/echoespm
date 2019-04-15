from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

from db import db

app = Flask(__name__)
dbconn = db()

import re


@app.route('/', methods=['GET'])
def default():
    return 'Hello world'

