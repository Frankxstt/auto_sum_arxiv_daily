# 将代码部署到GitHub并配置Actions

本指南将帮助您将本地代码推送到GitHub，并配置GitHub Actions自动运行。

## 步骤1: 初始化Git仓库（如果尚未初始化）

在项目根目录执行：

```bash
cd /Users/fengxiushi/Documents/AI_Coding/auto_sum_arxiv_daily

# 初始化git仓库
git init

# 配置git用户信息（如果尚未配置全局）
git config user.name "Frankxstt"
git config user.email "xiushi.feng2021@gmail.com"
```

## 步骤2: 添加文件到Git

```bash
# 查看当前状态
git status

# 添加所有文件（.gitignore会自动排除敏感文件）
git add .

# 查看将要提交的文件
git status
```

**注意**: `config.yaml` 文件会被自动忽略（已在.gitignore中配置），不会提交到GitHub。

## 步骤3: 创建初始提交

```bash
# 创建提交
git commit -m "Initial commit: AI新闻自动汇总系统"

# 查看提交历史
git log --oneline
```

## 步骤4: 在GitHub上创建新仓库

1. 登录GitHub
2. 点击右上角的 **+** 号，选择 **New repository**
3. 填写仓库信息：
   - **Repository name**: `auto_sum_arxiv_daily`（或您喜欢的名称）
   - **Description**: `AI新闻自动汇总系统 - 每天自动获取、分类和发送AI相关新闻`
   - **Visibility**: 
     - 选择 **Public**（免费账户可以使用Actions定时任务）
     - 或选择 **Private**（需要GitHub Pro/Team账户才能使用定时任务）
   - **不要**勾选 "Initialize this repository with a README"（因为本地已有代码）
4. 点击 **Create repository**

## 步骤5: 连接本地仓库到GitHub

GitHub会显示设置说明，执行以下命令：

```bash
# 添加远程仓库（将YOUR_USERNAME替换为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/auto_sum_arxiv_daily.git

# 或者使用SSH（如果您配置了SSH密钥）
# git remote add origin git@github.com:YOUR_USERNAME/auto_sum_arxiv_daily.git

# 验证远程仓库
git remote -v
```

## 步骤6: 推送代码到GitHub

```bash
# 重命名分支为main（如果当前是master）
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

如果提示输入用户名和密码：
- 用户名：您的GitHub用户名
- 密码：使用Personal Access Token（不是GitHub密码）
  - 生成Token: GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
  - 权限选择：至少需要 `repo` 权限

## 步骤7: 配置GitHub Actions Secrets

代码推送成功后，需要配置Secrets才能让Actions正常工作：

### 7.1 进入Secrets设置

1. 在GitHub仓库页面，点击 **Settings**（设置）
2. 左侧菜单选择 **Secrets and variables** > **Actions**
3. 点击 **New repository secret**

### 7.2 添加必需的Secrets

逐个添加以下Secrets（参考 [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) 获取详细说明）：

#### 必需配置

1. **EMAIL_HOST**
   - Name: `EMAIL_HOST`
   - Value: `smtp.gmail.com`（Gmail）或其他SMTP服务器

2. **EMAIL_PORT**
   - Name: `EMAIL_PORT`
   - Value: `587`

3. **EMAIL_USER**
   - Name: `EMAIL_USER`
   - Value: 您的邮箱地址，例如 `your_email@gmail.com`

4. **EMAIL_PASSWORD**
   - Name: `EMAIL_PASSWORD`
   - Value: 邮箱密码或应用专用密码
   - ⚠️ Gmail必须使用应用专用密码

5. **EMAIL_TO**
   - Name: `EMAIL_TO`
   - Value: 接收邮件的邮箱地址

#### 可选配置

6. **RSS_URLS**（可选）
   - Name: `RSS_URLS`
   - Value: RSS订阅源URL，多个用逗号分隔
   - 例如: `https://hnrss.org/frontpage,https://www.reddit.com/r/MachineLearning/.rss`

7. **NEWS_API_KEY**（可选）
   - Name: `NEWS_API_KEY`
   - Value: NewsAPI密钥（如果使用NewsAPI）

