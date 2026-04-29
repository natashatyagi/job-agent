# Job Agent v2

An intelligent job application assistant that tailors your resume and generates cover letters for each opportunity.

## Features

- 📄 **Upload Resume** — PDF or TXT format
- ⚡ **Select Skills** — Choose your technical skills (Android, Backend, Solidity, etc.)
- 📍 **Set Locations** — Pick preferred job locations
- 🔑 **Use Your API Key** — Bring your own Gemini API key (free tier available)
- 🎯 **Get Tailored Content** — Resume and cover letter customized for each job
- 📊 **Interactive Dashboard** — Search, filter, and copy tailored materials

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Gemini API Key

1. Go to https://ai.google.dev/aistudio
2. Click "Get API key"
3. Create a new key in Google Cloud
4. Copy the key (you'll paste it in the app)

### 3. Run the App

```bash
python app.py
```

The app will start at `http://localhost:5000`

### 4. Open in Browser

- Go to http://localhost:5000
- Upload your resume
- Select your skills and locations
- Paste your Gemini API key
- Click "Generate Opportunities"

## How It Works

1. **Form Submission** — You upload resume, select preferences, and provide API key
2. **Company Generation** — App generates 50 target companies based on your profile
3. **Job Scraping** — Fetches job listings from target companies
4. **Resume Tailoring** — Uses Gemini to customize your resume for each job
5. **Cover Letter** — Generates personalized cover letter for each opportunity
6. **Dashboard** — Shows all opportunities with tailored materials ready to copy

## File Structure

```
job-agent-v2/
├── app.py                 # Flask app main entry
├── job_processor.py       # Core logic with Gemini API
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main form
│   └── dashboard.html    # Results dashboard
└── README.md             # This file
```

## Usage Flow

1. **Upload Resume** — TXT or PDF
2. **Select Skills** — Click dropdown, choose skills (Android, Python, Solidity, etc.)
3. **Select Locations** — Bay Area, Remote, Seattle, NY, etc.
4. **Choose Level** — Junior, Mid-level, Senior, Staff+
5. **Enter API Key** — Your free Gemini API key
6. **Click Generate** — App processes everything (2-3 minutes)
7. **Review Dashboard** — See all tailored opportunities
8. **Copy & Apply** — Copy resume and cover letter, apply on company website

## Notes

- Your API key is **never saved** — it's used only for this session
- Resume is **not stored** — processed immediately and discarded
- All processing happens **locally** on your machine
- You apply **manually** to each job (for safety and control)

## Troubleshooting

**"No module named flask"**
```bash
pip install flask
```

**"API key invalid"**
- Make sure you copied the full key from ai.google.dev
- Don't include extra spaces

**"Processing takes too long"**
- Tailoring resumes + generating cover letters takes 2-3 minutes for 20 jobs
- This is normal with Gemini API

## Future Improvements

- Real company career page scraping (beyond mock data)
- Support for more API providers
- Auto-apply functionality (optional)
- Application tracking
- Cover letter customization per job

## License

MIT - Use freely, modify as needed

## Questions?

Check the code comments or refer to Gemini API docs: https://ai.google.dev/
