# from pydantic import BaseModel
# from typing import List, Optional

# class SkillEntry(BaseModel):
#     name: str
#     level: Optional[str] = "Intermediate"  # Default placeholder

# class ProjectEntry(BaseModel):
#     name: str
#     description: Optional[str]
#     tech_stack: List[str]
#     stars: int
#     forks: int
#     url: Optional[str]

# class ExperienceEntry(BaseModel):
#     company: str
#     role: str
#     duration: str  # Can be parsed into months/years if needed

# class CandidateProfile(BaseModel):
#     username: str
#     name: Optional[str]
#     bio: Optional[str]
#     public_repos: int
#     followers: int
#     following: int
#     skills: List[SkillEntry]
#     projects: List[ProjectEntry]
#     experiences: List[ExperienceEntry] = []  # Placeholder (GitHub may not include)

from pydantic import BaseModel
from typing import List, Optional

class SkillEntry(BaseModel):
    name: str
    level: Optional[str] = "Intermediate"

class ProjectEntry(BaseModel):
    name: str
    description: Optional[str]
    tech_stack: List[str]
    stars: int
    forks: int
    url: Optional[str]

class ExperienceEntry(BaseModel):
    company: str
    role: str
    duration: str

class CandidateProfile(BaseModel):
    username: str
    name: Optional[str]
    bio: Optional[str]
    public_repos: int
    followers: int
    following: int
    skills: List[SkillEntry]
    projects: List[ProjectEntry]
    experiences: List[ExperienceEntry] = []
    linkedin_data: Optional[str] = None