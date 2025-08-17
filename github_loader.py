# import requests
# from schemas import CandidateProfile, ProjectEntry, SkillEntry

# def get_github_profile(username: str) -> CandidateProfile:
#     user_url = f"https://api.github.com/users/{username}"
#     repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

#     user_data = requests.get(user_url).json()
#     repos_data = requests.get(repos_url).json()

#     skills_set = set()
#     projects = []

#     for repo in repos_data:
#         name = repo["name"]
#         description = repo.get("description", "")
#         stars = repo.get("stargazers_count", 0)
#         forks = repo.get("forks_count", 0)
#         languages_url = repo["languages_url"]
#         repo_url = repo["html_url"]

#         langs = requests.get(languages_url).json()
#         tech_stack = list(langs.keys())
#         skills_set.update(tech_stack)

#         projects.append(ProjectEntry(
#             name=name,
#             description=description,
#             tech_stack=tech_stack,
#             stars=stars,
#             forks=forks,
#             url=repo_url
#         ))

#     skills = [SkillEntry(name=skill) for skill in skills_set]

#     return CandidateProfile(
#         username=user_data["login"],
#         name=user_data.get("name"),
#         bio=user_data.get("bio"),
#         public_repos=user_data.get("public_repos", 0),
#         followers=user_data.get("followers", 0),
#         following=user_data.get("following", 0),
#         skills=skills,
#         projects=projects,
#     )

import requests
from schemas import CandidateProfile, ProjectEntry, SkillEntry

def get_github_profile(username: str) -> CandidateProfile:
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

    user_data = requests.get(user_url).json()
    repos_data = requests.get(repos_url).json()

    skills_set = set()
    projects = []

    for repo in repos_data:
        name = repo["name"]
        description = repo.get("description", "")
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        languages_url = repo["languages_url"]
        repo_url = repo["html_url"]

        langs = requests.get(languages_url).json()
        tech_stack = list(langs.keys())
        skills_set.update(tech_stack)

        projects.append(ProjectEntry(
            name=name,
            description=description,
            tech_stack=tech_stack,
            stars=stars,
            forks=forks,
            url=repo_url
        ))

    skills = [SkillEntry(name=skill) for skill in skills_set]

    return CandidateProfile(
        username=user_data["login"],
        name=user_data.get("name"),
        bio=user_data.get("bio"),
        public_repos=user_data.get("public_repos", 0),
        followers=user_data.get("followers", 0),
        following=user_data.get("following", 0),
        skills=skills,
        projects=projects
    )