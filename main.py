from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)
DATA_FILE = 'pilot_jobs.json'

def scrape_jobs():
    jobs = []
    try:
        url = "https://www.indeed.com/jobs?q=pilot&l=USA"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for job in soup.select('.job-card')[:15]:
            title = job.select_one('.job-title')
            company = job.select_one('.company-name')
            location = job.select_one('.company-location')
            link = job.select_one('a')
            
            if title:
                jobs.append({
                    'title': title.get_text(strip=True),
                    'company': company.get_text(strip=True) if company else 'N/A',
                    'location': location.get_text(strip=True) if location else 'N/A',
                    'url': 'https://www.indeed.com' + link.get('href') if link else '#'
                })
    except Exception as e:
        print(f"Scraper error: {e}")
    return jobs

@app.route('/')
def index():
    return '<h1>Pilot Job Finder</h1><p>Loading...</p>'

@app.route('/api/jobs')
def api_jobs():
    if not os.path.exists(DATA_FILE):
        jobs = scrape_jobs()
        with open(DATA_FILE, 'w') as f:
            json.dump(jobs, f)
    else:
        with open(DATA_FILE, 'r') as f:
            jobs = json.load(f)
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
