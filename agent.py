import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class JobAgent:
    def __init__(self, api_key=None):
        """Initialize the job agent with Gemini API."""
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY not provided")
        
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Base companies to build from
        self.base_companies = [
            "Google", "Meta", "OpenAI", "Anthropic", "Scale AI",
            "Coinbase", "Stripe", "Plaid", "Block", "Wise",
            "Apple", "Amazon", "Netflix", "Microsoft", "Salesforce",
            "Airbnb", "Uber", "DoorDash", "Twitch", "Discord"
        ]
    
    def generate_target_companies(self, skills, location, count=50):
        """
        Use Gemini to intelligently generate target companies based on skills and location.
        """
        prompt = f"""You are a career advisor helping identify the best tech companies for a job search.

CANDIDATE PROFILE:
- Skills: {skills}
- Location preference: {location}
- Target level: Mid-level engineer (6 years YoE, L4/E4/IC4 equivalent)
- Interests: Full-stack, Backend, Android/Mobile, Blockchain

BASE COMPANIES (already considering): {', '.join(self.base_companies)}

Generate a JSON list of {count} companies that:
1. Are actively hiring engineers with these skills
2. Match location preferences (Bay Area, Seattle, Remote)
3. Are known for paying well and respecting engineers
4. Span startups, scale-ups, and established tech

For each company, provide:
- "name": company name
- "type": "FAANG" | "Fintech" | "Crypto" | "Startup" | "Other"
- "location": primary hiring location
- "career_url": estimated careers page URL (e.g., careers.google.com, jobs.stripe.com)
- "skill_match": 1-10 score for how well it matches the skills

Return ONLY valid JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            text = response.text
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
            return []
    
    def tailor_resume(self, original_resume, job_title, job_description, company_name):
        """
        Tailor resume for a specific job by highlighting relevant bullet points.
        """
        prompt = f"""You are an expert resume coach. Given a candidate's resume and a specific job posting, 
tailor the resume to highlight the most relevant experience.

IMPORTANT RULES:
1. Keep the original resume structure and order of roles (chronological)
2. Do NOT move entire roles around
3. Within each role, reorder or emphasize bullet points that match the job
4. Add relevance scores (internal - not shown) to bullets
5. Keep the same formatting as the original

ORIGINAL RESUME:
{original_resume}

TARGET JOB:
Company: {company_name}
Title: {job_title}
Description: {job_description}

Return the tailored resume in the same format as the original, with bullet points reordered/emphasized 
to match the job requirements. Start with the most relevant experience first within each role."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error tailoring resume: {e}")
            return original_resume
    
    def generate_cover_letter(self, resume_text, job_title, job_description, company_name):
        """
        Generate a personalized cover letter for a specific job.
        """
        prompt = f"""Write a personal, warm cover letter for this job application.

CANDIDATE RESUME:
{resume_text}

JOB DETAILS:
Company: {company_name}
Title: {job_title}
Description: {job_description}

Requirements:
- Personal and warm tone (not formal/stiff)
- 3-4 paragraphs
- Show genuine interest in the company and role
- Highlight 1-2 key accomplishments from resume that match the role
- End with clear call to action
- Keep it under 250 words

Return ONLY the cover letter text, no headers or additional formatting."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return ""
    
    def get_mock_jobs(self, companies, max_jobs=80):
        """
        For MVP, use mock job data since real scraping would take too long.
        In production, this would scrape company career pages.
        """
        mock_jobs = [
            {
                "company": "Google",
                "title": "Senior Software Engineer - Android",
                "level": "L4",
                "location": "Mountain View, CA",
                "url": "https://careers.google.com/jobs/results/senior-software-engineer-android/",
                "description": "Build Android apps for Google Play. Experience with Kotlin, Jetpack, performance optimization required."
            },
            {
                "company": "Meta",
                "title": "Software Engineer - Backend Infrastructure",
                "level": "E4",
                "location": "Menlo Park, CA",
                "url": "https://www.metacareers.com/jobs/senior-software-engineer-backend/",
                "description": "Design and build backend systems. AWS, Java, system design expertise needed."
            },
            {
                "company": "Stripe",
                "title": "Senior Backend Engineer - Payments",
                "level": "IC4",
                "location": "San Francisco, CA",
                "url": "https://stripe.com/jobs/listing/senior-backend-engineer/",
                "description": "Build payment infrastructure. REST APIs, PostgreSQL, system scalability required."
            },
            {
                "company": "Coinbase",
                "title": "Senior Software Engineer - Blockchain",
                "level": "L4",
                "location": "San Francisco, CA",
                "url": "https://www.coinbase.com/careers/positions/senior-blockchain-engineer/",
                "description": "Build on-chain systems. Solidity, Ethereum, smart contracts expertise required."
            },
            {
                "company": "OpenAI",
                "title": "Senior Software Engineer - Infrastructure",
                "level": "IC4",
                "location": "San Francisco, CA",
                "url": "https://openai.com/careers/senior-software-engineer/",
                "description": "Build ML infrastructure. Python, distributed systems, scale required."
            },
            {
                "company": "Scale AI",
                "title": "Backend Engineer - Data Platform",
                "level": "IC4",
                "location": "San Francisco, CA",
                "url": "https://scale.com/careers/backend-engineer/",
                "description": "Build data infrastructure. SQL, Python, API design required."
            },
            {
                "company": "Plaid",
                "title": "Senior Software Engineer - Fintech",
                "level": "IC4",
                "location": "San Francisco, CA",
                "url": "https://plaid.com/careers/senior-engineer/",
                "description": "Build fintech APIs. REST APIs, banking integrations, security required."
            },
            {
                "company": "Wise",
                "title": "Software Engineer - Payments",
                "level": "IC4",
                "location": "San Francisco, CA",
                "url": "https://wise.com/careers/engineer/",
                "description": "Build cross-border payment systems. Distributed systems, reliability required."
            },
            {
                "company": "Apple",
                "title": "Senior Software Engineer - iOS",
                "level": "L4",
                "location": "Cupertino, CA",
                "url": "https://www.apple.com/careers/us/jobs.html",
                "description": "Build iOS apps. Swift, performance, user experience critical."
            },
            {
                "company": "Netflix",
                "title": "Senior Backend Engineer - Platform",
                "level": "L4",
                "location": "Los Gatos, CA",
                "url": "https://jobs.netflix.com/search?q=senior-backend/",
                "description": "Build streaming infrastructure at scale. Java, Kubernetes, observability."
            },
            {
                "company": "Block",
                "title": "Senior Software Engineer - Cash App",
                "level": "L4",
                "location": "San Francisco, CA",
                "url": "https://www.block.xyz/careers/search?query=senior-backend/",
                "description": "Build Cash App backend. Kotlin, Android, financial systems experience needed."
            },
            {
                "company": "Anthropic",
                "title": "Senior Software Engineer - Infrastructure",
                "level": "IC4",
                "location": "San Francisco, CA",
                "url": "https://www.anthropic.com/careers",
                "description": "Build AI infrastructure. Python, distributed systems, ML ops required."
            }
        ]
        
        # Return sample jobs (in reality would be 80)
        return mock_jobs[:max_jobs]
