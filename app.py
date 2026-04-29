from flask import Flask, render_template, request, jsonify, send_file
import os
from dotenv import load_dotenv
from job_processor import JobProcessor
import json

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    """Serve the main form"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_jobs():
    """
    Process resume and stream job opportunities as they're generated
    """
    try:
        from flask import stream_with_context
        
        # Get form data
        resume_file = request.files.get('resume')
        api_key = request.form.get('api_key')
        skills = request.form.getlist('skills[]')
        locations = request.form.getlist('locations[]')
        level = request.form.get('level')
        dream_companies = request.form.get('dream_companies', '')
        companies_count = int(request.form.get('companies_count', 50))
        max_jobs = int(request.form.get('max_jobs', 20))
        
        # Enforce limits
        companies_count = min(50, max(1, companies_count))
        max_jobs = min(50, max(1, max_jobs))

        # Validate inputs
        if not resume_file or not api_key or not skills or not locations:
            return jsonify({'error': 'Missing required fields'}), 400

        # Read resume
        resume_text = resume_file.read().decode('utf-8', errors='ignore')
        processor = JobProcessor(api_key)

        # Generate companies
        target_companies = processor.generate_companies(
            skills=skills,
            locations=locations,
            level=level,
            count=companies_count,
            dream_companies=dream_companies
        )

        # Get jobs
        jobs = processor.get_jobs(target_companies, max_jobs=max_jobs)

        def stream_jobs():
            """Generator to stream jobs as they're processed"""
            # Send metadata
            yield 'data: ' + json.dumps({
                'type': 'metadata',
                'skills': skills,
                'locations': locations,
                'level': level,
                'total_jobs': len(jobs),
                'total_companies': len(target_companies)
            }) + '\n\n'
            
            # Process and stream each job
            for i, job in enumerate(jobs):
                tailored_resume = processor.tailor_resume(
                    resume_text, job['title'], job['description'], job['company']
                )
                cover_letter = processor.generate_cover_letter(
                    resume_text, job['title'], job['description'], job['company']
                )
                
                job['tailored_resume'] = tailored_resume
                job['cover_letter'] = cover_letter
                
                # Stream job immediately
                yield 'data: ' + json.dumps({
                    'type': 'job',
                    'job': job,
                    'progress': {'current': i + 1, 'total': len(jobs)}
                }) + '\n\n'
            
            # Send completion
            yield 'data: ' + json.dumps({'type': 'complete'}) + '\n\n'

        return app.response_class(
            stream_with_context(stream_jobs()),
            mimetype='text/event-stream',
            headers={'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Serve dashboard template"""
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
