"""
BOSS 直聘搜索器实现

注意：本搜索器提供业务逻辑封装和数据处理，浏览器自动化操作
通过 Hermes Agent 的 MCP Chrome 工具完成。详见 skills/boss-search/
"""

import json
import re
import time
from typing import Dict, List, Optional, Any
from pathlib import Path

from ..base_searcher import BaseSearcher
from ..models import (
    Candidate, CandidateContact, CandidateExperience, CandidateEducation
)
from utils.log import logger
from utils.cookie_manager import CookieManager
from conf import COOKIES_DIR
from . import selectors


class BossSearcher(BaseSearcher):
    """BOSS 直聘招聘者端人才搜索器"""

    platform = "boss"
    base_url = "https://www.zhipin.com"
    login_url = "https://www.zhipin.com/web/user/"
    search_url = "https://www.zhipin.com/chat/geek"

    def __init__(self, account: str = "default", headed: bool = True):
        super().__init__(account=account, headed=headed)
        self.cookie_manager = CookieManager(self.platform, account)
        self.platform_name = "BOSS 直聘"

    async def login(self) -> bool:
        """
        执行登录流程 - 返回登录状态

        注意：实际浏览器操作由 Hermes Agent 通过 MCP Chrome 完成
        本方法处理登录后的 Cookie 保存逻辑

        使用 Skill 中的登录流程:
        1. chrome_navigate(login_url)
        2. chrome_read_page() 识别二维码
        3. 等待用户扫码 (screenshot + wait)
        4. 调用本方法保存 Cookie
        """
        logger.info(f"[BOSS] 账号 '{self.account}' 登录流程启动")
        logger.info("  请通过 Hermes Agent 执行以下步骤:")
        logger.info("  1. mcp_chrome_navigate(url='%s')", self.login_url)
        logger.info("  2. 等待二维码出现并扫码")
        logger.info("  3. 登录成功后调用 save_cookies() 保存 Cookie")
        return False

    def save_cookies(self, cookies: List[Dict]) -> None:
        """保存浏览器 Cookie"""
        self.cookie_manager.save(cookies)
        self._cookies = cookies
        self._is_logged_in = True
        logger.info(f"[BOSS] Cookie 已保存: {len(cookies)} 条")

    def check_cookie(self) -> bool:
        """检查 Cookie 是否有效"""
        cookies = self.cookie_manager.load()
        if not cookies:
            logger.warning(f"[BOSS] 账号 '{self.account}' 未找到 Cookie")
            return False

        # 简单的有效性检查（可后续通过实际请求验证）
        has_valid_cookie = any(
            c.get("name") in ["__zp_stoken__", "t"] for c in cookies
        )

        if has_valid_cookie:
            logger.info(f"[BOSS] 账号 '{self.account}' Cookie 有效")
            self._cookies = cookies
            self._is_logged_in = True
            return True
        else:
            logger.warning(f"[BOSS] 账号 '{self.account}' Cookie 已过期")
            return False

    def parse_candidate_list(self, page_data: Dict[str, Any]) -> List[Dict]:
        """
        解析候选人列表页面数据

        Args:
            page_data: chrome_read_page() 返回的页面数据

        Returns:
            候选人简要信息列表
        """
        candidates = []

        # 根据实际页面结构解析
        # 这里提供解析逻辑，实际数据由 MCP 工具获取后传入
        elements = page_data.get("elements", [])

        for elem in elements:
            if "geek-item" in elem.get("class", ""):
                candidate = self._parse_list_item(elem)
                if candidate:
                    candidates.append(candidate)

        return candidates

    def _parse_list_item(self, elem: Dict) -> Optional[Dict]:
        """解析单个列表项"""
        try:
            text = elem.get("text", "")
            html = elem.get("html", "")

            # 提取基本信息
            name = self._extract_text(elem, selectors.CANDIDATE_NAME)
            title = self._extract_text(elem, selectors.CANDIDATE_TITLE)
            company = self._extract_text(elem, selectors.CANDIDATE_COMPANY)
            salary = self._extract_text(elem, selectors.CANDIDATE_EXPECTED_SALARY)
            location = self._extract_text(elem, selectors.CANDIDATE_LOCATION)
            work_years = self._extract_text(elem, selectors.CANDIDATE_WORK_YEARS)

            # 提取 ID
            href = elem.get("href", "") or re.search(r'href="([^"]+)"', html).group(1) if re.search(r'href="([^"]+)"', html) else ""
            candidate_id = self._extract_id(href)

            if not candidate_id:
                return None

            return {
                "candidate_id": candidate_id,
                "name": name or "未知",
                "title": title,
                "company": company,
                "expected_salary": salary,
                "location": location,
                "work_years": work_years,
                "profile_url": self.base_url + href if href else None,
            }
        except Exception as e:
            logger.debug(f"解析列表项失败: {e}")
            return None

    def _extract_text(self, elem: Dict, selector: str) -> Optional[str]:
        """从元素中提取文本"""
        # 实际实现需要根据 chrome_read_page 的返回结构调整
        children = elem.get("children", [])
        for child in children:
            if selector.replace(".", "") in child.get("class", ""):
                return child.get("text", "").strip()
        return None

    def _extract_id(self, href: str) -> Optional[str]:
        """从链接提取候选人 ID"""
        match = re.search(r"/chat/geek/(\w+)", href)
        return match.group(1) if match else None

    def parse_candidate_detail(self, detail_data: Dict[str, Any]) -> Candidate:
        """
        解析候选人详情页面，返回结构化数据

        Args:
            detail_data: chrome_read_page() 返回的详情页数据

        Returns:
            Candidate 结构化对象
        """
        elements = detail_data.get("elements", [])
        html = detail_data.get("html", "")
        text = detail_data.get("text", "")

        # 基本信息（从详情页提取完整信息）
        candidate_id = self._extract_id(detail_data.get("url", "")) or "unknown"

        # 构建基础候选人对象
        candidate = Candidate(
            platform=self.platform,
            candidate_id=candidate_id,
            name=self._extract_detail_field(detail_data, "name", "姓名"),
            current_title=self._extract_detail_field(detail_data, "title", "职位"),
            current_company=self._extract_detail_field(detail_data, "company", "公司"),
            current_salary=self._extract_detail_field(detail_data, "current_salary", "当前薪资"),
            expected_salary=self._extract_detail_field(detail_data, "expected_salary", "期望薪资"),
            location=self._extract_detail_field(detail_data, "location", "所在地"),
            age=self._extract_age(detail_data),
            gender=self._extract_gender(detail_data),
            profile_url=detail_data.get("url"),
            collected_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

        # 解析联系方式
        candidate.contact = self._parse_contact(detail_data)

        # 解析工作经历
        candidate.experiences = self._parse_experiences(detail_data)

        # 解析教育经历
        candidate.educations = self._parse_educations(detail_data)

        # 解析技能标签
        candidate.skills = self._parse_skills(detail_data)

        # 最后活跃时间
        candidate.last_active = self._extract_detail_field(detail_data, "last_active", "最后活跃")

        return candidate

    def _extract_detail_field(self, data: Dict, field: str, keyword: str) -> Optional[str]:
        """从详情页数据提取字段"""
        text = data.get("text", "")
        html = data.get("html", "")

        # 简单的关键词匹配提取
        pattern = rf"{keyword}[：:]\s*([^\n<]+)"
        match = re.search(pattern, text + html)
        return match.group(1).strip() if match else None

    def _extract_age(self, data: Dict) -> Optional[int]:
        """提取年龄"""
        age_str = self._extract_detail_field(data, "age", "年龄")
        if age_str:
            match = re.search(r"(\d+)", age_str)
            return int(match.group(1)) if match else None
        return None

    def _extract_gender(self, data: Dict) -> Optional[str]:
        """提取性别"""
        text = data.get("text", "")
        if "男" in text:
            return "男"
        elif "女" in text:
            return "女"
        return None

    def _parse_contact(self, data: Dict) -> CandidateContact:
        """解析联系方式"""
        phone = self._extract_detail_field(data, "phone", "手机")
        email = self._extract_detail_field(data, "email", "邮箱")
        wechat = self._extract_detail_field(data, "wechat", "微信")

        return CandidateContact(
            phone=phone,
            email=email,
            wechat=wechat,
        )

    def _parse_experiences(self, data: Dict) -> List[CandidateExperience]:
        """解析工作经历"""
        experiences = []
        # 根据实际页面结构解析
        # 这里提供框架，实际实现需要根据页面结构调整
        return experiences

    def _parse_educations(self, data: Dict) -> List[CandidateEducation]:
        """解析教育经历"""
        educations = []
        # 根据实际页面结构解析
        return educations

    def _parse_skills(self, data: Dict) -> List[str]:
        """解析技能标签"""
        skills = []
        text = data.get("text", "")
        # 提取标签类的技能
        tag_pattern = r"#(\w+)"
        skills.extend(re.findall(tag_pattern, text))
        return list(set(skills))

    async def search(
        self,
        keyword: str,
        city: Optional[str] = None,
        salary: Optional[str] = None,
        experience: Optional[str] = None,
        pages: int = 1,
    ) -> List[Candidate]:
        """
        执行搜索并返回候选人列表

        注意：实际浏览器操作由 Hermes Agent 完成，本方法提供搜索参数和结果处理

        使用 Skill 中的搜索流程:
        1. chrome_navigate(search_url)
        2. chrome_fill_or_select(搜索框, keyword)
        3. chrome_click_element(搜索按钮)
        4. 循环抓取页面，调用 parse_candidate_list() 解析
        5. 如需详情，点击进入详情页，调用 parse_candidate_detail()
        """
        if not self.check_cookie():
            logger.error("请先登录！")
            return []

        logger.info(f"[BOSS] 开始搜索: '{keyword}'")
        logger.info(f"  城市: {city or '不限'}")
        logger.info(f"  薪资: {salary or '不限'}")
        logger.info(f"  经验: {experience or '不限'}")
        logger.info(f"  页数: {pages}")

        # 返回空列表，实际数据由 Agent 通过 MCP 工具获取后解析
        logger.info("  请通过 Hermes Agent 执行搜索流程，详见 skills/boss-search/")
        return []

    def get_mcp_operation_script(self, operation: str, **kwargs) -> str:
        """
        生成 MCP 工具调用脚本供 Hermes Agent 执行

        Args:
            operation: 'login' | 'search' | 'detail'
            **kwargs: 操作参数

        Returns:
            MCP 工具调用脚本
        """
        if operation == "login":
            return self._get_login_script()
        elif operation == "search":
            return self._get_search_script(**kwargs)
        elif operation == "detail":
            return self._get_detail_script(**kwargs)
        else:
            return f"未知操作: {operation}"

    def _get_login_script(self) -> str:
        """生成登录操作的 MCP 调用脚本"""
        return f"""
# BOSS 直聘登录流程
# 请在 Hermes Agent 中依次执行以下 MCP 工具调用

1. 导航到登录页
   mcp_chrome_navigate(url="{self.login_url}")

2. 点击扫码登录
   mcp_chrome_click_element(selector="{selectors.QRCODE_LOGIN_BTN}")

3. 截取二维码展示给用户
   mcp_chrome_screenshot(name="boss_qrcode")

4. 等待用户扫码（建议等待 30 秒）
   # 手动扫码...

5. 验证登录成功
   mcp_chrome_read_page(filter="interactive")
   # 检查是否出现 {selectors.LOGIN_SUCCESS_INDICATOR}

6. 获取并保存 Cookie
   # 通过 chrome_javascript 获取 document.cookie
   mcp_chrome_javascript(code="JSON.stringify(document.cookie)")
   # 然后调用 boss_searcher.save_cookies(cookies_list)
"""

    def _get_search_script(self, keyword: str, city: str = None, pages: int = 1) -> str:
        """生成搜索操作的 MCP 调用脚本"""
        return f"""
# BOSS 直聘人才搜索流程
# 关键词: {keyword}
# 城市: {city or '不限'}
# 页数: {pages}

1. 导航到搜索页
   mcp_chrome_navigate(url="{self.search_url}")

2. 输入关键词
   mcp_chrome_fill_or_select(selector="{selectors.SEARCH_INPUT}", value="{keyword}")

3. 点击搜索
   mcp_chrome_click_element(selector="{selectors.SEARCH_BTN}")

4. 等待搜索结果
   # 等待页面加载...

5. 解析第 1 页
   mcp_chrome_read_page()
   # 调用 boss_searcher.parse_candidate_list(page_data)

6. 翻页循环
   for i in range(2, {pages + 1}):
       mcp_chrome_click_element(selector="{selectors.NEXT_PAGE_BTN}")
       mcp_chrome_read_page()
       # 解析...

7. （可选）抓取详情
   对感兴趣的候选人点击进入详情页
   调用 boss_searcher.parse_candidate_detail(detail_data)
"""

    def _get_detail_script(self, candidate_id: str) -> str:
        """生成详情抓取的 MCP 调用脚本"""
        detail_url = selectors.DETAIL_URL_PATTERN.format(candidate_id)
        return f"""
# BOSS 直聘候选人详情抓取
# 候选人 ID: {candidate_id}

1. 导航到详情页
   mcp_chrome_navigate(url="{detail_url}")

2. 读取页面完整内容
   mcp_chrome_read_page()

3. 解析结构化数据
   boss_searcher.parse_candidate_detail(detail_data)

4. 导出数据
   data_exporter.export_json([candidate], "output/boss_{candidate_id}.json")
"""
