# 推荐的RSS新闻源

本文档列出了一些推荐的AI相关RSS新闻源，可以直接在配置中使用。

## ArXiv论文

**重要**: ArXiv的RSS feed URL格式是 `https://rss.arxiv.org/rss/[分类]`，不是HTML页面URL。

### AI相关分类：
- `https://rss.arxiv.org/rss/cs.AI` - 人工智能
- `https://rss.arxiv.org/rss/cs.LG` - 机器学习
- `https://rss.arxiv.org/rss/cs.CL` - 计算语言学
- `https://rss.arxiv.org/rss/cs.CV` - 计算机视觉
- `https://rss.arxiv.org/rss/cs.NE` - 神经网络与进化计算
- `https://rss.arxiv.org/rss/cs.RO` - 机器人学

### 组合多个分类：
可以在配置中使用多个ArXiv分类的RSS源。

## 技术新闻网站

- `https://hnrss.org/frontpage` - Hacker News
- `https://techcrunch.com/feed/` - TechCrunch
- `https://feeds.feedburner.com/oreilly/radar` - O'Reilly Radar（可能不稳定）

## Reddit

- `https://www.reddit.com/r/MachineLearning/.rss` - r/MachineLearning
- `https://www.reddit.com/r/artificial/.rss` - r/artificial
- `https://www.reddit.com/r/compsci/.rss` - r/compsci

## AI专业网站

- `https://www.artificialintelligence-news.com/feed/` - AI News
- `https://venturebeat.com/ai/feed/` - VentureBeat AI

## 配置示例

在 `config.yaml` 或 GitHub Secrets 的 `RSS_URLS` 中配置（多个URL用逗号分隔）：

```yaml
rss_urls:
  - https://hnrss.org/frontpage
  - https://www.reddit.com/r/MachineLearning/.rss
  - https://rss.arxiv.org/rss/cs.AI
  - https://rss.arxiv.org/rss/cs.LG
  - https://techcrunch.com/feed/
```

或者在GitHub Secrets中：

```
RSS_URLS: https://hnrss.org/frontpage,https://www.reddit.com/r/MachineLearning/.rss,https://rss.arxiv.org/rss/cs.AI
```

## 常见错误

### ❌ 错误的ArXiv URL：
- `https://arxiv.org/list/cs.AI/recent?show=100` - 这是HTML页面，不是RSS feed

### ✅ 正确的ArXiv URL：
- `https://rss.arxiv.org/rss/cs.AI` - 这是RSS feed

## 测试RSS源

可以使用以下方法测试RSS源是否有效：

1. 在浏览器中打开RSS URL，应该看到XML格式的内容
2. 使用在线RSS验证工具
3. 运行程序时查看日志输出

## 注意事项

- 某些RSS源可能有访问频率限制
- 某些RSS源可能需要特定的User-Agent
- 如果某个RSS源经常失败，可以暂时移除它

