# candidate_fit_analyzer

An automated system for evaluating a candidate's suitability for a given job using both **GitHub** and **LinkedIn** profile data, analyzed by **Google Gemini LLM**.

---

## 🚀 Features
- ✅ Fetches structured data from **GitHub API**
- ✅ Scrapes LinkedIn profile data using **Playwright**
- ✅ Summarizes and evaluates using **Gemini 2.5 Pro**
- ✅ Generates:
  - Profile Summary
  - Top Project Contributions
  - Skill Matrix
  - Fit Score
  - Hiring Recommendation
- ✅ Output saved as a structured JSON report

---

## 📁 Folder Structure
```
candidate_fit_analyzer/
├── .env                     # Store your Gemini API Key
├── job_spec.json            # Job requirements in JSON
├── schemas.py               # Pydantic models for profile data
├── github_loader.py         # GitHub profile extractor
├── linkedin_scraper.py      # LinkedIn profile scraper (Playwright)
├── main.py                  # Main script to run the analysis
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/candidate_fit_analyzer.git
cd candidate_fit_analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**`requirements.txt` should include:**
```
playwright
pydantic
python-dotenv
google-generativeai
requests
```

### 3. Install Playwright Browsers
```bash
playwright install
```

### 4. Add Your Gemini API Key
Create a `.env` file:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 🛠️ How It Works
1. **GitHub Data**: Extracted using public API (`followers`, `repos`, `languages`, `stars` etc.)
2. **LinkedIn Data**: Scraped from your profile (experience, education, headline, etc.)
3. **LLM Prompt**: Combined data sent to Gemini for analysis
4. **Output**: JSON file with recommendation, score, and skill matrix

---

## 🧪 Run the Tool
```bash
python main.py
```
Then follow the prompts:
```text
Enter GitHub username: johndoe
Enter LinkedIn profile URL (or leave blank): https://linkedin.com/in/johndoe
```

Output is saved as:
```bash
johndoe_analysis_report.json
```

---

## 📄 Sample `job_spec.json`
```json
{
  "title": "Full Stack Developer",
  "required_skills": ["React", "Node.js", "PostgreSQL", "Docker"],
  "desired_skills": ["TypeScript", "GraphQL", "CI/CD", "Kubernetes"],
  "min_github_stars": 50,
  "description": "We are seeking a full stack engineer to build scalable web apps and APIs with modern tools."
}
```

---

## 📌 Notes
- Ensure your LinkedIn profile is public and viewable
- GitHub token is not required for public data
- Use only for personal/resume evaluation or internal HR prototyping
