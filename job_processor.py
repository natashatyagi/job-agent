import google.generativeai as genai
import json

class JobProcessor:
    def __init__(self, api_key):
        """Initialize with user's Gemini API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def generate_companies(self, skills, locations, level, count=50, dream_companies=''):
        """Generate target companies based on user profile"""
        
        dream_list = [c.strip() for c in dream_companies.split(',') if c.strip()] if dream_companies else []
        dream_text = f"Priority companies: {', '.join(dream_list)}\n" if dream_list else ""
        
        prompt = f"""You are a career advisor helping identify the best tech companies for a job search.

CANDIDATE PROFILE:
- Skills: {', '.join(skills)}
- Location preferences: {', '.join(locations)}
- Target level: {level}
{dream_text}

Generate a JSON list of {count} companies that:
1. Are actively hiring engineers with these skills
2. Match location preferences
3. {f"Include priority companies listed above + similar ones" if dream_list else "Span startups, mid-size, and established tech"}
4. Are known for fair compensation and culture

For each company, provide:
- "name": company name
- "type": "FAANG" | "Fintech" | "Crypto" | "Startup" | "Other"
- "location": primary hiring location
- "career_url": careers page URL (estimate if needed)

Return ONLY valid JSON array, no other text."""

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extract JSON
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            else:
                json_str = text.strip()
            
            companies = json.loads(json_str)
            return companies
        except Exception as e:
            print(f"Error generating companies: {e}")
            # Return mock companies if API fails
            return self.get_mock_companies()
    
    def get_mock_companies(self):
        """Mock companies for testing"""
        return [
            {"name": "Google", "type": "FAANG", "location": "Bay Area, CA", "career_url": "careers.google.com"},
            {"name": "Meta", "type": "FAANG", "location": "Bay Area, CA", "career_url": "metacareers.com"},
            {"name": "Stripe", "type": "Fintech", "location": "Bay Area, CA", "career_url": "stripe.com/jobs"},
            {"name": "Coinbase", "type": "Crypto", "location": "Bay Area, CA", "career_url": "coinbase.com/careers"},
            {"name": "OpenAI", "type": "Other", "location": "Bay Area, CA", "career_url": "openai.com/careers"},
        ]
    
    def get_jobs(self, companies, max_jobs=20):
        """Get sample jobs from companies"""
        
        sample_jobs = [
            {
                "company": "Google",
                "title": "Senior Android Engineer",
                "level": "L4",
                "location": "Bay Area, CA",
                "url": "https://careers.google.com/jobs/",
                "description": "Build Android apps at scale. Kotlin, Jetpack Compose expertise required."
            },
            {
                "company": "Meta",
                "title": "Software Engineer - Mobile",
                "level": "E4",
                "location": "Remote",
                "url": "https://metacareers.com/jobs/",
                "description": "Build mobile infrastructure. React Native, system design expertise needed."
            },
            {
                "company": "Stripe",
                "title": "Backend Engineer - Payments",
                "level": "IC4",
                "location": "Bay Area, CA",
                "url": "https://stripe.com/jobs",
                "description": "Build payment infrastructure. REST APIs, PostgreSQL, system design expertise needed."
            },
            {
                "company": "Coinbase",
                "title": "Senior Software Engineer - Blockchain",
                "level": "L4",
                "location": "Bay Area, CA",
                "url": "https://coinbase.com/careers",
                "description": "Build on-chain systems. Solidity, Ethereum, smart contracts expertise required."
            },
            {
                "company": "OpenAI",
                "title": "Senior Software Engineer - Infrastructure",
                "level": "IC4",
                "location": "Remote",
                "url": "https://openai.com/careers",
                "description": "Build ML infrastructure. Python, distributed systems expertise required."
            },
        ]
        
        return sample_jobs[:max_jobs]
    
    def tailor_resume(self, original_resume, job_title, job_description, company_name):
        """Tailor resume for specific job"""
        
        prompt = f"""You are an expert resume coach. Given a candidate's resume and a specific job posting, 
tailor the resume to highlight the most relevant experience.

IMPORTANT:
1. Keep the original resume structure and chronological order
2. Do NOT move entire roles around
3. Within each role, emphasize bullet points matching the job
4. Keep same formatting as original
5. Return ONLY the tailored resume text

ORIGINAL RESUME:
{original_resume}

TARGET JOB:
Company: {company_name}
Title: {job_title}
Description: {job_description}

Return the tailored resume with bullet points reordered to match job requirements."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error tailoring resume: {e}")
            return original_resume
    
    def generate_cover_letter(self, resume_text, job_title, job_description, company_name):
        """Generate personalized cover letter"""
        
        prompt = f"""Write a personal, warm cover letter for this job application.

CANDIDATE RESUME:
{resume_text}

JOB DETAILS:
Company: {company_name}
Title: {job_title}
Description: {job_description}

Requirements:
- Personal and warm tone (not formal/stiff)
- 3-4 paragraphs max
- Show genuine interest in the company and role
- Highlight 1-2 key accomplishments from resume
- End with clear call to action
- Keep under 250 words
- Return ONLY the cover letter text, no headers"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return "Unable to generate cover letter"
