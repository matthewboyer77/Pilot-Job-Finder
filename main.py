from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/jobs')
def api_jobs():
    return jsonify([])
