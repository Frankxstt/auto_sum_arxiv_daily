# GitHub Actions 配置指南

本指南将帮助您配置GitHub Actions，实现每天自动获取和发送AI新闻汇总。

## 前置条件

1. 已创建GitHub仓库
2. 已将代码推送到GitHub仓库
3. 已准备好邮箱SMTP配置信息

## 配置步骤

### 步骤1: 进入仓库设置

1. 打开您的GitHub仓库页面
2. 点击 **Settings**（设置）标签
3. 在左侧菜单中找到 **Secrets and variables**（密钥和变量）
4. 点击 **Actions**

### 步骤2: 添加必需的Secrets

点击 **New repository secret**（新建仓库密钥）按钮，逐个添加以下密钥：

#### 必需配置

##### 1. EMAIL_HOST
- **Name**: `EMAIL_HOST`
- **Value**: SMTP服务器地址
  - Gmail: `smtp.gmail.com`
  - Outlook: `smtp-mail.outlook.com`
  - QQ邮箱: `smtp.qq.com`
  - 163邮箱: `smtp.163.com`

##### 2. EMAIL_PORT
- **Name**: `EMAIL_PORT`
- **Value**: SMTP端口号
  - Gmail: `587`
  - Outlook: `587`
  - QQ邮箱: `587` 或 `465`
  - 163邮箱: `465`

##### 3. EMAIL_USER
- **Name**: `EMAIL_USER`
- **Value**: 发送邮件的邮箱账号（完整邮箱地址）
  - 例如: `your_email@gmail.com`

##### 4. EMAIL_PASSWORD
- **Name**: `EMAIL_PASSWORD`
- **Value**: 邮箱密码或应用专用密码
  - **重要**: Gmail必须使用应用专用密码，不能使用账户密码
  - **Gmail应用专用密码获取方法**:
    1. 登录Google账号
    2. 进入 [Google账号管理](https://myaccount.google.com/)
    3. 左侧菜单选择 **安全性**
    4. 找到 **两步验证** 并启用（如果未启用）
    5. 在 **应用专用密码** 部分生成新密码
    6. 复制生成的16位密码作为 `EMAIL_PASSWORD` 的值

##### 5. EMAIL_TO
- **Name**: `EMAIL_TO`
- **Value**: 接收新闻汇总的邮箱地址
  - 例如: `recipient@example.com`
  - 可以与 `EMAIL_USER` 相同（发送给自己）

#### 可选配置

##### 6. RSS_URLS
- **Name**: `RSS_URLS`
- **Value**: RSS订阅源URL列表，多个URL用逗号分隔
  - 例如: `https://hnrss.org/frontpage,https://www.reddit.com/r/MachineLearning/.rss`
  - 如果不设置，将使用代码中的默认RSS源

##### 7. NEWS_API_KEY
- **Name**: `NEWS_API_KEY`
- **Value**: NewsAPI密钥（可选）
  - 如果不需要使用NewsAPI，可以不设置此密钥
  - 获取方法: 访问 [NewsAPI官网](https://newsapi.org/) 注册并获取免费API密钥

### 步骤3: 验证配置

配置完成后，您的Secrets列表应该包含以下项：

```
✅ EMAIL_HOST
✅ EMAIL_PORT
✅ EMAIL_USER
✅ EMAIL_PASSWORD
✅ EMAIL_TO
✅ RSS_URLS (可选)
✅ NEWS_API_KEY (可选)
```

### 步骤4: 测试工作流

1. 进入仓库的 **Actions** 标签
2. 在左侧找到 **AI新闻每日汇总** 工作流
3. 点击工作流名称
4. 点击右侧的 **Run workflow**（运行工作流）按钮
5. 选择分支（通常是 `main` 或 `master`）
6. 点击绿色的 **Run workflow** 按钮

### 步骤5: 查看运行结果

1. 在工作流运行页面，点击最新的运行记录
2. 查看各个步骤的执行情况
3. 如果成功，您应该会收到邮件
4. 如果失败，点击失败的步骤查看错误日志

## 常见问题

### 1. 邮件发送失败

**问题**: 工作流运行成功但未收到邮件

**解决方案**:
- 检查 `EMAIL_PASSWORD` 是否正确（Gmail必须使用应用专用密码）
- 检查 `EMAIL_HOST` 和 `EMAIL_PORT` 是否正确
- 检查邮箱是否启用了SMTP服务
- 查看工作流日志中的错误信息

### 2. Gmail认证失败

**问题**: SMTP认证错误

**解决方案**:
- 确保已启用两步验证
- 使用应用专用密码而非账户密码
- 检查是否允许"不够安全的应用"访问（旧版Gmail设置）

### 3. 工作流未自动运行

**问题**: 定时任务没有触发

**解决方案**:
- GitHub Actions的定时任务需要仓库是公开的，或者您有GitHub Pro/Team/Enterprise账户
- 检查cron表达式是否正确
- 等待一段时间（GitHub Actions可能有延迟）

### 4. RSS源获取失败

**问题**: 无法获取RSS源新闻

**解决方案**:
- 检查RSS URL是否可访问
- 某些RSS源可能需要特殊处理
- 查看工作流日志了解具体错误

## 修改运行时间

默认运行时间为每天UTC 0:00（北京时间8:00）。如需修改，编辑 `.github/workflows/daily_news.yml` 文件中的cron表达式：

```yaml
schedule:
  - cron: '0 0 * * *'  # 格式: 分钟 小时 日 月 星期
```

**示例**:
- `'0 8 * * *'` - 每天UTC 8:00（北京时间16:00）
- `'0 12 * * 1'` - 每周一UTC 12:00
- `'30 6 * * *'` - 每天UTC 6:30

## 手动触发

除了定时运行，您也可以随时手动触发工作流：

1. 进入 **Actions** 标签
2. 选择 **AI新闻每日汇总** 工作流
3. 点击 **Run workflow**
4. 选择分支并运行

## 监控和日志

- 所有运行记录都在 **Actions** 标签中可见
- 如果运行失败，日志文件会自动上传为artifact
- 可以在工作流中查看详细的执行日志

## 安全提示

1. **永远不要**将敏感信息（如密码、API密钥）提交到代码仓库
2. 使用GitHub Secrets存储所有敏感配置
3. 定期更新应用专用密码
4. 如果不再使用，及时删除Secrets

## 下一步

配置完成后，系统将：
- 每天自动运行（根据cron设置）
- 从配置的RSS源获取AI相关新闻
- 对新闻进行分类和总结
- 发送HTML格式的邮件到指定邮箱

享受您的AI新闻每日汇总服务！🎉

