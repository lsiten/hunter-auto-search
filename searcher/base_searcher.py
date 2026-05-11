"""
搜索基类 - 所有平台搜索器的基类

设计理念：
- Python 类负责：数据结构定义、数据解析、Cookie 管理、生成 MCP 工具调用脚本
- 浏览器自动化：由 Hermes Agent 通过 MCP Chrome 工具完成
"""

import time
import random
from typing import Optional, List, Dict, Any

from conf import BROWSER_CONFIG, DEFAULT_SEARCH_PARAMS
from utils.log import logger
from utils.cookie_manager import CookieManager
from searcher.models import Candidate, SearchResult


class BaseSearcher:
    """搜索器基类 - 提供通用功能"""

    # 子类需要设置的属性
    platform: str  # 平台标识: boss/liepin/linkedin/maimai
    platform_name: str  # 平台显示名称
    base_url: str  # 基础 URL
    login_url: str  # 登录页面 URL
    search_url: str  # 搜索页面 URL

    def __init__(self, account: str = "default", headed: bool = True):
        self.account = account
        self.headed = headed
        self.cookie_manager = None  # 子类初始化
        self._cookies: Optional[List[Dict]] = None
        self._is_logged_in = False

    def _random_delay(self, min_sec: float = None, max_sec: float = None) -> None:
        """随机延迟，模拟人类行为"""
        if min_sec is None or max_sec is None:
            min_sec, max_sec = BROWSER_CONFIG["action_delay"]

        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _page_load_delay(self) -> None:
        """页面加载延迟"""
        min_sec, max_sec = BROWSER_CONFIG["page_load_delay"]
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    # ==================== Cookie 管理 ====================

    def save_cookies(self, cookies: List[Dict]) -> None:
        """保存浏览器 Cookie"""
        if self.cookie_manager:
            self.cookie_manager.save(cookies)
            self._cookies = cookies
            self._is_logged_in = True
            logger.info(f"[{self.platform_name}] Cookie 已保存: {len(cookies)} 条")

    def load_cookies(self) -> Optional[List[Dict]]:
        """加载 Cookie"""
        if self.cookie_manager:
            cookies = self.cookie_manager.load()
            if cookies:
                self._cookies = cookies
                logger.info(f"[{self.platform_name}] Cookie 已加载: {len(cookies)} 条")
            return cookies
        return None

    def check_cookie(self) -> bool:
        """检查 Cookie 是否存在"""
        if self.cookie_manager:
            return self.cookie_manager.exists()
        return False

    # ==================== 登录相关 ====================

    async def login(self) -> bool:
        """
        登录流程引导

        注意：实际浏览器操作由 Hermes Agent 通过 MCP Chrome 完成
        调用示例：
        1. mcp_chrome_navigate(url=self.login_url)
        2. 等待用户扫码/输入凭据
        3. 调用 save_cookies() 保存 Cookie
        """
        logger.info(f"[{self.platform_name}] 账号 '{self.account}' 登录流程")
        logger.info(f"  登录页面: {self.login_url}")
        logger.info("  请通过 Hermes Agent 执行 MCP Chrome 工具完成登录")
        return False

    # ==================== 搜索相关 ====================

    async def search(
        self,
        keyword: str,
        city: Optional[str] = None,
        salary: Optional[str] = None,
        experience: Optional[str] = None,
        pages: int = 1,
    ) -> List[Candidate]:
        """
        搜索流程引导

        注意：实际浏览器操作由 Hermes Agent 通过 MCP Chrome 完成
        调用示例：
        1. mcp_chrome_navigate(url=self.search_url)
        2. mcp_chrome_fill_or_select(selector=搜索框, value=keyword)
        3. mcp_chrome_click_element(selector=搜索按钮)
        4. 循环翻页，调用 parse_candidate_list() 解析
        """
        if not self.check_cookie():
            logger.warning(f"[{self.platform_name}] 未找到有效 Cookie，请先登录")
            return []

        logger.info(f"[{self.platform_name}] 开始搜索: '{keyword}'")
        logger.info(f"  城市: {city or '不限'}, 薪资: {salary or '不限'}")
        logger.info(f"  经验: {experience or '不限'}, 页数: {pages}")
        logger.info("  请通过 Hermes Agent 执行 MCP Chrome 工具完成搜索")
        return []

    # ==================== 数据解析 ====================

    def parse_candidate_list(self, page_data: Dict[str, Any]) -> List[Dict]:
        """
        解析候选人列表页面

        Args:
            page_data: chrome_read_page() 返回的页面数据

        Returns:
            候选人简要信息列表
        """
        raise NotImplementedError("子类必须实现此方法")

    def parse_candidate_detail(self, detail_data: Dict[str, Any]) -> Candidate:
        """
        解析候选人详情页面

        Args:
            detail_data: chrome_read_page() 返回的详情页数据

        Returns:
            Candidate 结构化对象
        """
        raise NotImplementedError("子类必须实现此方法")

    # ==================== MCP 脚本生成 ====================

    def get_mcp_login_script(self) -> str:
        """生成登录操作的 MCP 工具调用脚本"""
        raise NotImplementedError("子类必须实现此方法")

    def get_mcp_search_script(
        self, keyword: str, city: str = None, pages: int = 1
    ) -> str:
        """生成搜索操作的 MCP 工具调用脚本"""
        raise NotImplementedError("子类必须实现此方法")

    def get_mcp_detail_script(self, candidate_id: str) -> str:
        """生成详情抓取的 MCP 工具调用脚本"""
        raise NotImplementedError("子类必须实现此方法")
