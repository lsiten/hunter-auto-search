"""
Cookie 管理工具
"""
import json
from pathlib import Path
from typing import Optional, Dict, List
from conf import COOKIES_DIR
from utils.log import log


class CookieManager:
    """Cookie 管理器"""
    
    def __init__(self, platform: str, account: str):
        self.platform = platform
        self.account = account
        self.cookie_file = COOKIES_DIR / f"{platform}_{account}.json"
    
    def save(self, cookies: List[Dict]) -> bool:
        """保存 cookies"""
        try:
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            log.info(f"Cookie 已保存: {self.cookie_file}")
            return True
        except Exception as e:
            log.error(f"保存 Cookie 失败: {e}")
            return False
    
    def load(self) -> Optional[List[Dict]]:
        """加载 cookies"""
        if not self.cookie_file.exists():
            log.warning(f"Cookie 文件不存在: {self.cookie_file}")
            return None
        
        try:
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            log.info(f"Cookie 已加载: {self.cookie_file}")
            return cookies
        except Exception as e:
            log.error(f"加载 Cookie 失败: {e}")
            return None
    
    def exists(self) -> bool:
        """检查 Cookie 文件是否存在"""
        return self.cookie_file.exists()
    
    def delete(self) -> bool:
        """删除 Cookie 文件"""
        if self.cookie_file.exists():
            self.cookie_file.unlink()
            log.info(f"Cookie 文件已删除: {self.cookie_file}")
            return True
        return False
    
    def to_cookie_string(self, cookies: List[Dict]) -> str:
        """将 cookies 转换为 Cookie header 字符串"""
        cookie_parts = []
        for cookie in cookies:
            name = cookie.get('name', '')
            value = cookie.get('value', '')
            if name and value:
                cookie_parts.append(f"{name}={value}")
        return '; '.join(cookie_parts)
    
    def get_cookie_dict(self, cookies: List[Dict]) -> Dict[str, str]:
        """将 cookies 转换为字典"""
        return {c.get('name', ''): c.get('value', '') for c in cookies if c.get('name')}


__all__ = ["CookieManager"]
