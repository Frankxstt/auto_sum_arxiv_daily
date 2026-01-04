"""
邮件发送模块
支持通过SMTP发送HTML格式的邮件
"""

import smtplib
import logging
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_html_email(news_by_category: Dict, statistics: str = "", translate: bool = True) -> str:
    """
    生成HTML格式的邮件内容
    
    Args:
        news_by_category: 按分类组织的新闻字典
        statistics: 统计信息文本
        
    Returns:
        HTML格式的邮件内容
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
                padding: 10px;
                background-color: #ecf0f1;
                border-left: 4px solid #3498db;
            }}
            .news-item {{
                margin: 20px 0;
                padding: 15px;
                background-color: #fafafa;
                border-left: 3px solid #3498db;
                border-radius: 4px;
            }}
            .news-title {{
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 8px;
            }}
            .news-meta {{
                font-size: 12px;
                color: #7f8c8d;
                margin-bottom: 8px;
            }}
            .news-summary {{
                color: #555;
                margin: 10px 0;
            }}
            .news-link {{
                color: #3498db;
                text-decoration: none;
            }}
            .news-link:hover {{
                text-decoration: underline;
            }}
            .statistics {{
                background-color: #e8f4f8;
                padding: 15px;
                border-radius: 4px;
                margin: 20px 0;
                font-size: 14px;
            }}
            .topic-badge {{
                display: inline-block;
                padding: 3px 8px;
                background-color: #3498db;
                color: white;
                border-radius: 3px;
                font-size: 11px;
                margin-right: 5px;
            }}
            .importance-high {{
                border-left-color: #e74c3c !important;
            }}
            .importance-medium {{
                border-left-color: #f39c12 !important;
            }}
            .importance-low {{
                border-left-color: #95a5a6 !important;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ecf0f1;
                text-align: center;
                color: #7f8c8d;
                font-size: 12px;
            }}
            .overview {{
                background-color: #f8f9fa;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }}
            .overview-item {{
                margin: 10px 0;
                padding: 8px;
                background-color: white;
                border-left: 3px solid #3498db;
                border-radius: 3px;
            }}
            .overview-title {{
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 4px;
            }}
            .overview-summary {{
                color: #555;
                font-size: 14px;
                margin-left: 10px;
            }}
            .overview-link {{
                color: #3498db;
                text-decoration: none;
                font-size: 13px;
            }}
            .overview-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI新闻每日汇总 - {today}</h1>
    """
    
    # 添加统计信息
    if statistics:
        html += f'<div class="statistics"><pre>{statistics}</pre></div>'
    
    # 导入翻译函数
    from news_summarizer import summarize_news
    
    # 收集所有新闻用于概览，并为每个新闻生成唯一锚点ID
    all_news_for_overview = []
    news_anchor_map = {}  # 用于存储新闻到锚点ID的映射
    
    if 'by_topic' in news_by_category:
        news_counter = 0
        for topic, news_list in news_by_category['by_topic'].items():
            for news in news_list:
                news_counter += 1
                # 使用新闻的链接作为唯一标识生成锚点ID
                link = news.get('link', '')
                if link:
                    # 使用链接的哈希值生成简短的锚点ID
                    link_hash = hashlib.md5(link.encode()).hexdigest()[:8]
                    anchor_id = f"news-{link_hash}"
                else:
                    anchor_id = f"news-{news_counter}"
                
                news['_anchor_id'] = anchor_id
                news_anchor_map[id(news)] = anchor_id
                all_news_for_overview.append(news)
    
    # 生成新闻概览（每个新闻一句话）
    if all_news_for_overview:
        html += '<h2>📋 新闻概览</h2>'
        html += '<div class="overview">'
        html += '<p style="margin-top: 0; color: #7f8c8d; font-size: 14px;">以下是今日所有AI新闻的快速概览，点击标题可跳转到详细内容：</p>'
        
        for idx, news in enumerate(all_news_for_overview, 1):
            summarized = summarize_news(news, translate=translate)
            title = summarized.get('title', '无标题')
            summary = summarized.get('summary', '')
            
            # 生成一句话摘要（取摘要的第一句话或前100个字符）
            one_sentence = summary
            if len(summary) > 100:
                # 尝试找到第一个句号
                first_period = summary.find('。')
                first_exclamation = summary.find('！')
                first_question = summary.find('？')
                
                end_pos = len(summary)
                for pos in [first_period, first_exclamation, first_question]:
                    if pos > 0 and pos < end_pos:
                        end_pos = pos + 1
                        break
                
                if end_pos < len(summary):
                    one_sentence = summary[:end_pos]
                else:
                    one_sentence = summary[:100] + '...'
            
            # 获取锚点ID
            anchor_id = news.get('_anchor_id', f"news-{idx}")
            
            html += f'''
            <div class="overview-item">
                <div class="overview-title">
                    {idx}. <a href="#{anchor_id}" class="overview-link">{title}</a>
                </div>
                <div class="overview-summary">{one_sentence}</div>
            </div>
            '''
        
        html += '</div>'
        html += '<hr style="margin: 30px 0; border: none; border-top: 2px solid #ecf0f1;">'
    
    # 按主题展示
    if 'by_topic' in news_by_category:
        html += '<h2>📚 按主题分类</h2>'
        for topic, news_list in sorted(news_by_category['by_topic'].items()):
            html += f'<h3 style="color: #34495e; margin-top: 20px;">{topic} ({len(news_list)}条)</h3>'
            for news in news_list:
                # 翻译新闻
                summarized = summarize_news(news, translate=translate)
                importance_class = f"importance-{news.get('importance', 'medium').lower()}"
                
                # 获取锚点ID（如果已设置，否则生成一个）
                anchor_id = news.get('_anchor_id')
                if not anchor_id:
                    # 如果没有锚点ID，使用链接生成
                    link = news.get('link', '')
                    if link:
                        link_hash = hashlib.md5(link.encode()).hexdigest()[:8]
                        anchor_id = f"news-{link_hash}"
                    else:
                        anchor_id = f"news-{id(news)}"
                
                html += f'''
                <div id="{anchor_id}" class="news-item {importance_class}">
                    <div class="news-title">{summarized.get('title', '无标题')}</div>
                    <div class="news-meta">
                        <span class="topic-badge">{summarized.get('topic', '其他')}</span>
                        来源: {summarized.get('source', '未知')} | 
                        日期: {summarized.get('published', '未知日期')} | 
                        重要性: {summarized.get('importance', '中')}
                    </div>
                    <div class="news-summary">{summarized.get('summary', '')}</div>
                    <a href="{summarized.get('link', '#')}" class="news-link">阅读原文 →</a>
                </div>
                '''
    
    # 按重要性展示（高重要性新闻）
    if 'by_importance' in news_by_category and '高' in news_by_category['by_importance']:
        high_news = news_by_category['by_importance']['高']
        if high_news:
            html += '<h2>⭐ 高重要性新闻</h2>'
            for news in high_news:
                # 翻译新闻
                summarized = summarize_news(news, translate=translate)
                html += f'''
                <div class="news-item importance-high">
                    <div class="news-title">{summarized.get('title', '无标题')}</div>
                    <div class="news-meta">
                        <span class="topic-badge">{summarized.get('topic', '其他')}</span>
                        来源: {summarized.get('source', '未知')} | 
                        日期: {summarized.get('published', '未知日期')}
                    </div>
                    <div class="news-summary">{summarized.get('summary', '')}</div>
                    <a href="{summarized.get('link', '#')}" class="news-link">阅读原文 →</a>
                </div>
                '''
    
    html += '''
            <div class="footer">
                <p>本邮件由AI新闻自动汇总系统自动生成</p>
                <p>如有问题，请检查系统配置</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html


def send_email(config: Dict, subject: str, html_content: str) -> bool:
    """
    发送邮件
    
    Args:
        config: 邮件配置字典，包含smtp_host, smtp_port, email_user, email_password, email_to
        subject: 邮件主题
        html_content: HTML格式的邮件内容
        
    Returns:
        是否发送成功
    """
    try:
        smtp_host = config.get('smtp_host')
        smtp_port = config.get('smtp_port', 587)
        email_user = config.get('email_user')
        email_password = config.get('email_password')
        email_to = config.get('email_to')
        
        if not all([smtp_host, email_user, email_password, email_to]):
            logger.error("邮件配置不完整")
            return False
        
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['From'] = email_user
        msg['To'] = email_to
        msg['Subject'] = subject
        
        # 添加HTML内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 发送邮件
        logger.info(f"正在连接SMTP服务器: {smtp_host}:{smtp_port}")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # 启用TLS加密
        server.login(email_user, email_password)
        
        text = msg.as_string()
        server.sendmail(email_user, email_to, text)
        server.quit()
        
        logger.info(f"邮件已成功发送到 {email_to}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP认证失败: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"发送邮件时出错: {str(e)}")
        return False


def send_news_email(config: Dict, classified_news: Dict, statistics: str = "", translate: bool = True) -> bool:
    """
    发送新闻汇总邮件（便捷函数）
    
    Args:
        config: 配置字典，包含邮件配置和新闻数据
        classified_news: 分类后的新闻字典
        statistics: 统计信息
        translate: 是否翻译为中文，默认True
        
    Returns:
        是否发送成功
    """
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"AI新闻每日汇总 - {today}"
    
    # 准备按分类组织的新闻数据
    news_by_category = {
        'by_topic': classified_news.get('by_topic', {}),
        'by_importance': classified_news.get('by_importance', {})
    }
    
    # 生成HTML内容（使用翻译后的新闻）
    html_content = generate_html_email(news_by_category, statistics, translate=translate)
    
    # 发送邮件
    email_config = {
        'smtp_host': config.get('email', {}).get('smtp_host'),
        'smtp_port': config.get('email', {}).get('smtp_port', 587),
        'email_user': config.get('email', {}).get('email_user'),
        'email_password': config.get('email', {}).get('email_password'),
        'email_to': config.get('email', {}).get('email_to')
    }
    
    return send_email(email_config, subject, html_content)

