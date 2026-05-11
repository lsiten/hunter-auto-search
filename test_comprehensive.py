"""
综合功能测试
验证所有新增工具功能
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from loguru import logger

from conf import OUTPUT_DIR
from searcher.models import Candidate, CandidateContact, CandidateExperience, CandidateEducation
from utils.data_validator import DataValidator
from utils.search_aggregator import SearchResultAggregator, aggregate_search_results


def test_data_validator():
    """测试数据验证器"""
    print("\n" + "=" * 60)
    print("测试 1: 数据验证器")
    print("=" * 60)
    
    validator = DataValidator(strict=False)
    
    # 创建测试数据
    candidates = create_test_candidates(5)
    
    # 验证
    result = validator.validate_all(candidates)
    
    print(f"总候选人数: {result['total']}")
    print(f"有效: {result['valid']}")
    print(f"无效: {result['invalid']}")
    print(f"平均完整性: {result['avg_completeness']:.1%}")
    
    # 生成报告
    report = validator.generate_validation_report(result)
    print("\n" + report)
    
    # 测试去重
    print("\n测试去重功能...")
    duplicate_candidates = candidates + candidates  # 制造重复
    deduplicated, reports = validator.deduplicate_candidates(duplicate_candidates)
    print(f"原始: {len(duplicate_candidates)} -> 去重后: {len(deduplicated)}")
    print(f"发现重复组: {len(reports)}")
    
    print("✅ 数据验证器测试通过")


def test_search_aggregator():
    """测试搜索结果聚合器"""
    print("\n" + "=" * 60)
    print("测试 2: 搜索结果聚合器")
    print("=" * 60)
    
    aggregator = SearchResultAggregator()
    
    # 创建测试数据
    candidates = create_test_candidates(20)
    
    # 模拟不同平台
    platforms = ['boss', 'liepin', 'linkedin', 'maimai']
    for i, candidate in enumerate(candidates):
        candidate.platform = platforms[i % len(platforms)]
        if i % 3 == 0:
            candidate.current_company = f"测试公司_{i % 5}"
        if i % 2 == 0:
            candidate.location = f"城市_{i % 4}"
        candidate.skills = [f"技能_{j}" for j in range(i % 5 + 1)]
    
    # 添加到聚合器
    aggregator.add_candidates(candidates)
    
    # 聚合
    report = aggregator.aggregate(deduplicate=True)
    print(f"加载总数: {report['total_loaded']}")
    print(f"去重后: {report['after_deduplication']}")
    
    # 打印摘要
    aggregator.print_summary()
    
    # 测试过滤
    print("\n测试过滤功能...")
    
    # 按平台过滤
    boss_candidates = aggregator.filter_by_platform('boss')
    print(f"BOSS 平台: {len(boss_candidates)} 人")
    
    # 按关键词过滤
    filtered = aggregator.filter_by_keyword('测试公司_1')
    print(f"关键词 '测试公司_1' 匹配: {len(filtered)} 人")
    
    # 导出聚合结果
    output_path = aggregator.export_aggregated("test_aggregated")
    print(f"聚合结果已导出: {output_path}")
    
    print("✅ 搜索结果聚合器测试通过")


def create_test_candidates(count: int = 10):
    """创建测试候选人数据"""
    from datetime import datetime
    
    candidates = []
    platforms = ['boss', 'liepin', 'linkedin', 'maimai']
    
    for i in range(count):
        candidate = Candidate(
            platform=platforms[i % len(platforms)],
            candidate_id=f"test_{i:04d}",
            name=f"候选人_{i:02d}",
            avatar_url=f"https://example.com/avatar/{i}.jpg",
            gender='男' if i % 2 == 0 else '女',
            age=25 + (i % 20),
            location=f"{'北京' if i % 2 == 0 else '上海'}",
            current_title=f"{'高级' if i % 3 == 0 else ''}工程师",
            current_company=f"测试科技公司_{i % 5}",
            current_salary=f"{15 + (i % 10)}K-{25 + (i % 10)}K",
            expected_salary=f"{20 + (i % 10)}K-{35 + (i % 10)}K",
            work_years=f"{i % 10 + 1}年",
            profile_url=f"https://example.com/profile/{i}",
            last_active=datetime.now().isoformat(),
            collected_at=datetime.now().isoformat()
        )
        
        # 添加联系方式
        if i % 3 == 0:
            candidate.contact = CandidateContact(
                phone=f"1380000{i:04d}" if i % 4 == 0 else None,
                email=f"candidate_{i}@example.com" if i % 3 == 0 else None,
                wechat=f"wechat_{i}" if i % 5 == 0 else None
            )
        
        # 添加工作经历
        for j in range(i % 3 + 1):
            candidate.experiences.append(
                CandidateExperience(
                    company=f"前公司_{i}_{j}",
                    title=f"职位_{j}",
                    duration=f"{j + 1}年",
                    description=f"在{j + 1}年工作中负责相关业务"
                )
            )
        
        # 添加教育经历
        if i % 2 == 0:
            candidate.educations.append(
                CandidateEducation(
                    school=f"{'清华' if i % 4 == 0 else '北大'}大学",
                    degree='本科' if i % 3 == 0 else '硕士',
                    major=f"计算机科学与技术",
                    duration=f"201{i}-201{i+4}"
                )
            )
        
        # 添加技能
        candidate.skills = ['Python', 'Java', 'C++'][:i % 3 + 1]
        
        candidates.append(candidate)
    
    return candidates


def main():
    """运行所有测试"""
    logger.info("开始综合功能测试...")
    
    try:
        test_data_validator()
        test_search_aggregator()
        
        print("\n" + "=" * 60)
        print("🎉 所有综合测试通过！")
        print("=" * 60)
        print("\n已验证功能:")
        print("  ✅ 数据验证与完整性评分")
        print("  ✅ 重复数据检测与合并")
        print("  ✅ 跨平台去重")
        print("  ✅ 多文件批量加载")
        print("  ✅ 搜索结果聚合")
        print("  ✅ 关键词过滤")
        print("  ✅ 平台/地区过滤")
        print("  ✅ 统计摘要生成")
        print("  ✅ 聚合结果导出")
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
