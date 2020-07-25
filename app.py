from flask import Flask, request
from function import parse
import os
import requests
app = Flask(__name__)

@app.route('/', methods=['POST'])
def caller():
    return parse(request)
