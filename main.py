#!/usr/bin/env python3
"""
Job Application Agent
Generates 50 target companies, scrapes jobs, tailors resumes and cover letters,
outputs interactive HTML dashboard ready to apply.
"""

import sys
from agent import JobAgent
from dashboard import DashboardGenerator

def main():
    print("=" * 70)
    print("JOB APPLICATION AGENT")
    print("=" * 70)
    
    # Read resume from file
    resume_path = "resume.txt"
    try:
        with open(resume_path, 'r') as f:
            resume_text = f.read()
        print(f"\n✓ Loaded resume from {resume_path}")
    except FileNotFoundError:
        print(f"\n✗ Resume file not found: {resume_path}")
        print("  Please create resume.txt with your resume content")
        sys.exit(1)
    
    # User preferences
    print("\n" + "=" * 70)
    print("YOUR PREFERENCES")
    print("=" * 70)
    
    skills = "Android, Full Stack, Backend, Solidity"
    location = "Bay Area, Seattle, Remote"
    
    print(f"Skills: {skills}")
    print(f"Location: {location}")
    print(f"Level: Mid-level (L4/E4/IC4)")
    
    # Initialize agent
    print("\n" + "=" * 70)
    print("STARTING AGENT")
    print("=" * 70)
    
    try:
        agent = JobAgent()
        print("\n✓ Connected to Gemini API")
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("  Make sure GEMINI_API_KEY is set in .env file")
        sys.exit(1)
    
    # Step 1: Generate target companies
    print("\n[1/4] Generating target companies...")
    companies = agent.generate_target_companies(skills, location, count=50)
    
    if not companies:
        print("✗ Failed to generate companies")
        sys.exit(1)
    
    print(f"✓ Generated {len(companies)} target companies")
    
    # Step 2: Get jobs from companies
    print("\n[2/4] Scraping job listings...")
    jobs = agent.get_mock_jobs(companies, max_jobs=80)
    
    if not jobs:
        print("✗ No jobs found")
        sys.exit(1)
    
    print(f"✓ Found {len(jobs)} job opportunities")
    
    # Step 3: Tailor resumes and generate cover letters
    print("\n[3/4] Tailoring resumes and generating cover letters...")
    print("      (This may take a minute...)")
    
    jobs_with_tailored_content = []
    
    for i, job in enumerate(jobs):
        print(f"  Processing {i+1}/{len(jobs)}: {job['company']} - {job['title']}")
        
        # Tailor resume
        tailored_resume = agent.tailor_resume(
            resume_text,
            job['title'],
            job['description'],
            job['company']
        )
        
        # Generate cover letter
        cover_letter = agent.generate_cover_letter(
            resume_text,
            job['title'],
            job['description'],
            job['company']
        )
        
        job['tailored_resume'] = tailored_resume
        job['cover_letter'] = cover_letter
        jobs_with_tailored_content.append(job)
    
    print(f"✓ Processed {len(jobs_with_tailored_content)} jobs")
    
    # Step 4: Generate dashboard
    print("\n[4/4] Generating interactive dashboard...")
    
    dashboard_gen = DashboardGenerator()
    dashboard_file = dashboard_gen.generate_dashboard(jobs_with_tailored_content)
    
    print(f"✓ Dashboard created: {dashboard_file}")
    
    # Summary
    print("\n" + "=" * 70)
    print("AGENT COMPLETE")
    print("=" * 70)
    print(f"\n✓ {len(jobs_with_tailored_content)} jobs ready to apply")
    print(f"✓ Open {dashboard_file} in your browser")
    print(f"✓ Click 'Apply Now' for each job")
    print(f"✓ Tailored resume and cover letter already prepared")
    print("\nGood luck! 🚀")

if __name__ == "__main__":
    main()
