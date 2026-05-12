from typing import Optional
from pydantic import BaseModel, Field


class ResumeSchema(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    experiences: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    years_of_experience: Optional[int] = None
    industry_tags: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    job_id: str
    match_score: int
    is_information_complete: bool
    missing_dimensions: list[str] = Field(default_factory=list)
    skill_score: int
    experience_score: int
    industry_score: int
    education_score: int
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    reasoning: str
