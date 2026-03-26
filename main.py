from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

DATA_FILE = 'pilot_jobs.json'

def scrape_jobs():
    """Scrape pilot jobs from Indeed"""
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
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pilot Job Finder</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: #f5f7fa; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 40px; }
        h1 { color: #1a365d; font-size: 2.5rem; margin-bottom: 10px; }
        .subtitle { color: #4a5568; font-size: 1.1rem; margin-bottom: 30px; }
        .filters { background: white; padding: 15px; border-radius: 12px; margin-bottom: 20px; display: flex; gap: 15px; }
        input { padding: 10px; border: 1px solid #ddd; border-radius: 8px; flex: 1; }
        .jobs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .job-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .job-source { background: #ebf8ff; color: #2b6cb0; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; display: inline-block; margin-bottom: 10px; }
        .job-title { font-size: 1.2rem; color: #1a365d; margin-bottom: 8px; }
                .job-company { color: #4a5568; }
        .job-location { color: #718096; font-size: 0.9rem; margin-top: 5px; }
        .job-link { display: inline-block; background: #3182ce; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>✈️ Pilot Job Finder</h1>
            <p class="subtitle">Curated pilot opportunities from across the web</p>
        </header>
        <div class="filters">
            <input type="text" id="searchInput" placeholder="Search jobs...">
        </div>
        <div class="jobs-grid" id="jobsGrid">
                    <p>Loading jobs...</p>
        </div>
    </div>
    <script>
        let allJobs = [];
        async function loadJobs() {
            try {
                const res = await fetch('/api/jobs');
                allJobs = await res.json();
                renderJobs(allJobs);
            } catch(e) { document.getElementById('jobsGrid').innerHTML = 'Error loading jobs'; }
        }
        function renderJobs(jobs) {
            const grid = document.getElementById('jobsGrid');
            if(!jobs.length) { grid.innerHTML = 'No jobs found'; return; }
                        grid.innerHTML = jobs.map(j => '<div class="job-card"><span class="job-source">Indeed</span><h3 class="job-title">'+j.title+'</h3><p class="job-company">'+j.company+'</p><p class="job-location">'+j.location+'</p><a href="'+j.url+'" target="_blank" class="job-link">View Job</a></div>').join('');
        }
        document.getElementById('searchInput').addEventListener('input', e => {
            const q = e.target.value.toLowerCase();
            renderJobs(allJobs.filter(j => j.title.toLowerCase().includes(q) || j.company.toLowerCase().includes(q)));
        });
        loadJobs();
    </script>
</body>
</html>'''

@app.route('/api/jobs')
def api_jobs():
    # If no cached jobs, scrape now
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
