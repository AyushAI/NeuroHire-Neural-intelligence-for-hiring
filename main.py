# import json
# from github_loader import get_github_profile

# if __name__ == "__main__":
#     username = input("Enter GitHub username: ").strip()
#     profile = get_github_profile(username)
    
#     # Save structured output
#     with open(f"{username}_profile.json", "w") as f:
#         json.dump(profile.dict(), f, indent=2)

#     print(f"\n✅ Profile JSON saved to: {username}_profile.json")

import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

from github_loader import get_github_profile
from link_loader import scrape_linkedin_profile
from schemas import CandidateProfile

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_job_spec(path="job_spec.json"):
    with open(path, "r") as f:
        return json.load(f)

def format_input_for_llm(profile: CandidateProfile, job_spec: dict) -> str:
    skills = [skill.name for skill in profile.skills]
    projects = [
        {
            "name": p.name,
            "description": p.description,
            "tech_stack": p.tech_stack,
            "stars": p.stars,
            "forks": p.forks
        } for p in profile.projects
    ]

    linkedin_text = f"\nLinkedIn Data:\n{profile.linkedin_data}" if profile.linkedin_data else ""

    return f"""
You are an expert hiring analyst.

GitHub Profile:
Name: {profile.name or profile.username}
Bio: {profile.bio}
Skills: {skills}
Followers: {profile.followers}, Following: {profile.following}
Total Public Repos: {profile.public_repos}

Projects:
{json.dumps(projects, indent=2)}
{linkedin_text}

Job Specification:
{json.dumps(job_spec, indent=2)}

Instructions:
1. Summarize the candidate's profile in 2-3 bullet points.
2. Highlight the top 3 project contributions.
3. Create a skill matrix comparing required and desired skills.
4. Compute a Fit Score (0-100).
5. Give a 1-paragraph hiring recommendation.

Respond in JSON format with keys: summary, top_projects, skill_matrix, fit_score, recommendation.
""".strip()

def analyze_with_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

def run_analyzer(username: str, linkedin_url: str = None, job_spec_path="job_spec.json"):
    print("📦 Fetching GitHub profile...")
    profile = get_github_profile(username)

    if linkedin_url:
        print("🔗 Scraping LinkedIn profile...")
        profile.linkedin_data = scrape_linkedin_profile(linkedin_url)

    print("📄 Loading job spec...")
    job_spec = load_job_spec(job_spec_path)

    print("🧠 Sending prompt to Gemini...")
    prompt = format_input_for_llm(profile, job_spec)
    response = analyze_with_gemini(prompt)

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        parsed = {"raw_text": response}

    report = {
        "candidate": {
            "username": profile.username,
            "name": profile.name,
            "bio": profile.bio
        },
        "fit_analysis": parsed
    }

    out_file = f"{username}_analysis_report.json"
    with open(out_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ Report saved to: {out_file}")

if __name__ == "__main__":
    github_username = input("Enter GitHub username: ").strip()
    linkedin_url = input("Enter LinkedIn profile URL (or leave blank): ").strip() or None
    run_analyzer(github_username, linkedin_url)
