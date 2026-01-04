"""
邮件发送模块
支持通过SMTP发送HTML格式的邮件
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_html_email(news_by_category: Dict, statistics: str = "") -> str:
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI新闻每日汇总 - {today}</h1>
    """
    
    # 添加统计信息
    if statistics:
        html += f'<div class="statistics"><pre>{statistics}</pre></div>'
    
    # 按主题展示
    if 'by_topic' in news_by_category:
        html += '<h2>📚 按主题分类</h2>'
        for topic, news_list in sorted(news_by_category['by_topic'].items()):
            html += f'<h3 style="color: #34495e; margin-top: 20px;">{topic} ({len(news_list)}条)</h3>'
            for news in news_list:
                importance_class = f"importance-{news.get('importance', 'medium').lower()}"
                html += f'''
                <div class="news-item {importance_class}">
                    <div class="news-title">{news.get('title', '无标题')}</div>
                    <div class="news-meta">
                        <span class="topic-badge">{news.get('topic', '其他')}</span>
                        来源: {news.get('source', '未知')} | 
                        日期: {news.get('published', '未知日期')} | 
                        重要性: {news.get('importance', '中')}
                    </div>
                    <div class="news-summary">{news.get('summary', '')}</div>
                    <a href="{news.get('link', '#')}" class="news-link">阅读原文 →</a>
                </div>
                '''
    
    # 按重要性展示（高重要性新闻）
    if 'by_importance' in news_by_category and '高' in news_by_category['by_importance']:
        high_news = news_by_category['by_importance']['高']
        if high_news:
            html += '<h2>⭐ 高重要性新闻</h2>'
            for news in high_news:
                html += f'''
                <div class="news-item importance-high">
                    <div class="news-title">{news.get('title', '无标题')}</div>
                    <div class="news-meta">
                        <span class="topic-badge">{news.get('topic', '其他')}</span>
                        来源: {news.get('source', '未知')} | 
                        日期: {news.get('published', '未知日期')}
                    </div>
                    <div class="news-summary">{news.get('summary', '')}</div>
                    <a href="{news.get('link', '#')}" class="news-link">阅读原文 →</a>
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


def send_news_email(config: Dict, classified_news: Dict, statistics: str = "") -> bool:
    """
    发送新闻汇总邮件（便捷函数）
    
    Args:
        config: 配置字典，包含邮件配置和新闻数据
        classified_news: 分类后的新闻字典
        statistics: 统计信息
        
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
    
    # 生成HTML内容
    html_content = generate_html_email(news_by_category, statistics)
    
    # 发送邮件
    email_config = {
        'smtp_host': config.get('email', {}).get('smtp_host'),
        'smtp_port': config.get('email', {}).get('smtp_port', 587),
        'email_user': config.get('email', {}).get('email_user'),
        'email_password': config.get('email', {}).get('email_password'),
        'email_to': config.get('email', {}).get('email_to')
    }
    
    return send_email(email_config, subject, html_content)

