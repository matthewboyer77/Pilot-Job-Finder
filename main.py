from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Pilot Job Finder</h1><p>Coming soon!</p>'

@app.route('/api/jobs')
def api_jobs():
    return jsonify([])

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