## 步骤8: 测试GitHub Actions

### 8.1 手动触发测试

1. 在GitHub仓库页面，点击 **Actions** 标签
2. 左侧选择 **AI新闻每日汇总** 工作流
3. 点击右侧的 **Run workflow** 按钮
4. 选择分支（通常是 `main`）
5. 点击绿色的 **Run workflow** 按钮

### 8.2 查看运行结果

1. 在工作流运行页面，点击最新的运行记录
2. 查看各个步骤的执行情况：
   - ✅ 绿色表示成功
   - ❌ 红色表示失败
3. 点击失败的步骤查看详细错误信息

### 8.3 检查邮件

如果所有步骤都成功，您应该会收到一封包含AI新闻汇总的邮件。

## 步骤9: 验证定时任务

### 9.1 检查定时任务配置

定时任务默认每天UTC 0:00运行（北京时间8:00）。

查看配置：`.github/workflows/daily_news.yml`

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天UTC 0:00
```

### 9.2 修改运行时间（可选）

如果需要修改运行时间，编辑 `.github/workflows/daily_news.yml`：

```bash
# 在本地编辑文件
# 修改cron表达式后，提交并推送
git add .github/workflows/daily_news.yml
git commit -m "修改定时任务运行时间"
git push
```

**Cron表达式示例**：
- `'0 8 * * *'` - 每天UTC 8:00（北京时间16:00）
- `'0 12 * * 1'` - 每周一UTC 12:00
- `'30 6 * * *'` - 每天UTC 6:30

### 9.3 定时任务注意事项

⚠️ **重要提示**：
- **公开仓库**：免费账户可以使用定时任务
- **私有仓库**：需要GitHub Pro/Team/Enterprise账户才能使用定时任务
- 如果仓库是私有的，定时任务不会运行，但可以手动触发

## 步骤10: 后续更新代码

如果以后需要更新代码：

```bash
# 修改文件后
git add .
git commit -m "描述您的更改"
git push
```

GitHub Actions会在下次定时运行时使用最新代码。

## 故障排除

### 问题1: 推送被拒绝

**错误**: `error: failed to push some refs`

**解决方案**:
```bash
# 如果GitHub仓库有README等文件，先拉取
git pull origin main --allow-unrelated-histories
# 解决冲突后
git push -u origin main
```

### 问题2: Actions运行失败

**检查清单**:
- [ ] 所有必需的Secrets都已配置
- [ ] Secrets名称拼写正确（区分大小写）
- [ ] 邮箱配置正确（Gmail使用应用专用密码）
- [ ] RSS源URL可访问
- [ ] 查看Actions日志了解具体错误

### 问题3: 未收到邮件

**检查清单**:
- [ ] Actions运行成功（所有步骤都是绿色）
- [ ] 检查邮箱的垃圾邮件文件夹
- [ ] 验证EMAIL_TO配置正确
- [ ] 检查EMAIL_PASSWORD是否正确（Gmail必须使用应用专用密码）

### 问题4: 定时任务未运行

**可能原因**:
- 仓库是私有的，但账户是免费的（需要升级或改为公开仓库）
- Cron表达式有误
- GitHub Actions可能有延迟

**解决方案**:
- 检查仓库是否为公开
- 验证cron表达式格式
- 可以手动触发测试

## 快速命令参考

```bash
# 初始化仓库
git init
git add .
git commit -m "Initial commit"

# 连接GitHub
git remote add origin https://github.com/YOUR_USERNAME/auto_sum_arxiv_daily.git
git branch -M main
git push -u origin main

# 后续更新
git add .
git commit -m "Update"
git push
```

## 完成！

配置完成后，您的系统将：
- ✅ 每天自动运行（根据cron设置）
- ✅ 从配置的RSS源获取AI相关新闻
- ✅ 对新闻进行分类和总结
- ✅ 发送HTML格式的邮件到指定邮箱

享受您的AI新闻每日汇总服务！🎉

## 相关文档

- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - 详细的Actions配置指南
- [CONFIG_CHECKLIST.md](CONFIG_CHECKLIST.md) - 配置检查清单
- [README.md](README.md) - 项目说明文档

