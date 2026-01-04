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

## 中文RSS源

### 科技媒体
- `https://www.36kr.com/feed` - 36氪（科技新闻）
- `https://www.ifanr.com/feed` - 爱范儿（科技资讯）
- `https://www.geekpark.net/rss` - 极客公园（科技媒体）
- `https://www.huxiu.com/rss/0.xml` - 虎嗅（科技商业）
- `https://www.leiphone.com/feed` - 雷锋网（AI科技）
- `https://www.pingwest.com/feed` - PingWest品玩
- `https://www.techxuexi.com/feed` - 科技讯息

### AI/技术社区
- `https://www.jiqizhixin.com/rss` - 机器之心（AI专业媒体）
- `https://www.atyun.com/feed` - 人工智能头条
- `https://www.ctoutiao.com/feed` - 创头条

### 开发者社区
- `https://www.oschina.net/news/rss` - 开源中国
- `https://www.infoq.cn/feed` - InfoQ中文站

**注意**: 某些中文RSS源可能需要验证或可能不稳定，建议测试后使用。

## 配置示例

在 `config.yaml` 或 GitHub Secrets 的 `RSS_URLS` 中配置（多个URL用逗号分隔）：

```yaml
# 英文源 + 中文源混合配置
rss_urls:
  # 英文源
  - https://hnrss.org/frontpage
  - https://www.reddit.com/r/MachineLearning/.rss
  - https://rss.arxiv.org/rss/cs.AI
  - https://rss.arxiv.org/rss/cs.LG
  - https://techcrunch.com/feed/
  
  # 中文源
  - https://www.36kr.com/feed
  - https://www.ifanr.com/feed
  - https://www.geekpark.net/rss
  - https://www.huxiu.com/rss/0.xml
  - https://www.leiphone.com/feed
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

