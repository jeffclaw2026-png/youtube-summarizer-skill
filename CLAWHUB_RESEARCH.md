# ClawHub 發布研究報告

**日期：** 2026-03-10
**狀態：** 📋 研究中

---

## 📊 發現

### ClawHub 安裝結構

```
~/.npm-global/lib/node_modules/openclaw/skills/
├── github/
│   └── SKILL.md
├── clawhub/
│   └── SKILL.md
└── ...
```

**觀察：**
- 每個 skill 是一個資料夾
- 資料夾名稱 = skill slug
- 必須包含 SKILL.md
- 其他文件可選（README.md 等）

---

## 🔧 發布問題

### 問題 1：SKILL.md required

**錯誤訊息：**
```
Error: SKILL.md required
```

**可能原因：**
1. SKILL.md 格式問題
2. metadata 格式不正確
3. ClawHub 需要特定結構

### 嘗試的解決方案

```bash
# 方法 1：發布整個資料夾
clawhub publish . --slug youtube-summarizer ...

# 方法 2：發布 SKILL.md 文件
clawhub publish ./SKILL.md ...
```

---

## 📋 建議步驟

### 1. 檢查 SKILL.md 格式

對比現有 skill 的 SKILL.md：

```bash
# 查看 github skill
cat ~/.npm-global/lib/node_modules/openclaw/skills/github/SKILL.md | head -30
```

### 2. 創建標準結構

```
youtube-summarizer/
├── SKILL.md          # 必需
├── README.md         # 可選
├── youtube-summarizer.py  # 可選
└── requirements.txt  # 可選
```

### 3. 使用正確的發布命令

```bash
cd /home/jeff/papertowne/Projects
clawhub publish youtube-summarizer-skill \
  --slug youtube-summarizer \
  --name "YouTube Summarizer" \
  --version 1.0.0 \
  --changelog "Initial release"
```

---

## 🎯 下一步

- [ ] 對比現有 SKILL.md 格式
- [ ] 檢查 metadata 語法
- [ ] 嘗試發布到測試環境
- [ ] 聯繫 ClawHub 支持

---

## 🔗 參考

- **ClawHub:** https://clawhub.com
- **文檔：** https://docs.openclaw.ai/skills/clawhub
- **CLI 版本：** v0.7.0

---

_研究於：2026-03-10_
