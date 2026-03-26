from flask import Flask, jsonify

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
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
        .subtitle { color: #4a5568; font-size: 1.1rem; }
        .jobs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .job-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .job-title { font-size: 1.2rem; color: #1a365d; margin-bottom: 8px; }
        .job-company { color: #4a5568; margin-bottom: 5px; }
        .loading { text-align: center; padding: 40px; color: #718096; }
    </style>
</head>
<body>
    <div class="container">
        <header>
                    <h1>✈️ Pilot Job Finder</h1>
            <p class="subtitle">Curated pilot opportunities from across the web</p>
        </header>
        <div class="jobs-grid" id="jobsGrid">
            <p class="loading">Loading pilot jobs...</p>
        </div>
    </div>
    <script>
        async function loadJobs() {
            try {
                const response = await fetch('/api/jobs');
                const jobs = await response.json();
                const grid = document.getElementById('jobsGrid');
                if (jobs.length === 0) {
                    grid.innerHTML = '<p class="loading">No jobs yet. Check back soon!</p>';
                                    } else {
                    grid.innerHTML = jobs.map(job => '<div class="job-card"><h3 class="job-title">' + job.title + '</h3><p class="job-company">' + job.company + '</p></div>').join('');
                }
            } catch (e) {
                document.getElementById('jobsGrid').innerHTML = '<p class="loading">Error loading jobs.</p>';
            }
        }
        loadJobs();
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return HTML
    @app.route('/api/jobs')
def api_jobs():
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
