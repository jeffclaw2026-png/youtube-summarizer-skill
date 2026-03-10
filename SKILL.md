---
name: youtube-summarizer
description: 自動將 YouTube 影片轉化為結構化筆記，支援本地 ASR 轉錄，完全免費
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
            {
              "id": "ffmpeg-macos",
              "kind": "shell",
              "command": "brew install ffmpeg",
              "label": "安裝 ffmpeg (macOS)",
            },
          ],
      },
  }
---

# YouTube Summarizer Skill

自動將 YouTube 影片轉化為結構化筆記。

## 使用方式

對 OpenClaw 說：
- 「幫我總結這條 YouTube 影片：[URL]」
- 「把這條影片做成筆記：[URL]」

## 功能

- ✅ 自動檢測字幕
- ✅ 本地 ASR 轉錄（無字幕時）
- ✅ 結構化筆記
- ✅ Git 同步

## 依賴

- ffmpeg
- yt-dlp
- youtube-transcript-api
- faster-whisper
