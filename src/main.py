"""
主程序入口
整合所有模块，实现完整的新闻获取、分类、总结和邮件发送流程
"""

import sys
import os
import logging
import argparse
import yaml
from datetime import datetime
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_fetcher import fetch_all_news
from news_classifier import classify_all
from news_summarizer import format_news_by_category, generate_summary_statistics
from email_sender import send_news_email

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('news_aggregator.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yaml') -> dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"成功加载配置文件: {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"配置文件不存在: {config_path}")
        logger.info("请复制 config.yaml.example 为 config.yaml 并填写配置")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"配置文件格式错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"加载配置文件时出错: {str(e)}")
        sys.exit(1)


def load_config_from_env() -> dict:
    """
    从环境变量加载配置（用于GitHub Actions）
    
    Returns:
        配置字典
    """
    # 翻译配置（默认启用）
    translation_enabled = os.getenv('TRANSLATION_ENABLED', 'true').lower() == 'true'
    
    config = {
        'email': {
            'smtp_host': os.getenv('EMAIL_HOST', ''),
            'smtp_port': int(os.getenv('EMAIL_PORT', '587')),
            'email_user': os.getenv('EMAIL_USER', ''),
            'email_password': os.getenv('EMAIL_PASSWORD', ''),
            'email_to': os.getenv('EMAIL_TO', '')
        },
        'translation': {
            'enabled': translation_enabled,
            'target_language': 'zh'
        },
        'news_sources': {
            'rss_urls': os.getenv('RSS_URLS', '').split(',') if os.getenv('RSS_URLS') else [],
            'newsapi': {
                'enabled': bool(os.getenv('NEWS_API_KEY')),
                'api_key': os.getenv('NEWS_API_KEY', ''),
                'keywords': ['artificial intelligence', 'machine learning', 'AI'],
                'days_back': 1
            }
        },
        'ai_keywords': [
            'artificial intelligence', 'AI', 'machine learning', 'ML',
            'deep learning', 'neural network', 'NLP', 'natural language processing',
            'computer vision', 'CV', 'reinforcement learning', 'RL',
            'GPT', 'BERT', 'transformer', 'LLM', 'large language model'
        ]
    }
    
    # 过滤空的RSS URLs
    config['news_sources']['rss_urls'] = [url.strip() for url in config['news_sources']['rss_urls'] if url.strip()]
    
    return config


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI新闻自动汇总系统')
    parser.add_argument('--config', '-c', default='config.yaml', help='配置文件路径')
    parser.add_argument('--env', action='store_true', help='从环境变量加载配置（用于GitHub Actions）')
    parser.add_argument('--no-email', action='store_true', help='不发送邮件，仅输出到控制台')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("AI新闻自动汇总系统启动")
    logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    # 加载配置
    if args.env:
        logger.info("从环境变量加载配置")
        config = load_config_from_env()
    else:
        config = load_config(args.config)
    
    try:
        # 步骤1: 获取新闻
        logger.info("\n[步骤1] 开始获取新闻...")
        news_list = fetch_all_news(config)
        
        if not news_list:
            logger.warning("未获取到任何新闻")
            return
        
        logger.info(f"共获取 {len(news_list)} 条AI相关新闻")
        
        # 步骤2: 分类新闻
        logger.info("\n[步骤2] 开始分类新闻...")
        classified_news = classify_all(news_list)
        
        # 步骤3: 生成摘要和统计
        logger.info("\n[步骤3] 生成摘要和统计信息...")
        statistics = generate_summary_statistics(classified_news)
        logger.info(f"\n{statistics}")
        
        # 获取翻译配置
        translate = config.get('translation', {}).get('enabled', True)
        
        # 步骤4: 发送邮件
        if not args.no_email:
            logger.info("\n[步骤4] 准备发送邮件...")
            success = send_news_email(config, classified_news, statistics, translate=translate)
            
            if success:
                logger.info("邮件发送成功！")
            else:
                logger.error("邮件发送失败！")
                sys.exit(1)
        else:
            logger.info("\n[步骤4] 跳过邮件发送（--no-email选项）")
            # 输出到控制台
            formatted = format_news_by_category(classified_news, translate=translate)
            print("\n" + "=" * 60)
            print(statistics)
            print("\n" + formatted.get('by_topic', ''))
        
        logger.info("\n" + "=" * 60)
        logger.info("任务完成！")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("\n用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

