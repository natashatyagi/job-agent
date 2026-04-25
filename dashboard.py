import html

class DashboardGenerator:
    def __init__(self):
        pass
    
    def generate_dashboard(self, jobs_data, filename="job_dashboard.html"):
        """
        Generate an interactive HTML dashboard showing all jobs with tailored resumes and cover letters.
        """
        
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px 30px;
            border-radius: 10px;
            color: white;
            backdrop-filter: blur(10px);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .filters {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .filter-group {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        input[type="search"], select {
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        input[type="search"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .jobs-grid {
            display: grid;
            gap: 20px;
        }
        
        .job-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .job-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .job-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            display: flex;
            justify-content: space-between;
            align-items: start;
        }
        
        .job-title-section h2 {
            font-size: 1.4em;
            margin-bottom: 8px;
        }
        
        .job-company {
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .job-meta {
            display: flex;
            gap: 15px;
            margin-top: 10px;
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.85em;
        }
        
        .apply-btn {
            background: white;
            color: #667eea;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .apply-btn:hover {
            background: #f0f0f0;
            transform: scale(1.05);
        }
        
        .job-body {
            padding: 25px;
        }
        
        .job-description {
            margin-bottom: 20px;
            color: #333;
            line-height: 1.6;
        }
        
        .section-title {
            font-size: 1.1em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #667eea;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
        }
        
        .resume-section {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            max-height: 300px;
            overflow-y: auto;
            font-size: 0.95em;
            line-height: 1.5;
            color: #333;
        }
        
        .resume-section pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
        }
        
        .cover-letter-section {
            background: #f0f8ff;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            max-height: 250px;
            overflow-y: auto;
            font-size: 0.95em;
            line-height: 1.6;
            color: #333;
            border-left: 4px solid #667eea;
        }
        
        .copy-button {
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s;
        }
        
        .copy-button:hover {
            background: #764ba2;
        }
        
        .copy-button:active {
            background: #5568d3;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: white;
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
        }
        
        @media (max-width: 768px) {
            .job-header {
                flex-direction: column;
                gap: 15px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            .filters {
                flex-direction: column;
                align-items: stretch;
            }
            
            .filter-group {
                flex-direction: column;
            }
            
            input[type="search"], select {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Job Application Dashboard</h1>
            <p class="subtitle">Tailored resumes and cover letters ready to apply</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">""" + str(len(jobs_data)) + """</div>
                <div class="stat-label">Total Opportunities</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(len(set(j['company'] for j in jobs_data))) + """</div>
                <div class="stat-label">Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">Ready</div>
                <div class="stat-label">To Apply</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <label>Search:</label>
                <input type="search" id="searchInput" placeholder="Filter by company or job title...">
            </div>
            <div class="filter-group">
                <label>Company:</label>
                <select id="companyFilter">
                    <option value="">All Companies</option>
                </select>
            </div>
        </div>
        
        <div class="jobs-grid" id="jobsContainer">
        </div>
    </div>
    
    <script>
        const jobsData = """ + json_to_js_safe(jobs_data) + """;
        
        function renderJobs(jobs) {
            const container = document.getElementById('jobsContainer');
            
            if (jobs.length === 0) {
                container.innerHTML = '<div class="no-results"><h2>No jobs found matching your criteria</h2></div>';
                return;
            }
            
            container.innerHTML = jobs.map((job, index) => `
                <div class="job-card" data-company="${job['company']}" data-index="${index}">
                    <div class="job-header">
                        <div class="job-title-section">
                            <h2>${escapeHtml(job['title'])}</h2>
                            <div class="job-company">${escapeHtml(job['company'])}</div>
                            <div class="job-meta">
                                <span class="badge">${escapeHtml(job['level'])}</span>
                                <span class="badge">${escapeHtml(job['location'])}</span>
                            </div>
                        </div>
                        <a href="${job['url']}" target="_blank" class="apply-btn">View Job</a>
                    </div>
                    
                    <div class="job-body">
                        <div class="job-description">${escapeHtml(job['description'])}</div>
                        
                        <div class="section-title">📄 Tailored Resume</div>
                        <div class="resume-section">
                            <pre>${escapeHtml(job['tailored_resume'])}</pre>
                        </div>
                        <button class="copy-button" onclick="copyToClipboard('resume-${index}')">Copy Resume</button>
                        <textarea id="resume-${index}" style="display:none;">${job['tailored_resume']}</textarea>
                        
                        <div class="section-title">📝 Cover Letter</div>
                        <div class="cover-letter-section">
                            ${escapeHtml(job['cover_letter']).replace(/\\n/g, '<br>')}
                        </div>
                        <button class="copy-button" onclick="copyToClipboard('letter-${index}')">Copy Cover Letter</button>
                        <textarea id="letter-${index}" style="display:none;">${job['cover_letter']}</textarea>
                        
                        <div style="margin-top: 20px;">
                            <a href="${job['url']}" target="_blank" class="apply-btn" style="width: 100%; text-align: center; padding: 15px;">Apply Now →</a>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        function copyToClipboard(elementId) {
            const element = document.getElementById(elementId);
            element.select();
            document.execCommand('copy');
            alert('Copied to clipboard!');
        }
        
        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        }
        
        function setupFilters() {
            const companies = [...new Set(jobsData.map(j => j['company']))].sort();
            const companySelect = document.getElementById('companyFilter');
            companies.forEach(company => {
                const option = document.createElement('option');
                option.value = company;
                option.textContent = company;
                companySelect.appendChild(option);
            });
            
            document.getElementById('searchInput').addEventListener('input', filterJobs);
            document.getElementById('companyFilter').addEventListener('change', filterJobs);
        }
        
        function filterJobs() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const companyFilter = document.getElementById('companyFilter').value;
            
            const filtered = jobsData.filter(job => {
                const matchesSearch = job['title'].toLowerCase().includes(searchTerm) || 
                                     job['company'].toLowerCase().includes(searchTerm);
                const matchesCompany = !companyFilter || job['company'] === companyFilter;
                return matchesSearch && matchesCompany;
            });
            
            renderJobs(filtered);
        }
        
        // Initialize
        setupFilters();
        renderJobs(jobsData);
    </script>
</body>
</html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"Dashboard generated: {filename}")
        return filename


def json_to_js_safe(data):
    """Convert Python dict to safe JavaScript JSON."""
    import json
    return json.dumps(data, ensure_ascii=False)
