# YouTube Summarizer Skill

🎬 自動將 YouTube 影片轉化為結構化筆記

[![OpenCLaw Skill](https://img.shields.io/badge/OpenCLaw-Skill-blue)](https://github.com/openclaw/openclaw)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 概述

**YouTube Summarizer** 是一個 OpenCLaw Skill，自動將 YouTube 影片轉化為結構化筆記。

**核心優勢：**
- 🎯 自動檢測字幕（有字幕直接提取）
- 🎙️ 本地 ASR 轉錄（無字幕使用 Faster Whisper）
- 📝 結構化筆記（自動標籤、分類）
- 🔄 Git 同步（自動 commit + push）
- 💰 完全免費（無需 API Key）

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
# Ubuntu
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Python 套件
pip install youtube-transcript-api faster-whisper yt-dlp
```

### 2. 使用方式

```bash
# 基本使用
python3 youtube-summarizer.py "https://youtu.be/VIDEO_ID"

# 指定模型大小
python3 youtube-summarizer.py "URL" base
```

### 3. 輸出位置

筆記會保存到：`_Inbox/YouTube-VIDEO_ID-摘要.md`

---

## 📦 安裝

### 方法 A：使用 OpenCLaw

在 OpenClaw 中說：
```
安裝 youtube-summarizer skill
```

### 方法 B：手動安裝

```bash
# Clone Repo
git clone https://github.com/jeffrey2212/youtube-summarizer-skill.git

# 安裝依賴
cd youtube-summarizer-skill
pip install -r requirements.txt
```

---

## 🎯 使用範例

### 範例 1：有字幕影片

```bash
python3 youtube-summarizer.py "https://youtu.be/MtukF1C8epQ"
```

**輸出：**
```
✅ 成功提取字幕：5000 字元
📝 筆記已保存
✅ Git 同步成功
```

### 範例 2：無字幕影片

```bash
python3 youtube-summarizer.py "https://youtu.be/F-z_JtRwIYs"
```

**輸出：**
```
❌ 無字幕，使用 ASR
📥 下載音頻：13.17 MB
🎙️ 轉錄完成：5333 字元
📝 筆記已保存
✅ Git 同步成功
```

---

## ⚙️ 配置選項

### 模型大小

| 模型 | 速度 | 準確度 | 推薦場景 |
|------|------|--------|----------|
| **tiny** | ⚡ 最快 | ⭐⭐⭐ | 快速測試 |
| **base** | ⚡ 快速 | ⭐⭐⭐⭐ | 日常使用 |
| **small** | 🐌 中 | ⭐⭐⭐⭐⭐ | 正式使用 |
| **medium** | 🐌 慢 | ⭐⭐⭐⭐⭐ | 高精度 |
| **large** | 🐌 最慢 | ⭐⭐⭐⭐⭐ | 關鍵任務 |

### 使用方式

```bash
# tiny 模型（預設）
python3 youtube-summarizer.py "URL"

# base 模型
python3 youtube-summarizer.py "URL" base

# small 模型
python3 youtube-summarizer.py "URL" small
```

---

## 📊 性能數據

### 轉錄速度（9 分鐘影片）

| 模型 | 時間 | 準確度 |
|------|------|--------|
| **tiny** | ~30 秒 | 85% |
| **base** | ~60 秒 | 90% |
| **small** | ~2 分鐘 | 95% |
| **medium** | ~5 分鐘 | 97% |
| **large** | ~10 分鐘 | 98% |

---

## 🔧 故障排除

### 問題 1：ffmpeg 未安裝

```bash
# Ubuntu
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### 問題 2：無法下載音頻

```bash
# 更新 yt-dlp
pip install -U yt-dlp

# 安裝 nodejs（JavaScript runtime）
sudo apt install nodejs
```

### 問題 3：字幕提取失敗

自動切換到 ASR 轉錄，無需手動干預。

---

## 📁 文件結構

```
youtube-summarizer-skill/
├── SKILL.md                 # Skill 配置
├── README.md                # 使用說明
├── youtube-summarizer.py    # 主腳本
├── requirements.txt         # 依賴清單
├── examples/                # 範例
│   └── example-output.md
└── LICENSE                  # 授權
```

---

## 🎯 使用場景

### 1. 學習教程

```
YouTube 教程 → 結構化筆記 → Obsidian 知識庫
```

### 2. 會議記錄

```
會議錄影 → 轉錄文字 → 行動清單
```

### 3. 內容研究

```
多個相關影片 → 批量處理 → 主題筆記
```

### 4. 語言學習

```
外語影片 → 雙語轉錄 → 學習筆記
```

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

1. Fork 本專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 📄 授權

MIT License - 詳見 [LICENSE](LICENSE) 文件

---

## 🔗 相關資源

- [OpenCLaw](https://github.com/openclaw/openclaw)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [youtube-transcript-api](https://github.com/ndfreitas/youtube_transcript_api)

---

## 📝 更新日誌

### v1.0.0 (2026-03-10)

- ✅ 初始版本
- ✅ 字幕提取
- ✅ Faster Whisper ASR
- ✅ Git 同步
- ✅ 結構化筆記

---

_Made with ❤️ by Jeffrey Chan_
