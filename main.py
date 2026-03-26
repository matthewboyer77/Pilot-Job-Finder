from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/jobs')
def api_jobs():
    return jsonify([])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
