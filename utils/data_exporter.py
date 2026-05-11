"""
数据导出工具 - 支持 JSON/CSV 格式
"""
import json
import csv
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from searcher.models import Candidate, SearchResult
from utils.log import log
from conf import OUTPUT_DIR


class DataExporter:
    """数据导出器"""
    
    @staticmethod
    def _get_output_path(filename: str, format: str = "json") -> Path:
        """生成输出文件路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(filename).stem
        output_file = OUTPUT_DIR / f"{base_name}_{timestamp}.{format}"
        return output_file
    
    @staticmethod
    def _flatten_candidate(candidate: Candidate) -> dict:
        """将 Candidate 对象扁平化，用于 CSV 导出"""
        data = candidate.model_dump()
        
        # 扁平化联系方式
        contact = data.pop("contact", {})
        for k, v in contact.items():
            data[f"contact_{k}"] = v
        
        # 简化经历字段（只保留前 3 条）
        experiences = data.pop("experiences", [])
        for i, exp in enumerate(experiences[:3]):
            data[f"exp_{i+1}_company"] = exp.get("company")
            data[f"exp_{i+1}_title"] = exp.get("title")
            data[f"exp_{i+1}_duration"] = exp.get("duration")
        
        # 简化教育字段
        educations = data.pop("educations", [])
        for i, edu in enumerate(educations[:2]):
            data[f"edu_{i+1}_school"] = edu.get("school")
            data[f"edu_{i+1}_degree"] = edu.get("degree")
        
        # 技能转为字符串
        if "skills" in data:
            data["skills"] = ", ".join(data["skills"])
        
        # 移除原始数据
        data.pop("raw_data", None)
        
        return data
    
    @classmethod
    def to_json(cls, candidates: List[Candidate], filename: Optional[str] = None) -> Path:
        """导出为 JSON 格式"""
        if not filename:
            filename = f"candidates_{candidates[0].platform if candidates else 'unknown'}"
        
        output_file = cls._get_output_path(filename, "json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(
                [c.model_dump(exclude_none=True) for c in candidates],
                f,
                ensure_ascii=False,
                indent=2
            )
        
        log.info(f"已导出 {len(candidates)} 条数据到: {output_file}")
        return output_file
    
    @classmethod
    def to_csv(cls, candidates: List[Candidate], filename: Optional[str] = None) -> Path:
        """导出为 CSV 格式"""
        if not candidates:
            log.warning("没有数据可导出")
            return None
        
        if not filename:
            filename = f"candidates_{candidates[0].platform}"
        
        output_file = cls._get_output_path(filename, "csv")
        
        # 先扁平化所有数据，收集所有可能的字段名
        all_flat = []
        all_fields = set()
        
        for candidate in candidates:
            flat_data = cls._flatten_candidate(candidate)
            all_flat.append(flat_data)
            all_fields.update(flat_data.keys())
        
        # 按逻辑顺序排名字段
        fieldnames = sorted(all_fields)
        
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, restval='', extrasaction='ignore')
            writer.writeheader()
            
            for flat_data in all_flat:
                writer.writerow(flat_data)
        
        log.info(f"已导出 {len(candidates)} 条数据到: {output_file}")
        return output_file
    
    @classmethod
    def export_search_result(cls, result: SearchResult, format: str = "json") -> Path:
        """导出搜索结果"""
        if format == "json":
            return cls.to_json(result.candidates, f"search_{result.keyword}")
        elif format == "csv":
            return cls.to_csv(result.candidates, f"search_{result.keyword}")
        else:
            raise ValueError(f"不支持的导出格式: {format}")


__all__ = ["DataExporter"]
