# GitHub Repo 推送指南

**Skill 名稱：** YouTube Summarizer
**本地位置：** `/home/jeff/papertowne/Projects/youtube-summarizer-skill/`

---

## 📋 推送步驟

### 方法 1：使用 GitHub Token（推薦）

```bash
cd /home/jeff/papertowne/Projects/youtube-summarizer-skill

# 1. 在 GitHub 創建新 Repo
# 訪問：https://github.com/new
# Repo 名稱：youtube-summarizer-skill
# 設為 Public

# 2. 創建 Personal Access Token
# 訪問：https://github.com/settings/tokens
# 權限：repo (full control)

# 3. 使用 token 推送
git remote set-url origin https://YOUR_TOKEN@github.com/jeffrey2212/youtube-summarizer-skill.git
git push -u origin main
```

### 方法 2：使用 SSH Key

```bash
# 1. 檢查 SSH key
ls -la ~/.ssh/id_rsa.pub

# 2. 如果沒有，創建一個
ssh-keygen -t rsa -b 4096 -C "jeffclaw2026@gmail.com"

# 3. 添加到 GitHub
# 訪問：https://github.com/settings/keys
# 複製 ~/.ssh/id_rsa.pub 的內容

# 4. 推送
cd /home/jeff/papertowne/Projects/youtube-summarizer-skill
git remote set-url origin git@github.com:jeffrey2212/youtube-summarizer-skill.git
git push -u origin main
```

---

## 🎯 快速推送（使用 gh CLI）

```bash
# 安裝 GitHub CLI
sudo apt install gh

# 登入
gh auth login

# 創建並推送
cd /home/jeff/papertowne/Projects/youtube-summarizer-skill
gh repo create youtube-summarizer-skill --public --source=. --remote=origin --push
```

---

## ✅ 驗證清單

推送完成後檢查：

- [ ] GitHub Repo 已創建
- [ ] 所有文件已上傳
- [ ] README.md 顯示正常
- [ ] 其他人可以 clone

---

## 📝 Repo 描述建議

**Name:** YouTube Summarizer Skill

**Description:**
```
🎬 OpenCLaw Skill - 自動將 YouTube 影片轉化為結構化筆記
支援本地 ASR 轉錄，完全免費，無需 API Key

✨ 功能：
- 自動檢測字幕
- Faster Whisper 本地轉錄
- 結構化筆記
- Git 自動同步

🚀 安裝：pip install -r requirements.txt
```

**Topics:**
- openclaw
- skill
- youtube
- summarizer
- ai
- transcription
- faster-whisper
- notes

---

_創建於：2026-03-10_
