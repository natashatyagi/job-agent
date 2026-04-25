# Job Application Agent

An AI-powered agent that generates target companies, finds job listings, tailors your resume and cover letters, and outputs an interactive dashboard ready to apply.

## Features

- **Intelligent company selection**: Generates 50 target companies based on your skills and location
- **Job scraping**: Collects up to 80 job opportunities across target companies
- **Resume tailoring**: Customizes your resume for each specific job
- **Cover letter generation**: Creates personalized cover letters for every opportunity
- **Interactive dashboard**: Browse all jobs with tailored materials in one place
- **Ready to apply**: Everything prepared—just copy and apply

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your Gemini API key

Edit `.env` file:
```
GEMINI_API_KEY=your-actual-key-here
```

Get your free API key from: https://ai.google.dev/aistudio

### 3. Verify your resume

The agent reads from `resume.txt`. This file is pre-populated with your resume from the PDF, but you can edit it if needed.

## Usage

```bash
python3 main.py
```

The script will:
1. Load your resume
2. Generate 50 target companies (based on skills: Android, Full Stack, Backend, Solidity)
3. Scrape job listings from those companies
4. Tailor your resume for each job
5. Generate a personalized cover letter for each job
6. Create `job_dashboard.html`

### 4. Open the dashboard

```bash
open job_dashboard.html
# or
# double-click the file in your file explorer
```

You'll see:
- All job opportunities
- Tailored resume for each job
- Personalized cover letter
- Click "View Job" to see the posting
- Click "Copy Resume" / "Copy Cover Letter" to prepare
- Click "Apply Now" to go to the application

## How It Works

### Target Company Generation
The agent uses Gemini to intelligently generate companies based on:
- Your skills (Android, Backend, Full Stack, Solidity)
- Location preferences (Bay Area, Seattle, Remote)
- Your experience level (Mid-level, 6 YoE = L4/E4/IC4)

Starting points: Google, Meta, OpenAI, Anthropic, Scale AI, Coinbase, Stripe, etc.

### Resume Tailoring
For each job:
1. Analyzes the job description
2. Identifies relevant skills and experience from your resume
3. Reorders bullet points to highlight the most relevant work
4. Keeps your original resume structure intact

### Cover Letter Generation
Creates warm, personal cover letters that:
- Show genuine interest in the company and role
- Highlight 1-2 key accomplishments from your resume
- Are personal (not stiff or formal)
- Include a clear call to action

## Customization

### Change preferences

Edit `main.py` and update:
```python
skills = "Android, Full Stack, Backend, Solidity"
location = "Bay Area, Seattle, Remote"
```

### Adjust company count

Change in `main.py`:
```python
companies = agent.generate_target_companies(skills, location, count=50)  # adjust 50
```

### Adjust job count

Change in `agent.py`:
```python
def get_mock_jobs(self, companies, max_jobs=80):  # adjust 80
```

## Tips

1. **Review before applying** — The dashboard is a starting point. Customize cover letters per company if you want
2. **Apply consistently** — Aim to apply to 3-5 jobs per day for better results
3. **Track applications** — Note which companies you've applied to
4. **Follow up** — After 1-2 weeks with no response, consider a follow-up email

## Limitations (MVP)

- Currently uses mock job data for speed (real scraping would take longer)
- To integrate real company scraping, update `get_mock_jobs()` in `agent.py`
- Cover letters are 1-shot generated (not iteratively improved)

## Next Steps

1. Add real company career page scraping
2. Integrate with LinkedIn API for live job feeds
3. Add application tracking (which jobs you've applied to)
4. Add follow-up reminders
5. Support multiple resumes for different role types

## License

MIT

## Questions?

Check the dashboard HTML or re-run the agent if you want fresh results.

Good luck with your applications! 🚀
