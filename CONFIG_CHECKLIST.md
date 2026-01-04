# GitHub Actions 配置检查清单

使用此清单确保所有配置都正确完成。

## 必需配置项

### 邮箱配置

- [ ] **EMAIL_HOST** 已设置
  - Gmail: `smtp.gmail.com`
  - Outlook: `smtp-mail.outlook.com`
  - QQ邮箱: `smtp.qq.com`
  - 其他邮箱请查询对应SMTP服务器地址

- [ ] **EMAIL_PORT** 已设置
  - 通常为 `587` (TLS) 或 `465` (SSL)
  - Gmail和Outlook使用 `587`

- [ ] **EMAIL_USER** 已设置
  - 完整的邮箱地址，例如: `your_email@gmail.com`

- [ ] **EMAIL_PASSWORD** 已设置
  - ⚠️ **重要**: Gmail必须使用应用专用密码
  - 不是账户登录密码
  - 16位应用专用密码

- [ ] **EMAIL_TO** 已设置
  - 接收邮件的邮箱地址
  - 可以与EMAIL_USER相同

### 可选配置项

- [ ] **RSS_URLS** 已设置（可选）
  - 多个URL用逗号分隔
  - 例如: `https://hnrss.org/frontpage,https://www.reddit.com/r/MachineLearning/.rss`
  - 如果不设置，将使用代码中的默认RSS源

- [ ] **NEWS_API_KEY** 已设置（可选）
  - 仅在需要使用NewsAPI时设置
  - 从 https://newsapi.org/ 获取

## Gmail用户特别检查

如果您使用Gmail，请确认：

- [ ] 已启用两步验证
  - 访问: https://myaccount.google.com/security
  - 确认"两步验证"已启用

- [ ] 已生成应用专用密码
  - 访问: https://myaccount.google.com/apppasswords
  - 已生成并复制16位密码
  - 已将此密码设置为 `EMAIL_PASSWORD`

- [ ] 未使用账户登录密码
  - ⚠️ Gmail不允许使用账户密码通过SMTP发送邮件

## 测试步骤

1. [ ] 已将所有Secrets添加到GitHub仓库
2. [ ] 已推送代码到GitHub
3. [ ] 已手动触发工作流进行测试
4. [ ] 工作流运行成功
5. [ ] 已收到测试邮件

## 常见问题检查

如果工作流失败，请检查：

- [ ] Secrets名称拼写是否正确（区分大小写）
- [ ] Secrets值是否正确（无多余空格）
- [ ] 邮箱SMTP服务是否已启用
- [ ] 网络连接是否正常（GitHub Actions需要访问外部网络）
- [ ] RSS源URL是否可访问

## 验证命令

在本地测试配置（需要先创建config.yaml）：

```bash
# 安装依赖
pip install -r requirements.txt

# 测试运行（不发送邮件）
python src/main.py --no-email

# 测试运行（发送邮件）
python src/main.py
```

## 完成检查

所有项目都打勾后，您的GitHub Actions应该可以正常工作了！

如果遇到问题，请查看：
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - 详细配置指南
- GitHub Actions运行日志
- 工作流artifact中的日志文件

