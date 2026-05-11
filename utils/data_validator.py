"""
数据验证与去重工具
验证候选人数据完整性，处理重复数据
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict

from loguru import logger
from pydantic import ValidationError

from searcher.models import Candidate


class DataValidator:
    """数据验证器"""
    
    # 手机号正则 (中国大陆)
    PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')
    
    # 邮箱正则
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.validation_results = defaultdict(list)
    
    def validate_candidate(self, candidate: Candidate) -> Dict:
        """验证单个候选人数据
        
        Args:
            candidate: 候选人对象
            
        Returns:
            验证结果字典
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'completeness': 0.0
        }
        
        # 必填字段检查
        if not candidate.name:
            result['errors'].append('name: 姓名不能为空')
            result['valid'] = False
        
        if not candidate.candidate_id:
            result['errors'].append('candidate_id: 候选人ID不能为空')
            result['valid'] = False
        
        # 格式验证
        if candidate.contact and candidate.contact.phone:
            if not self._validate_phone(candidate.contact.phone):
                result['warnings'].append(
                    f'phone: 手机号格式可能不正确: {candidate.contact.phone}'
                )
        
        if candidate.contact and candidate.contact.email:
            if not self._validate_email(candidate.contact.email):
                result['warnings'].append(
                    f'email: 邮箱格式可能不正确: {candidate.contact.email}'
                )
        
        # 数据完整性评分
        result['completeness'] = self._calculate_completeness(candidate)
        
        # 根据严格模式调整结果
        if self.strict and result['warnings']:
            result['valid'] = False
        
        return result
    
    def _validate_phone(self, phone: str) -> bool:
        """验证手机号格式"""
        # 移除常见分隔符
        cleaned = re.sub(r'[\s\-\+\(\)]', '', phone)
        return bool(self.PHONE_PATTERN.match(cleaned))
    
    def _validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        return bool(self.EMAIL_PATTERN.match(email))
    
    def _calculate_completeness(self, candidate: Candidate) -> float:
        """计算数据完整性得分 (0-1)
        
        加权评分：
        - 姓名 (10%)
        - 职位 (15%)
        - 公司 (15%)
        - 工作经历 (20%)
        - 教育经历 (15%)
        - 联系方式 (25%)
        """
        score = 0.0
        
        # 基本信息
        if candidate.name:
            score += 0.10
        
        if candidate.current_title:
            score += 0.15
        
        if candidate.current_company:
            score += 0.15
        
        # 工作经历
        if candidate.experiences:
            exp_score = min(len(candidate.experiences) * 0.10, 0.20)
            score += exp_score
        
        # 教育经历
        if candidate.educations:
            edu_score = min(len(candidate.educations) * 0.075, 0.15)
            score += edu_score
        
        # 联系方式
        contact_score = 0.0
        if candidate.contact:
            if candidate.contact.phone:
                contact_score += 0.10
            if candidate.contact.email:
                contact_score += 0.10
            if candidate.contact.wechat:
                contact_score += 0.05
        score += min(contact_score, 0.25)
        
        return round(score, 3)
    
    def validate_all(self, candidates: List[Candidate]) -> Dict:
        """批量验证候选人数据
        
        Args:
            candidates: 候选人列表
            
        Returns:
            批量验证结果
        """
        results = {
            'total': len(candidates),
            'valid': 0,
            'invalid': 0,
            'has_warnings': 0,
            'avg_completeness': 0.0,
            'details': []
        }
        
        total_completeness = 0.0
        
        for candidate in candidates:
            validation = self.validate_candidate(candidate)
            results['details'].append({
                'candidate_id': candidate.candidate_id,
                'name': candidate.name,
                **validation
            })
            
            if validation['valid']:
                results['valid'] += 1
            else:
                results['invalid'] += 1
            
            if validation['warnings']:
                results['has_warnings'] += 1
            
            total_completeness += validation['completeness']
        
        if candidates:
            results['avg_completeness'] = round(total_completeness / len(candidates), 3)
        
        return results
    
    def deduplicate_candidates(
        self,
        candidates: List[Candidate],
        strategy: str = 'merge'
    ) -> Tuple[List[Candidate], List[Dict]]:
        """候选人去重
        
        Args:
            candidates: 候选人列表
            strategy: 去重策略
                - 'keep_first': 保留第一个
                - 'keep_last': 保留最后一个
                - 'merge': 合并信息（默认）
            
        Returns:
            (去重后的列表, 去重报告)
        """
        # 按 candidate_id 分组
        id_groups = defaultdict(list)
        for candidate in candidates:
            id_groups[candidate.candidate_id].append(candidate)
        
        deduplicated = []
        reports = []
        
        for candidate_id, group in id_groups.items():
            if len(group) == 1:
                deduplicated.append(group[0])
            else:
                # 处理重复
                if strategy == 'keep_first':
                    deduplicated.append(group[0])
                elif strategy == 'keep_last':
                    deduplicated.append(group[-1])
                else:  # merge
                    merged = self._merge_candidates(group)
                    deduplicated.append(merged)
                
                reports.append({
                    'candidate_id': candidate_id,
                    'name': group[0].name,
                    'duplicate_count': len(group),
                    'strategy': strategy
                })
        
        return deduplicated, reports
    
    def _merge_candidates(self, candidates: List[Candidate]) -> Candidate:
        """合并多个重复候选人的信息
        
        优先保留更完整的数据
        """
        if len(candidates) == 1:
            return candidates[0]
        
        # 按完整性排序
        scored = [(self._calculate_completeness(c), c) for c in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        base = scored[0][1]
        
        # 合并其他候选人的信息
        for _, candidate in scored[1:]:
            # 合并工作经历
            existing_exp = {f"{e.company}|{e.title}" for e in base.experiences}
            for exp in candidate.experiences:
                key = f"{exp.company}|{exp.title}"
                if key not in existing_exp:
                    base.experiences.append(exp)
                    existing_exp.add(key)
            
            # 合并教育经历
            existing_edu = {f"{e.school}|{e.degree}" for e in base.educations}
            for edu in candidate.educations:
                key = f"{edu.school}|{edu.degree}"
                if key not in existing_edu:
                    base.educations.append(edu)
                    existing_edu.add(key)
            
            # 合并技能
            existing_skills = set(base.skills)
            for skill in candidate.skills:
                if skill not in existing_skills:
                    base.skills.append(skill)
                    existing_skills.add(skill)
            
            # 合并联系方式
            if candidate.contact:
                if not base.contact.phone and candidate.contact.phone:
                    base.contact.phone = candidate.contact.phone
                if not base.contact.email and candidate.contact.email:
                    base.contact.email = candidate.contact.email
                if not base.contact.wechat and candidate.contact.wechat:
                    base.contact.wechat = candidate.contact.wechat
        
        return base
    
    def cross_platform_deduplicate(
        self,
        candidates: List[Candidate]
    ) -> Tuple[List[Candidate], List[Dict]]:
        """跨平台去重（基于姓名 + 公司识别同一人）
        
        Returns:
            (去重后的列表, 重复检测报告)
        """
        # 构建去重键
        def make_key(c: Candidate) -> str:
            name = c.name.strip().lower() if c.name else ''
            company = c.current_company.strip().lower() if c.current_company else ''
            return f"{name}|{company}"
        
        key_groups = defaultdict(list)
        for candidate in candidates:
            key = make_key(candidate)
            if key and key != '|':
                key_groups[key].append(candidate)
        
        deduplicated = []
        reports = []
        
        for key, group in key_groups.items():
            if len(group) == 1:
                deduplicated.append(group[0])
            else:
                # 发现跨平台重复
                platforms = [c.platform for c in group]
                merged = self._merge_candidates(group)
                deduplicated.append(merged)
                
                reports.append({
                    'key': key,
                    'name': group[0].name,
                    'platforms': platforms,
                    'duplicate_count': len(group)
                })
        
        return deduplicated, reports
    
    def generate_validation_report(
        self,
        validation_results: Dict,
        deduplication_reports: Optional[List[Dict]] = None
    ) -> str:
        """生成验证报告
        
        Args:
            validation_results: validate_all 的结果
            deduplication_reports: 去重报告
            
        Returns:
            格式化的报告字符串
        """
        lines = ["=" * 60]
        lines.append("数据验证报告")
        lines.append("=" * 60)
        lines.append(f"总候选人数: {validation_results['total']}")
        lines.append(f"有效数据: {validation_results['valid']}")
        lines.append(f"无效数据: {validation_results['invalid']}")
        lines.append(f"含警告数据: {validation_results['has_warnings']}")
        lines.append(f"平均完整性: {validation_results['avg_completeness']:.1%}")
        lines.append("")
        
        if validation_results['details']:
            lines.append("详细问题:")
            lines.append("-" * 60)
            
            for detail in validation_results['details']:
                if not detail['valid'] or detail['warnings']:
                    status = "❌" if not detail['valid'] else "⚠️"
                    lines.append(
                        f"{status} {detail['name']} ({detail['candidate_id']})"
                    )
                    if detail['errors']:
                        for err in detail['errors']:
                            lines.append(f"   错误: {err}")
                    if detail['warnings']:
                        for warn in detail['warnings']:
                            lines.append(f"   警告: {warn}")
        
        if deduplication_reports:
            lines.append("")
            lines.append("=" * 60)
            lines.append("去重报告")
            lines.append("=" * 60)
            lines.append(f"发现重复: {len(deduplication_reports)} 组")
            lines.append("")
            
            for report in deduplication_reports:
                if 'platforms' in report:
                    lines.append(
                        f"🔄 {report['name']} - 跨平台重复: {', '.join(report['platforms'])}"
                    )
                else:
                    lines.append(
                        f"🔄 {report['name']} - 重复 {report['duplicate_count']} 次"
                    )
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
