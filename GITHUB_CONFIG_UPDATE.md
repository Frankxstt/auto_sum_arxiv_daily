# GitHub Actions 配置更新指南

本文档说明在添加翻译功能和中文RSS源后，需要在GitHub中更新的配置。

## 需要更新的配置

### 1. RSS_URLS（推荐更新）

**目的**: 添加中文RSS源，获取更多中文AI新闻

**操作步骤**:
1. 进入 GitHub 仓库的 **Settings** > **Secrets and variables** > **Actions**
2. 找到 `RSS_URLS` secret
3. 点击编辑，更新为包含中文源的URL列表

**推荐配置**（英文+中文混合）:
```
https://hnrss.org/frontpage,https://www.reddit.com/r/MachineLearning/.rss,https://rss.arxiv.org/rss/cs.AI,https://rss.arxiv.org/rss/cs.LG,https://www.36kr.com/feed,https://www.ifanr.com/feed,https://www.geekpark.net/rss,https://www.huxiu.com/rss/0.xml,https://www.leiphone.com/feed
```

**或者只使用英文源**（会自动翻译为中文）:
```
https://hnrss.org/frontpage,https://www.reddit.com/r/MachineLearning/.rss,https://rss.arxiv.org/rss/cs.AI,https://rss.arxiv.org/rss/cs.LG,https://techcrunch.com/feed/
```

### 2. TRANSLATION_ENABLED（可选，新增）

**目的**: 控制是否启用翻译功能

**操作步骤**:
1. 进入 GitHub 仓库的 **Settings** > **Secrets and variables** > **Actions**
2. 点击 **New repository secret**
3. 添加以下配置：

- **Name**: `TRANSLATION_ENABLED`
- **Value**: 
  - `true` - 启用翻译（推荐，默认值）
  - `false` - 禁用翻译

**注意**: 
- 如果不设置此Secret，系统默认启用翻译
- 翻译功能会将英文新闻的标题和摘要自动翻译为中文
- 中文RSS源的内容不需要翻译，系统会自动识别

## 完整配置清单

更新后的完整Secrets列表：

### 必需配置
- ✅ `EMAIL_HOST` - SMTP服务器地址
- ✅ `EMAIL_PORT` - SMTP端口
- ✅ `EMAIL_USER` - 发送邮箱账号
- ✅ `EMAIL_PASSWORD` - 邮箱密码/授权码
- ✅ `EMAIL_TO` - 接收邮箱地址

### 推荐配置
- ✅ `RSS_URLS` - RSS订阅源（建议包含中文源）
- ⚙️ `TRANSLATION_ENABLED` - 翻译功能开关（可选，默认启用）

### 可选配置
- ⚙️ `NEWS_API_KEY` - NewsAPI密钥（如果使用NewsAPI）

## 快速更新步骤

### 方法1: 只更新RSS源（推荐）

如果您只想添加中文RSS源，只需更新 `RSS_URLS`：

1. 进入 **Settings** > **Secrets and variables** > **Actions**
2. 找到 `RSS_URLS`，点击编辑
3. 在现有URL后添加中文源（用逗号分隔）：
   ```
   原有URL,https://www.36kr.com/feed,https://www.ifanr.com/feed,https://www.geekpark.net/rss
   ```

### 方法2: 完整配置（包含翻译控制）

1. 更新 `RSS_URLS`（如上）
2. 添加 `TRANSLATION_ENABLED`:
   - Name: `TRANSLATION_ENABLED`
   - Value: `true`（启用翻译）或 `false`（禁用翻译）

## 中文RSS源推荐列表

### 科技媒体
- `https://www.36kr.com/feed` - 36氪
- `https://www.ifanr.com/feed` - 爱范儿
- `https://www.geekpark.net/rss` - 极客公园
- `https://www.huxiu.com/rss/0.xml` - 虎嗅
- `https://www.leiphone.com/feed` - 雷锋网

### AI专业媒体
- `https://www.jiqizhixin.com/rss` - 机器之心

更多RSS源请查看 [RSS_SOURCES.md](RSS_SOURCES.md)

## 验证配置

更新配置后：

1. 进入 **Actions** 标签
2. 手动触发工作流测试
3. 查看运行日志，确认：
   - RSS源获取成功
   - 翻译功能正常工作（如果启用）
   - 邮件发送成功

## 注意事项

1. **RSS源格式**: 多个URL用逗号分隔，不要有空格
2. **翻译性能**: 翻译可能需要一些时间，特别是新闻较多时
3. **翻译限制**: 使用Google Translate免费API，可能有频率限制
4. **中文源**: 中文RSS源的内容不需要翻译，系统会自动识别

## 常见问题

### Q: 翻译功能是否必须启用？
A: 不是必须的。如果不设置 `TRANSLATION_ENABLED`，默认启用翻译。如果只想看中文源，可以设置为 `false`。

### Q: 如何知道翻译是否工作？
A: 查看工作流日志，如果看到"翻译失败"的警告，说明翻译功能有问题，但系统会返回原文。

### Q: 可以只使用中文源吗？
A: 可以。在 `RSS_URLS` 中只配置中文RSS源，并设置 `TRANSLATION_ENABLED: false`。

### Q: 翻译会影响性能吗？
A: 可能会稍微增加运行时间，但通常影响不大。如果新闻很多（>100条），可能需要更长时间。

## 下一步

配置更新完成后：
1. 提交代码更新（如果修改了工作流文件）
2. 手动触发一次工作流测试
3. 检查收到的邮件，确认翻译和中文源正常工作

享受您的中文AI新闻汇总服务！🎉

