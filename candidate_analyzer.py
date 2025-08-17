import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
from github_loader import get_github_profile
from schemas import CandidateProfile

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---- Load job specification ----
def load_job_spec(path="job_spec.json"):
    with open(path, "r") as f:
        return json.load(f)

# ---- Format input for Gemini ----
def format_input_for_llm(profile: CandidateProfile, job_spec: dict) -> str:
    skills = [skill.name for skill in profile.skills]
    projects = [
        {
            "name": p.name,
            "description": p.description,
            "tech_stack": p.tech_stack,
            "stars": p.stars,
            "forks": p.forks,
        }
        for p in profile.projects
    ]

    return f"""
You are an expert hiring analyst.

A candidate has the following GitHub profile:

Name: {profile.name or profile.username}
Bio: {profile.bio}
Skills: {skills}
Followers: {profile.followers}, Following: {profile.following}
Total Public Repos: {profile.public_repos}

Projects:
{json.dumps(projects, indent=2)}

The job specification is:
{json.dumps(job_spec, indent=2)}

Instructions:
1. Summarize the candidate's profile in 2-3 bullet points.
2. Highlight the top 3 project contributions with 1-line summaries.
3. Create a skill matrix comparing required and desired skills with the candidate's.
4. Compute a Fit Score (0-100).
5. Give a 1-paragraph hiring recommendation.
Respond in valid JSON format with keys: summary, top_projects, skill_matrix, fit_score, recommendation.
""".strip()

# ---- Call Gemini ----
def analyze_with_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# ---- Main Function ----
def run_analyzer(username: str, job_spec_path="job_spec.json"):
    print("📦 Loading GitHub profile...")
    profile = get_github_profile(username)

    print("📄 Loading job specification...")
    job_spec = load_job_spec(job_spec_path)

    print("🧠 Sending data to Gemini LLM...")
    prompt = format_input_for_llm(profile, job_spec)
    analysis_output = analyze_with_gemini(prompt)

    try:
        parsed_output = json.loads(analysis_output)
    except json.JSONDecodeError:
        print("⚠️ Gemini response not valid JSON. Saving raw text.")
        parsed_output = {"raw_text": analysis_output}

    report = {
        "candidate": {
            "username": profile.username,
            "name": profile.name,
            "bio": profile.bio,
        },
        "fit_analysis": parsed_output,
    }

    out_file = f"{username}_analysis_report.json"
    with open(out_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ Report saved to: {out_file}")

if __name__ == "__main__":
    github_username = input("Enter GitHub username: ").strip()
    run_analyzer(github_username)