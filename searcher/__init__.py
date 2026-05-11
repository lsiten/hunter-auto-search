"""
Hunter Auto Search - 招聘平台自动化搜索模块
"""
from .base_searcher import BaseSearcher
from .boss_searcher import BossSearcher
from .liepin_searcher import LiepinSearcher
from .linkedin_searcher import LinkedInSearcher
from .maimai_searcher import MaimaiSearcher
from .models import (
    CandidateContact,
    CandidateExperience,
    CandidateEducation,
    Candidate,
    SearchResult,
)

__all__ = [
    "BaseSearcher",
    "BossSearcher",
    "LiepinSearcher",
    "LinkedInSearcher",
    "MaimaiSearcher",
    "CandidateContact",
    "CandidateExperience",
    "CandidateEducation",
    "Candidate",
    "SearchResult",
]

# 版本信息
__version__ = "0.1.0"
