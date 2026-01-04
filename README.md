# AI新闻自动汇总系统

## 📑 目录导航

### 快速开始
- [项目介绍](#项目介绍)
- [功能特性](#功能特性)
- [安装和配置](#安装和配置)
  - [环境要求](#1-环境要求)
  - [安装依赖](#2-安装依赖)
  - [配置文件](#3-配置文件)
  - [部署到GitHub](#4-部署到github)
  - [GitHub Actions配置](#5-github-actions配置用于定时任务)
- [使用方法](#使用方法)
  - [本地运行](#本地运行)
  - [定时任务](#定时任务github-actions)

### 详细文档
- [新闻来源](#新闻来源)
- [分类规则](#分类规则)
  - [按主题分类](#按主题分类)
  - [按重要性分类](#按重要性分类)
  - [按来源分类](#按来源分类)
- [项目结构](#项目结构)

### 配置指南
- 📘 [GitHub部署指南](GITHUB_DEPLOYMENT.md) - 如何将代码推送到GitHub
- 📗 [GitHub Actions配置指南](GITHUB_ACTIONS_SETUP.md) - 详细的Actions配置步骤
- 📙 [配置更新指南](GITHUB_CONFIG_UPDATE.md) - 翻译功能和中文RSS源配置
- 📕 [RSS源推荐列表](RSS_SOURCES.md) - 推荐的RSS订阅源
- 📋 [配置检查清单](CONFIG_CHECKLIST.md) - 配置验证清单

### 其他
- [注意事项](#注意事项)
- [扩展功能](#扩展功能)
- [许可证](#许可证)

---

## 项目介绍

这是一个自动化系统，每天从多个来源获取AI相关的新闻，对其进行分类和总结，并通过邮件发送给用户。系统使用Python实现，通过GitHub Actions实现定时任务。

## 功能特性

- **多源新闻获取**：支持RSS订阅源和NewsAPI等多种新闻来源（支持中英文源）
- **智能分类**：按主题、重要性、来源对新闻进行分类
- **自动总结**：使用模板化摘要生成新闻摘要
- **中文翻译**：自动将英文新闻翻译为中文（可配置）
- **邮件推送**：每天自动发送分类汇总的新闻到指定邮箱
- **定时任务**：通过GitHub Actions实现每天自动运行

## 安装和配置

### 1. 环境要求

- Python 3.8+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

复制配置文件模板并填写相关信息：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml` 文件，配置以下内容：

- **邮箱配置**：SMTP服务器地址、端口、账号、密码（或应用专用密码）
- **收件人邮箱**：接收新闻汇总的邮箱地址
- **新闻源配置**：RSS订阅源URL列表、NewsAPI密钥（可选）
- **分类关键词**：用于分类的关键词配置

### 4. 部署到GitHub

**首次部署**：请参考 [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) 了解如何将代码推送到GitHub。

### 5. GitHub Actions配置（用于定时任务）

详细的GitHub Actions配置步骤请参考 [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)

简要步骤：
1. 在GitHub仓库中，进入 Settings > Secrets and variables > Actions
2. 添加以下Secrets：
   - `EMAIL_HOST`: SMTP服务器地址
   - `EMAIL_PORT`: SMTP端口
   - `EMAIL_USER`: 邮箱账号
   - `EMAIL_PASSWORD`: 邮箱密码或应用专用密码
   - `EMAIL_TO`: 收件人邮箱
   - `RSS_URLS`: RSS订阅源URL列表（可选，用逗号分隔）
   - `NEWS_API_KEY`: NewsAPI密钥（可选）

## 使用方法

### 本地运行

```bash
python src/main.py
```

### 定时任务（GitHub Actions）

系统已配置GitHub Actions工作流，每天自动运行。默认运行时间为每天UTC 22:00（北京时间次日6:00），可在 `.github/workflows/daily_news.yml` 中修改。

## 新闻来源

系统支持以下新闻来源：

### RSS订阅源

**英文源**：
- Hacker News RSS
- Reddit r/MachineLearning
- ArXiv AI相关论文
- 科技媒体RSS（如TechCrunch等）

**中文源**：
- 36氪、爱范儿、极客公园、虎嗅、雷锋网等
- 更多中文RSS源请查看 [RSS_SOURCES.md](RSS_SOURCES.md)

### NewsAPI

- 通过NewsAPI获取AI相关新闻（需要API密钥）

### 自定义来源

可以在 `config.yaml` 中添加自定义RSS源。

## 分类规则

### 按主题分类

- **机器学习**：ML、深度学习、神经网络等
- **自然语言处理**：NLP、大语言模型、GPT、BERT等
- **计算机视觉**：CV、图像识别、目标检测等
- **强化学习**：RL、强化学习相关
- **AI伦理**：AI安全、AI伦理、AI治理等
- **其他**：其他AI相关主题

### 按重要性分类

- **高重要性**：
  - 包含重要关键词（如"突破"、"重大"、"首次"等）
  - 来自权威来源
  - 高关注度话题
  
- **中重要性**：一般性新闻
  
- **低重要性**：次要新闻或重复内容

### 按来源分类

自动识别新闻来源并分类。

## 项目结构

```
auto_sum_arxiv_daily/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖
├── config.yaml.example          # 配置文件模板
├── .github/
│   └── workflows/
│       └── daily_news.yml      # GitHub Actions工作流
├── src/
│   ├── __init__.py
│   ├── news_fetcher.py         # 新闻获取模块
│   ├── news_classifier.py      # 新闻分类模块
│   ├── news_summarizer.py      # 新闻总结模块
│   ├── email_sender.py         # 邮件发送模块
│   └── main.py                 # 主程序入口
└── .gitignore                  # Git忽略文件
```

## 注意事项

1. **邮箱安全**：建议使用应用专用密码而非账户密码
2. **API限制**：注意NewsAPI的免费额度限制
3. **敏感信息**：不要将 `config.yaml` 提交到Git仓库
4. **运行时间**：GitHub Actions的免费额度有限，注意使用频率

## 扩展功能

- 支持添加新的新闻源
- 支持自定义分类规则
- 支持多种邮件模板
- 支持数据持久化（可选）

## 许可证

MIT License

