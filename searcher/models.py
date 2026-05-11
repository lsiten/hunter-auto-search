"""
候选人数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CandidateContact(BaseModel):
    """联系方式"""
    phone: Optional[str] = None
    email: Optional[str] = None
    wechat: Optional[str] = None
    linkedin: Optional[str] = None


class CandidateExperience(BaseModel):
    """工作经历"""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class CandidateEducation(BaseModel):
    """教育经历"""
    school: str
    degree: str
    major: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[str] = None


class Candidate(BaseModel):
    """候选人核心数据模型"""
    # 来源信息
    platform: str = Field(description="平台: liepin/boss/linkedin/maimai")
    candidate_id: str = Field(description="平台内唯一 ID")
    
    # 基础信息
    name: str = Field(description="姓名")
    avatar_url: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None
    current_residence: Optional[str] = None
    
    # 职业状态
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    current_industry: Optional[str] = None
    current_salary: Optional[str] = None
    expected_salary: Optional[str] = None
    work_years: Optional[str] = None
    
    # 求职状态
    job_status: Optional[str] = Field(default=None, description="求职状态: 在职-考虑机会/在职-暂不考虑/离职-正在找工作等")
    
    # 详细经历
    experiences: List[CandidateExperience] = Field(default_factory=list, description="工作经历列表")
    educations: List[CandidateEducation] = Field(default_factory=list, description="教育经历列表")
    skills: List[str] = Field(default_factory=list, description="技能标签列表")
    
    # 联系方式
    contact: CandidateContact = Field(default_factory=CandidateContact)
    
    # 自我描述
    summary: Optional[str] = None
    
    # 元数据
    profile_url: Optional[str] = None
    last_active: Optional[str] = None
    collected_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    search_keyword: Optional[str] = None
    
    # 原始数据 (用于调试)
    raw_data: Optional[dict] = Field(default=None, exclude=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "platform": "boss",
                "candidate_id": "xxx123",
                "name": "张三",
                "current_title": "高级 Python 开发工程师",
                "current_company": "某知名互联网公司",
                "location": "北京",
                "skills": ["Python", "Django", "MySQL", "Redis"],
            }
        }


class SearchResult(BaseModel):
    """搜索结果封装"""
    keyword: str
    platform: str
    account: str
    total_count: int = 0
    candidates: List[Candidate] = Field(default_factory=list)
    page: int = 1
    has_more: bool = False
    error: Optional[str] = None
    search_time: str = Field(default_factory=lambda: datetime.now().isoformat())


__all__ = [
    "CandidateContact",
    "CandidateExperience",
    "CandidateEducation",
    "Candidate",
    "SearchResult",
]
