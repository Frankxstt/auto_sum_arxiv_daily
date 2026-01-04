"""
新闻总结模块
使用模板化摘要生成新闻摘要
"""

import logging
from typing import List, Dict
from datetime import datetime
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


def parse_date(date_str: str) -> str:
    """
    解析日期字符串并格式化为可读格式
    
    Args:
        date_str: 日期字符串
        
    Returns:
        格式化后的日期字符串
    """
    if not date_str:
        return "未知日期"
    
    try:
        # 尝试解析各种日期格式
        dt = date_parser.parse(date_str)
        # 格式化为中文日期格式
        return dt.strftime("%Y年%m月%d日")
    except (ValueError, TypeError):
        # 如果解析失败，返回原始字符串或截取部分
        try:
            return date_str[:10]  # 取前10个字符（通常是日期部分）
        except:
            return "未知日期"


def summarize_news(news: Dict) -> Dict:
    """
    生成单条新闻的摘要
    
    Args:
        news: 新闻字典
        
    Returns:
        包含摘要信息的字典
    """
    title = news.get('title', '无标题')
    link = news.get('link', '')
    summary = news.get('summary', '')
    published = news.get('published', '')
    source = news.get('source', '未知来源')
    
    # 如果summary为空，使用title作为摘要
    if not summary or len(summary.strip()) < 10:
        summary = title
    
    # 截取摘要长度（避免过长）
    max_summary_length = 300
    if len(summary) > max_summary_length:
        summary = summary[:max_summary_length] + "..."
    
    # 解析日期
    formatted_date = parse_date(published)
    
    return {
        'title': title,
        'link': link,
        'summary': summary,
        'published': formatted_date,
        'source': source,
        'topic': news.get('topic', '其他'),
        'importance': news.get('importance', '中'),
        'source_category': news.get('source_category', '未知来源')
    }


def format_news_summary(news_list: List[Dict], max_items: int = None) -> str:
    """
    格式化新闻列表为文本摘要
    
    Args:
        news_list: 新闻列表
        max_items: 最大显示条数，None表示显示全部
        
    Returns:
        格式化后的文本摘要
    """
    if max_items:
        news_list = news_list[:max_items]
    
    if not news_list:
        return "暂无新闻"
    
    lines = []
    for i, news in enumerate(news_list, 1):
        summarized = summarize_news(news)
        lines.append(f"{i}. {summarized['title']}")
        lines.append(f"   来源: {summarized['source']} | 日期: {summarized['published']}")
        lines.append(f"   摘要: {summarized['summary']}")
        lines.append(f"   链接: {summarized['link']}")
        lines.append("")
    
    return "\n".join(lines)


def format_news_by_category(classified_news: Dict) -> Dict[str, str]:
    """
    按分类格式化新闻摘要
    
    Args:
        classified_news: 分类后的新闻字典
        
    Returns:
        按分类组织的格式化文本字典
    """
    formatted = {}
    
    # 按主题格式化
    if 'by_topic' in classified_news:
        topic_texts = []
        for topic, news_list in sorted(classified_news['by_topic'].items()):
            topic_texts.append(f"\n【{topic}】({len(news_list)}条)")
            topic_texts.append(format_news_summary(news_list))
        formatted['by_topic'] = "\n".join(topic_texts)
    
    # 按重要性格式化
    if 'by_importance' in classified_news:
        importance_texts = []
        for importance in ['高', '中', '低']:
            if importance in classified_news['by_importance']:
                news_list = classified_news['by_importance'][importance]
                importance_texts.append(f"\n【{importance}重要性】({len(news_list)}条)")
                importance_texts.append(format_news_summary(news_list))
        formatted['by_importance'] = "\n".join(importance_texts)
    
    # 按来源格式化
    if 'by_source' in classified_news:
        source_texts = []
        for source, news_list in sorted(classified_news['by_source'].items()):
            source_texts.append(f"\n【{source}】({len(news_list)}条)")
            source_texts.append(format_news_summary(news_list, max_items=5))  # 每个来源最多显示5条
        formatted['by_source'] = "\n".join(source_texts)
    
    return formatted


def generate_summary_statistics(classified_news: Dict) -> str:
    """
    生成摘要统计信息
    
    Args:
        classified_news: 分类后的新闻字典
        
    Returns:
        统计信息文本
    """
    total = len(classified_news.get('all_news', []))
    
    stats = [f"今日共收集 {total} 条AI相关新闻\n"]
    
    # 按主题统计
    if 'by_topic' in classified_news:
        stats.append("按主题分布:")
        for topic, news_list in sorted(classified_news['by_topic'].items()):
            count = len(news_list)
            percentage = (count / total * 100) if total > 0 else 0
            stats.append(f"  - {topic}: {count}条 ({percentage:.1f}%)")
    
    # 按重要性统计
    if 'by_importance' in classified_news:
        stats.append("\n按重要性分布:")
        for importance in ['高', '中', '低']:
            if importance in classified_news['by_importance']:
                count = len(classified_news['by_importance'][importance])
                percentage = (count / total * 100) if total > 0 else 0
                stats.append(f"  - {importance}重要性: {count}条 ({percentage:.1f}%)")
    
    return "\n".join(stats)

