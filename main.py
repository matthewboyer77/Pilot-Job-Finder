from flask import Flask, jsonify, render_template
import os
import json

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/jobs')
def api_jobs():
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
