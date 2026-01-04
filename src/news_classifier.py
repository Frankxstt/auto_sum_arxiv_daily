"""
新闻分类模块
支持按主题、重要性、来源对新闻进行分类
"""

import logging
from typing import Dict, List
from collections import defaultdict

logger = logging.getLogger(__name__)


# 主题关键词映射
TOPIC_KEYWORDS = {
    '机器学习': [
        'machine learning', 'ML', '机器学习', 'supervised learning',
        'unsupervised learning', 'semi-supervised learning', 'ensemble learning'
    ],
    '自然语言处理': [
        'NLP', 'natural language processing', '自然语言处理', 'GPT', 'BERT',
        'transformer', 'LLM', 'large language model', '大语言模型', '语言模型',
        'text generation', '文本生成', 'chatbot', 'chatgpt', 'claude', 'llama'
    ],
    '计算机视觉': [
        'computer vision', 'CV', '计算机视觉', 'image recognition', '图像识别',
        'object detection', '目标检测', 'image classification', '图像分类',
        'CNN', 'convolutional neural network', '卷积神经网络'
    ],
    '强化学习': [
        'reinforcement learning', 'RL', '强化学习', 'Q-learning', 'DQN',
        'policy gradient', '策略梯度', 'actor-critic'
    ],
    'AI伦理': [
        'AI ethics', 'AI safety', 'AI governance', 'AI伦理', 'AI安全',
        'AI治理', 'responsible AI', 'responsible artificial intelligence',
        'AI bias', 'AI偏见', 'algorithmic fairness', '算法公平'
    ],
    'AI硬件': [
        'GPU', 'TPU', 'AI chip', 'AI芯片', 'neural processing unit',
        'NPU', 'AI accelerator', 'AI加速器'
    ],
    '其他': []
}

# 重要性关键词
HIGH_IMPORTANCE_KEYWORDS = [
    'breakthrough', '重大突破', '首次', 'first', 'revolutionary', '革命性',
    'game-changing', 'game changer', '里程碑', 'milestone', '重大', 'major',
    'significant', '重要', 'critical', '关键'
]

# 权威来源（高权重）
AUTHORITATIVE_SOURCES = [
    'nature', 'science', 'arxiv', 'openai', 'deepmind', 'google ai',
    'microsoft research', 'stanford', 'mit', 'berkeley', 'techcrunch',
    'the verge', 'wired', 'nature machine intelligence'
]


def classify_by_topic(news: Dict, topic_keywords: Dict = None) -> str:
    """
    按主题分类新闻
    
    Args:
        news: 新闻字典
        topic_keywords: 主题关键词字典，如果为None则使用默认
        
    Returns:
        主题名称
    """
    if topic_keywords is None:
        topic_keywords = TOPIC_KEYWORDS
    
    title = news.get('title', '').lower()
    summary = news.get('summary', '').lower()
    text = f"{title} {summary}"
    
    # 计算每个主题的匹配分数
    topic_scores = {}
    for topic, keywords in topic_keywords.items():
        if topic == '其他':
            continue
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        if score > 0:
            topic_scores[topic] = score
    
    # 返回得分最高的主题，如果没有匹配则返回"其他"
    if topic_scores:
        return max(topic_scores.items(), key=lambda x: x[1])[0]
    else:
        return '其他'


def classify_by_importance(news: Dict, 
                          high_importance_keywords: List[str] = None,
                          authoritative_sources: List[str] = None) -> str:
    """
    按重要性分类新闻
    
    Args:
        news: 新闻字典
        high_importance_keywords: 高重要性关键词列表
        authoritative_sources: 权威来源列表
        
    Returns:
        重要性等级：'高'、'中'、'低'
    """
    if high_importance_keywords is None:
        high_importance_keywords = HIGH_IMPORTANCE_KEYWORDS
    
    if authoritative_sources is None:
        authoritative_sources = AUTHORITATIVE_SOURCES
    
    title = news.get('title', '').lower()
    summary = news.get('summary', '').lower()
    source = news.get('source', '').lower()
    text = f"{title} {summary}"
    
    score = 0
    
    # 检查是否包含高重要性关键词
    if any(keyword.lower() in text for keyword in high_importance_keywords):
        score += 2
    
    # 检查是否来自权威来源
    if any(auth_source in source for auth_source in authoritative_sources):
        score += 2
    
    # 标题长度（通常重要新闻标题更详细）
    if len(title) > 50:
        score += 1
    
    # 根据分数判断重要性
    if score >= 3:
        return '高'
    elif score >= 1:
        return '中'
    else:
        return '低'


def classify_by_source(news: Dict) -> str:
    """
    按来源分类新闻
    
    Args:
        news: 新闻字典
        
    Returns:
        来源名称
    """
    source = news.get('source', '未知来源')
    
    # 清理来源名称
    if isinstance(source, dict):
        source = source.get('title', '未知来源')
    
    # 标准化一些常见来源
    source_lower = source.lower()
    
    if 'arxiv' in source_lower:
        return 'ArXiv'
    elif 'hacker news' in source_lower or 'hn' in source_lower:
        return 'Hacker News'
    elif 'reddit' in source_lower:
        return 'Reddit'
    elif 'github' in source_lower:
        return 'GitHub'
    elif 'twitter' in source_lower or 'x.com' in source_lower:
        return 'Twitter/X'
    else:
        # 返回原始来源，首字母大写
        return source.title() if source else '未知来源'


def classify_all(news_list: List[Dict], 
                 topic_keywords: Dict = None,
                 high_importance_keywords: List[str] = None,
                 authoritative_sources: List[str] = None) -> Dict:
    """
    对所有新闻进行综合分类
    
    Args:
        news_list: 新闻列表
        topic_keywords: 主题关键词字典
        high_importance_keywords: 高重要性关键词列表
        authoritative_sources: 权威来源列表
        
    Returns:
        分类结果字典，包含按主题、重要性、来源分类的新闻
    """
    classified = {
        'by_topic': defaultdict(list),
        'by_importance': defaultdict(list),
        'by_source': defaultdict(list),
        'all_news': []
    }
    
    for news in news_list:
        # 添加分类标签
        news['topic'] = classify_by_topic(news, topic_keywords)
        news['importance'] = classify_by_importance(
            news, high_importance_keywords, authoritative_sources
        )
        news['source_category'] = classify_by_source(news)
        
        # 按各种方式分类
        classified['by_topic'][news['topic']].append(news)
        classified['by_importance'][news['importance']].append(news)
        classified['by_source'][news['source_category']].append(news)
        classified['all_news'].append(news)
    
    # 转换为普通字典
    classified['by_topic'] = dict(classified['by_topic'])
    classified['by_importance'] = dict(classified['by_importance'])
    classified['by_source'] = dict(classified['by_source'])
    
    logger.info(f"分类完成: 共 {len(news_list)} 条新闻")
    logger.info(f"按主题: {', '.join(f'{k}({len(v)})' for k, v in classified['by_topic'].items())}")
    logger.info(f"按重要性: {', '.join(f'{k}({len(v)})' for k, v in classified['by_importance'].items())}")
    
    return classified

