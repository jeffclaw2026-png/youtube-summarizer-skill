# 發布到 ClawHub 指南

**Skill：** YouTube Summarizer
**日期：** 2026-03-10
**狀態：** 📋 待發布

---

## 📋 發布步驟

### 1. 準備 SKILL.md

確保 SKILL.md 包含正確的 metadata：

```markdown
---
name: youtube-summarizer
description: 自動將 YouTube 影片轉化為結構化筆記，支援本地 ASR 轉錄
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["ffmpeg", "yt-dlp"] },
        "install":
          [
            {
              "id": "python-packages",
              "kind": "pip",
              "packages": ["youtube-transcript-api", "faster-whisper", "yt-dlp"],
              "label": "安裝 Python 套件",
            },
            {
              "id": "ffmpeg-ubuntu",
              "kind": "shell",
              "command": "sudo apt install ffmpeg",
              "label": "安裝 ffmpeg (Ubuntu)",
            },
          ],
      },
  }
---
```

### 2. 登入 ClawHub

```bash
clawhub login
clawhub whoami  # 確認登入狀態
```

**當前狀態：** ✅ 已登入（jeffrey2212）

### 3. 發布 Skill

```bash
cd /home/jeff/papertowne/Projects/youtube-summarizer-skill

# 發布 v1.0.0
clawhub publish . \
  --slug youtube-summarizer \
  --name "YouTube Summarizer" \
  --version 1.0.0 \
  --changelog "Initial release - 自動將 YouTube 影片轉化為結構化筆記" \
  --tags "latest,youtube,ai,summarizer,transcription"
```

### 4. 驗證發布

```bash
# 搜尋技能
clawhub search "youtube summarizer"

# 查看詳情
clawhub inspect youtube-summarizer
```

### 5. 安裝測試

```bash
# 在新目錄測試安裝
cd /tmp
clawhub install youtube-summarizer
```

---

## 🔧 更新技能

```bash
# 修改 SKILL.md 或代碼

# 更新版本號（semver）
# 1.0.0 → 1.0.1 (bug fix)
# 1.0.0 → 1.1.0 (minor feature)
# 1.0.0 → 2.0.0 (major breaking change)

# 發布更新
clawhub publish . \
  --slug youtube-summarizer \
  --version 1.0.1 \
  --changelog "Fix youtube-transcript API compatibility"
```

---

## 📊 發布清單

- [ ] SKILL.md metadata 正確
- [ ] README.md 完整
- [ ] requirements.txt 正確
- [ ] LICENSE 文件
- [ ] 版本號符合 semver
- [ ] changelog 描述清楚
- [ ] tags 合適
- [ ] 本地測試通過
- [ ] ClawHub 登入
- [ ] 發布成功
- [ ] 安裝測試通過

---

## 🎯 最佳實踐

### 版本號規則（SemVer）

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Bug fixes
  │     └─────── New features (backward compatible)
  └───────────── Breaking changes
```

### Changelog 撰寫

```markdown
# 1.0.1 (2026-03-10)
- Fix youtube-transcript API compatibility
- Update README with more examples

# 1.0.0 (2026-03-10)
- Initial release
- Support subtitle extraction
- Support local ASR transcription (Faster Whisper)
- Auto Git sync
```

### Tags 建議

```
latest,youtube,ai,summarizer,transcription,notes,openclaw,skill
```

---

## ⚠️ 注意事項

### 發布前檢查

1. **SKILL.md 格式** - 確保 metadata 正確
2. **依賴清單** - requirements.txt 完整
3. **測試** - 本地測試通過
4. **文檔** - README.md 清晰

### 發布後驗證

1. **搜尋** - clawhub search 能找到
2. **安裝** - clawhub install 成功
3. **使用** - 功能正常運作

---

## 🔗 相關資源

| 資源 | 連結 |
|------|------|
| **ClawHub** | https://clawhub.com |
| **ClawHub CLI** | npm package: clawhub |
| **文檔** | https://docs.openclaw.ai/skills/clawhub |

---

_指南版本：1.0_
_最後更新：2026-03-10_
