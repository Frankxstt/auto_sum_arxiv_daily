"""
新闻获取模块
支持从RSS订阅源和NewsAPI获取新闻
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


def fetch_from_rss(urls: List[str]) -> List[Dict]:
    """
    从RSS订阅源获取新闻
    
    Args:
        urls: RSS源URL列表
        
    Returns:
        新闻列表，每个新闻包含title, link, published, summary, source等字段
    """
    all_news = []
    
    for url in urls:
        try:
            logger.info(f"正在获取RSS源: {url}")
            feed = feedparser.parse(url)
            
            if feed.bozo and feed.bozo_exception:
                logger.warning(f"RSS源解析错误 {url}: {feed.bozo_exception}")
                continue
            
            for entry in feed.entries:
                news_item = {
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', entry.get('description', '')),
                    'source': entry.get('source', {}).get('title', url) if hasattr(entry, 'source') else url,
                    'source_type': 'rss'
                }
                all_news.append(news_item)
            
            logger.info(f"从 {url} 获取了 {len(feed.entries)} 条新闻")
            
        except Exception as e:
            logger.error(f"获取RSS源 {url} 时出错: {str(e)}")
            continue
    
    return all_news


def fetch_from_newsapi(api_key: str, keywords: List[str] = None, days_back: int = 1) -> List[Dict]:
    """
    从NewsAPI获取新闻
    
    Args:
        api_key: NewsAPI密钥
        keywords: 搜索关键词列表，默认为AI相关关键词
        days_back: 获取多少天前的新闻，默认1天
        
    Returns:
        新闻列表
    """
    if keywords is None:
        keywords = ['artificial intelligence', 'machine learning', 'AI', 'deep learning']
    
    all_news = []
    
    # 计算日期范围
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)
    
    try:
        # NewsAPI的everything端点
        url = 'https://newsapi.org/v2/everything'
        
        for keyword in keywords:
            params = {
                'q': keyword,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': api_key
            }
            
            try:
                logger.info(f"正在从NewsAPI获取关键词 '{keyword}' 的新闻")
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'ok':
                    articles = data.get('articles', [])
                    for article in articles:
                        news_item = {
                            'title': article.get('title', '无标题'),
                            'link': article.get('url', ''),
                            'published': article.get('publishedAt', ''),
                            'summary': article.get('description', ''),
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'source_type': 'newsapi',
                            'author': article.get('author', '')
                        }
                        all_news.append(news_item)
                    
                    logger.info(f"从NewsAPI获取了 {len(articles)} 条关于 '{keyword}' 的新闻")
                else:
                    logger.warning(f"NewsAPI返回错误: {data.get('message', 'Unknown error')}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"请求NewsAPI时出错 (关键词: {keyword}): {str(e)}")
                continue
            except Exception as e:
                logger.error(f"处理NewsAPI响应时出错 (关键词: {keyword}): {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"NewsAPI获取过程中出错: {str(e)}")
    
    return all_news


def deduplicate_news(news_list: List[Dict]) -> List[Dict]:
    """
    新闻去重，基于标题和链接
    
    Args:
        news_list: 新闻列表
        
    Returns:
        去重后的新闻列表
    """
    seen = set()
    unique_news = []
    
    for news in news_list:
        # 使用标题和链接的组合作为唯一标识
        identifier = (news.get('title', '').lower().strip(), news.get('link', '').strip())
        
        if identifier not in seen and identifier[0] and identifier[1]:
            seen.add(identifier)
            unique_news.append(news)
    
    logger.info(f"去重前: {len(news_list)} 条，去重后: {len(unique_news)} 条")
    return unique_news


def filter_ai_news(news_list: List[Dict], keywords: List[str] = None) -> List[Dict]:
    """
    过滤AI相关新闻
    
    Args:
        news_list: 新闻列表
        keywords: AI相关关键词列表
        
    Returns:
        过滤后的AI相关新闻列表
    """
    if keywords is None:
        keywords = [
            'artificial intelligence', 'AI', 'machine learning', 'ML',
            'deep learning', 'neural network', 'NLP', 'natural language processing',
            'computer vision', 'CV', 'reinforcement learning', 'RL',
            'GPT', 'BERT', 'transformer', 'LLM', 'large language model',
            'chatbot', 'chatgpt', 'claude', '人工智能', '机器学习',
            '深度学习', '神经网络', '自然语言处理', '计算机视觉'
        ]
    
    ai_news = []
    
    for news in news_list:
        title = news.get('title', '').lower()
        summary = news.get('summary', '').lower()
        text = f"{title} {summary}"
        
        # 检查是否包含AI相关关键词
        if any(keyword.lower() in text for keyword in keywords):
            ai_news.append(news)
    
    logger.info(f"过滤前: {len(news_list)} 条，过滤后: {len(ai_news)} 条AI相关新闻")
    return ai_news


def fetch_all_news(config: Dict) -> List[Dict]:
    """
    从所有配置的源获取新闻
    
    Args:
        config: 配置字典，包含rss_urls和newsapi配置
        
    Returns:
        去重和过滤后的AI相关新闻列表
    """
    all_news = []
    
    # 从RSS源获取
    rss_urls = config.get('news_sources', {}).get('rss_urls', [])
    if rss_urls:
        rss_news = fetch_from_rss(rss_urls)
        all_news.extend(rss_news)
    
    # 从NewsAPI获取（如果配置了）
    newsapi_config = config.get('news_sources', {}).get('newsapi', {})
    if newsapi_config.get('enabled', False) and newsapi_config.get('api_key'):
        newsapi_news = fetch_from_newsapi(
            api_key=newsapi_config.get('api_key'),
            keywords=newsapi_config.get('keywords'),
            days_back=newsapi_config.get('days_back', 1)
        )
        all_news.extend(newsapi_news)
    
    # 去重
    unique_news = deduplicate_news(all_news)
    
    # 过滤AI相关新闻
    ai_keywords = config.get('ai_keywords', [])
    filtered_news = filter_ai_news(unique_news, ai_keywords)
    
    return filtered_news

