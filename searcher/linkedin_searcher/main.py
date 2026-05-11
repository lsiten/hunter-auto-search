"""
领英搜索器实现

注意：本搜索器提供业务逻辑封装和数据处理，浏览器自动化操作
通过 Hermes Agent 的 MCP Chrome 工具完成。详见 skills/linkedin-search/
"""

import re
import time
from typing import Dict, List, Optional, Any

from ..base_searcher import BaseSearcher
from ..models import (
    Candidate, CandidateContact, CandidateExperience, CandidateEducation
)
from utils.log import logger
from utils.cookie_manager import CookieManager
from conf import COOKIES_DIR
from . import selectors


class LinkedInSearcher(BaseSearcher):
    """领英人才搜索器"""

    platform = "linkedin"
    base_url = "https://www.linkedin.com"
    login_url = "https://www.linkedin.com/login"
    search_url = "https://www.linkedin.com/search/results/people/"

    def __init__(self, account: str = "default", headed: bool = True):
        super().__init__(account=account, headed=headed)
        self.cookie_manager = CookieManager(self.platform, account)
        self.platform_name = "领英"

    async def login(self) -> bool:
        """执行登录流程"""
        logger.info(f"[领英] 账号 '{self.account}' 登录流程启动")
        logger.info("  请通过 Hermes Agent 执行以下步骤:")
        logger.info("  1. mcp_chrome_navigate(url='%s')", self.login_url)
        logger.info("  2. 输入账号密码或扫码登录")
        logger.info("  3. 登录成功后调用 save_cookies() 保存 Cookie")
        return False

    def save_cookies(self, cookies: List[Dict]) -> None:
        """保存浏览器 Cookie"""
        self.cookie_manager.save(cookies)
        self._cookies = cookies
        self._is_logged_in = True
        logger.info(f"[领英] Cookie 已保存: {len(cookies)} 条")

    def check_cookie(self) -> bool:
        """检查 Cookie 是否有效"""
        cookies = self.cookie_manager.load()
        if not cookies:
            logger.warning(f"[领英] 账号 '{self.account}' 未找到 Cookie")
            return False

        has_valid_cookie = any(
            c.get("name") in ["li_at", "JSESSIONID"] for c in cookies
        )

        if has_valid_cookie:
            logger.info(f"[领英] 账号 '{self.account}' Cookie 有效")
            self._cookies = cookies
            self._is_logged_in = True
            return True
        else:
            logger.warning(f"[领英] 账号 '{self.account}' Cookie 已过期")
            return False

    def parse_candidate_list(self, page_data: Dict[str, Any]) -> List[Dict]:
        """解析候选人列表页面"""
        candidates = []
        elements = page_data.get("elements", [])

        for elem in elements:
            if "reusable-search__result-container" in elem.get("class", ""):
                candidate = self._parse_list_item(elem)
                if candidate:
                    candidates.append(candidate)

        return candidates

    def _parse_list_item(self, elem: Dict) -> Optional[Dict]:
        """解析单个列表项"""
        try:
            name = self._extract_text(elem, selectors.CANDIDATE_NAME)
            title = self._extract_text(elem, selectors.CANDIDATE_TITLE)
            company = self._extract_text(elem, selectors.CANDIDATE_COMPANY)
            location = self._extract_text(elem, selectors.CANDIDATE_LOCATION)

            href = elem.get("href", "")
            candidate_id = self._extract_id(href)

            if not candidate_id:
                return None

            return {
                "candidate_id": candidate_id,
                "name": name or "未知",
                "title": title,
                "company": company,
                "location": location,
                "profile_url": self.base_url + href if href else None,
            }
        except Exception as e:
            logger.debug(f"解析列表项失败: {e}")
            return None

    def _extract_text(self, elem: Dict, selector: str) -> Optional[str]:
        """从元素中提取文本"""
        children = elem.get("children", [])
        for child in children:
            if selector.replace(".", "") in child.get("class", ""):
                return child.get("text", "").strip()
        return None

    def _extract_id(self, href: str) -> Optional[str]:
        """从链接提取候选人 ID"""
        match = re.search(r"/in/([^/?]+)", href)
        return match.group(1) if match else None

    def parse_candidate_detail(self, detail_data: Dict[str, Any]) -> Candidate:
        """解析候选人详情页面"""
        candidate_id = self._extract_id(detail_data.get("url", "")) or "unknown"

        candidate = Candidate(
            platform=self.platform,
            candidate_id=candidate_id,
            name=self._extract_detail_field(detail_data, "name", "姓名"),
            current_title=self._extract_detail_field(detail_data, "title", "职位"),
            current_company=self._extract_detail_field(detail_data, "company", "公司"),
            location=self._extract_detail_field(detail_data, "location", "所在地"),
            profile_url=detail_data.get("url"),
            collected_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

        candidate.contact = self._parse_contact(detail_data)
        candidate.experiences = self._parse_experiences(detail_data)
        candidate.educations = self._parse_educations(detail_data)
        candidate.skills = self._parse_skills(detail_data)

        return candidate

    def _extract_detail_field(self, data: Dict, field: str, keyword: str) -> Optional[str]:
        """从详情页数据提取字段"""
        text = data.get("text", "")
        html = data.get("html", "")
        pattern = rf"{keyword}[：:]\s*([^\n<]+)"
        match = re.search(pattern, text + html)
        return match.group(1).strip() if match else None

    def _parse_contact(self, data: Dict) -> CandidateContact:
        """解析联系方式"""
        phone = self._extract_detail_field(data, "phone", "手机")
        email = self._extract_detail_field(data, "email", "邮箱")
        return CandidateContact(phone=phone, email=email)

    def _parse_experiences(self, data: Dict) -> List[CandidateExperience]:
        """解析工作经历"""
        return []

    def _parse_educations(self, data: Dict) -> List[CandidateEducation]:
        """解析教育经历"""
        return []

    def _parse_skills(self, data: Dict) -> List[str]:
        """解析技能标签"""
        text = data.get("text", "")
        tag_pattern = r"#(\w+)"
        return list(set(re.findall(tag_pattern, text)))

    async def search(
        self,
        keyword: str,
        city: Optional[str] = None,
        salary: Optional[str] = None,
        experience: Optional[str] = None,
        pages: int = 1,
    ) -> List[Candidate]:
        """执行搜索"""
        if not self.check_cookie():
            logger.error("请先登录！")
            return []

        logger.info(f"[领英] 开始搜索: '{keyword}'")
        logger.info(f"  城市: {city or '不限'}, 页数: {pages}")
        logger.info("  请通过 Hermes Agent 执行搜索流程，详见 skills/linkedin-search/")
        return []
