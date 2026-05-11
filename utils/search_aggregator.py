"""
搜索结果聚合工具
整合多平台搜索结果，统一管理和分析
"""
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set
from collections import defaultdict

from loguru import logger

from searcher.models import Candidate
from utils.data_exporter import DataExporter
from utils.data_validator import DataValidator


class SearchResultAggregator:
    """搜索结果聚合器"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        from conf import OUTPUT_DIR
        self.output_dir = output_dir or OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.aggregated_results: List[Candidate] = []
        self.source_files: List[str] = []
        self.validator = DataValidator(strict=False)
    
    def load_from_file(self, file_path: str) -> List[Candidate]:
        """从文件加载搜索结果
        
        Args:
            file_path: JSON 或 CSV 文件路径
            
        Returns:
            候选人列表
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"文件不存在: {file_path}")
            return []
        
        try:
            if path.suffix.lower() == '.json':
                return self._load_from_json(path)
            elif path.suffix.lower() == '.csv':
                return self._load_from_csv(path)
            else:
                logger.error(f"不支持的文件格式: {path.suffix}")
                return []
        except Exception as e:
            logger.error(f"加载文件失败 {file_path}: {e}")
            return []
    
    def _load_from_json(self, path: Path) -> List[Candidate]:
        """从 JSON 加载"""
        candidates = []
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 处理不同格式
        if isinstance(data, list):
            # 直接是候选人列表
            for item in data:
                try:
                    candidates.append(Candidate(**item))
                except Exception as e:
                    logger.warning(f"解析候选人失败: {e}")
        elif isinstance(data, dict) and 'candidates' in data:
            # 包含 candidates 字段
            for item in data['candidates']:
                try:
                    candidates.append(Candidate(**item))
                except Exception as e:
                    logger.warning(f"解析候选人失败: {e}")
        
        logger.info(f"从 {path.name} 加载了 {len(candidates)} 个候选人")
        self.source_files.append(str(path))
        return candidates
    
    def _load_from_csv(self, path: Path) -> List[Candidate]:
        """从 CSV 加载（简化版，只加载基础字段）"""
        candidates = []
        
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # 从 CSV 重建基础字段
                    candidate = Candidate(
                        platform=row.get('platform', 'unknown'),
                        candidate_id=row.get('candidate_id', ''),
                        name=row.get('name', ''),
                        current_title=row.get('current_title'),
                        current_company=row.get('current_company'),
                        current_salary=row.get('current_salary'),
                        location=row.get('location'),
                        collected_at=row.get('collected_at', datetime.now().isoformat())
                    )
                    candidates.append(candidate)
                except Exception as e:
                    logger.warning(f"解析 CSV 行失败: {e}")
        
        logger.info(f"从 {path.name} 加载了 {len(candidates)} 个候选人")
        self.source_files.append(str(path))
        return candidates
    
    def load_directory(self, directory: str, pattern: str = "*.json") -> List[Candidate]:
        """从目录批量加载搜索结果
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式
            
        Returns:
            所有候选人列表
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"目录不存在: {directory}")
            return []
        
        all_candidates = []
        
        for file_path in sorted(dir_path.glob(pattern)):
            candidates = self.load_from_file(str(file_path))
            all_candidates.extend(candidates)
        
        logger.info(f"从目录加载了共 {len(all_candidates)} 个候选人")
        return all_candidates
    
    def add_candidates(self, candidates: List[Candidate]):
        """添加候选人到聚合结果
        
        Args:
            candidates: 候选人列表
        """
        self.aggregated_results.extend(candidates)
        logger.info(f"添加了 {len(candidates)} 个候选人到聚合结果")
    
    def aggregate(self, deduplicate: bool = True) -> Dict:
        """聚合所有结果
        
        Args:
            deduplicate: 是否去重
            
        Returns:
            聚合报告
        """
        report = {
            'total_loaded': len(self.aggregated_results),
            'source_files': len(self.source_files),
            'deduplicated': deduplicate,
            'after_deduplication': 0,
            'validation_report': None,
            'deduplication_reports': None
        }
        
        # 数据验证
        validation_report = self.validator.validate_all(self.aggregated_results)
        report['validation_report'] = validation_report
        
        # 去重
        if deduplicate:
            deduplicated, dedup_reports = self.validator.deduplicate_candidates(
                self.aggregated_results
            )
            # 跨平台去重
            final_candidates, cross_reports = self.validator.cross_platform_deduplicate(
                deduplicated
            )
            
            self.aggregated_results = final_candidates
            report['after_deduplication'] = len(final_candidates)
            report['deduplication_reports'] = dedup_reports + cross_reports
        
        return report
    
    def export_aggregated(self, prefix: str = "aggregated") -> str:
        """导出聚合结果
        
        Args:
            prefix: 文件名前缀
            
        Returns:
            导出的文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{prefix}_{timestamp}"
        
        exporter = DataExporter()
        
        # 导出 JSON
        json_path = exporter.to_json(self.aggregated_results, base_name)
        
        # 导出 CSV
        csv_path = exporter.to_csv(self.aggregated_results, base_name)
        
        logger.info(f"聚合结果已导出: {base_name}")
        logger.info(f"  JSON: {json_path}")
        logger.info(f"  CSV: {csv_path}")
        
        return str(json_path)
    
    def generate_summary(self) -> Dict:
        """生成聚合摘要
        
        Returns:
            摘要字典
        """
        summary = {
            'total_candidates': len(self.aggregated_results),
            'by_platform': defaultdict(int),
            'by_location': defaultdict(int),
            'salary_range': defaultdict(int),
            'avg_completeness': 0.0,
            'top_companies': [],
            'top_skills': []
        }
        
        # 按平台统计
        for candidate in self.aggregated_results:
            summary['by_platform'][candidate.platform] += 1
            
            if candidate.location:
                summary['by_location'][candidate.location] += 1
            
            if candidate.current_salary:
                summary['salary_range'][candidate.current_salary] += 1
        
        # 统计公司出现频率
        company_count = defaultdict(int)
        for candidate in self.aggregated_results:
            if candidate.current_company:
                company_count[candidate.current_company] += 1
        
        summary['top_companies'] = sorted(
            company_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # 统计技能出现频率
        skill_count = defaultdict(int)
        for candidate in self.aggregated_results:
            for skill in candidate.skills:
                skill_count[skill] += 1
        
        summary['top_skills'] = sorted(
            skill_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        # 平均完整性
        if self.aggregated_results:
            total = sum(
                self.validator._calculate_completeness(c)
                for c in self.aggregated_results
            )
            summary['avg_completeness'] = round(total / len(self.aggregated_results), 3)
        
        return dict(summary)
    
    def print_summary(self):
        """打印聚合摘要"""
        summary = self.generate_summary()
        
        print("\n" + "=" * 60)
        print("搜索结果聚合摘要")
        print("=" * 60)
        print(f"总候选人数: {summary['total_candidates']}")
        print(f"平均完整性: {summary['avg_completeness']:.1%}")
        print()
        
        print("按平台分布:")
        for platform, count in sorted(summary['by_platform'].items(), key=lambda x: -x[1]):
            percentage = count / summary['total_candidates'] * 100
            print(f"  {platform:12} {count:4} ({percentage:5.1f}%)")
        
        print()
        print("热门公司 Top 10:")
        for i, (company, count) in enumerate(summary['top_companies'][:10], 1):
            print(f"  {i:2}. {company:30} {count:3} 人")
        
        print()
        print("热门技能 Top 10:")
        for i, (skill, count) in enumerate(summary['top_skills'][:10], 1):
            print(f"  {i:2}. {skill:20} {count:3} 次")
        
        print("=" * 60 + "\n")
    
    def filter_by_keyword(
        self,
        keyword: str,
        fields: Optional[List[str]] = None
    ) -> List[Candidate]:
        """按关键词过滤候选人
        
        Args:
            keyword: 搜索关键词
            fields: 搜索字段，默认搜索姓名、职位、公司
            
        Returns:
            匹配的候选人列表
        """
        if fields is None:
            fields = ['name', 'current_title', 'current_company', 'skills']
        
        keyword = keyword.lower()
        results = []
        
        for candidate in self.aggregated_results:
            matched = False
            
            if 'name' in fields and candidate.name:
                if keyword in candidate.name.lower():
                    matched = True
            
            if 'current_title' in fields and candidate.current_title:
                if keyword in candidate.current_title.lower():
                    matched = True
            
            if 'current_company' in fields and candidate.current_company:
                if keyword in candidate.current_company.lower():
                    matched = True
            
            if 'skills' in fields:
                for skill in candidate.skills:
                    if keyword in skill.lower():
                        matched = True
                        break
            
            if matched:
                results.append(candidate)
        
        logger.info(f"关键词 '{keyword}' 匹配到 {len(results)} 个候选人")
        return results
    
    def filter_by_platform(self, platform: str) -> List[Candidate]:
        """按平台过滤"""
        return [c for c in self.aggregated_results if c.platform == platform]
    
    def filter_by_location(self, location: str) -> List[Candidate]:
        """按地区过滤"""
        location = location.lower()
        return [
            c for c in self.aggregated_results
            if c.location and location in c.location.lower()
        ]
    
    def get_by_id(self, candidate_id: str) -> Optional[Candidate]:
        """按 ID 查找候选人"""
        for candidate in self.aggregated_results:
            if candidate.candidate_id == candidate_id:
                return candidate
        return None


# 快捷函数
def aggregate_search_results(
    directory: str,
    output_prefix: str = "aggregated"
) -> Dict:
    """快捷函数：聚合目录下所有搜索结果
    
    Args:
        directory: 搜索结果目录
        output_prefix: 输出文件前缀
        
    Returns:
        聚合结果报告
    """
    aggregator = SearchResultAggregator()
    
    # 加载所有 JSON 文件
    candidates = aggregator.load_directory(directory, "*.json")
    aggregator.add_candidates(candidates)
    
    # 聚合
    report = aggregator.aggregate(deduplicate=True)
    
    # 导出
    output_path = aggregator.export_aggregated(output_prefix)
    
    # 打印摘要
    aggregator.print_summary()
    
    return {
        'report': report,
        'output_path': output_path,
        'summary': aggregator.generate_summary()
    }
