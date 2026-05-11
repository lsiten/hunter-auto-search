"""
Hunter Auto Search 配置文件
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.absolute()

# Cookie 存储目录
COOKIES_DIR = PROJECT_ROOT / "cookies"
COOKIES_DIR.mkdir(exist_ok=True)

# 数据导出目录
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# 平台配置
PLATFORMS = {
    "boss": {
        "name": "BOSS 直聘",
        "login_url": "https://www.zhipin.com/web/user/?ka=header-login",
        "search_url": "https://www.zhipin.com/web/geek/job",
    },
    "liepin": {
        "name": "猎聘",
        "login_url": "https://www.liepin.com/",
        "search_url": "https://www.liepin.com/zhaopin/",
    },
    "linkedin": {
        "name": "领英",
        "login_url": "https://www.linkedin.com/login",
        "search_url": "https://www.linkedin.com/search/results/people/",
    },
    "maimai": {
        "name": "脉脉",
        "login_url": "https://maimai.cn/",
        "search_url": "https://maimai.cn/search",
    },
}

# 浏览器行为配置
BROWSER_CONFIG = {
    "default_timeout": 30000,  # 毫秒
    "page_load_delay": (2, 4),  # 页面加载随机延迟范围 (秒)
    "action_delay": (1, 3),  # 操作间随机延迟范围 (秒)
    "scroll_delay": (0.5, 1.5),  # 滚动延迟范围 (秒)
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# 搜索默认参数
DEFAULT_SEARCH_PARAMS = {
    "pages": 1,
    "max_candidates": 50,
    "fetch_detail": True,
}
