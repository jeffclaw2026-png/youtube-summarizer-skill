#!/usr/bin/env python3
"""
YouTube 摘要工作流 - 使用 OpenClaw sub-agent 生成高質量摘要

功能：
1. 自動檢測字幕
2. 有字幕 → 直接提取
3. 無字幕 → Faster Whisper 轉錄
4. OpenClaw sub-agent 分析並創建筆記
5. Git 同步

使用方式：
python3 youtube-summarizer.py "https://youtu.be/VIDEO_ID"
"""

import os
import sys
import subprocess
import re
from datetime import datetime

# 導入依賴
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("✅ youtube-transcript-api 已安裝")
except ImportError:
    print("❌ 請安裝：pip install youtube-transcript-api")
    sys.exit(1)

try:
    from faster_whisper import WhisperModel
    print("✅ faster-whisper 已安裝")
except ImportError:
    print("❌ 請安裝：pip install faster-whisper")
    sys.exit(1)


def extract_video_id(url):
    """從 YouTube URL 提取 video ID"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]+)',
        r'v=([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def download_audio(video_url, output_path="/tmp/video_audio.webm"):
    """使用 yt-dlp 下載音頻"""
    print(f"\n📥 下載音頻：{video_url}")
    
    cmd = [
        'yt-dlp',
        '--js-runtimes', 'node',
        '-f', 'bestaudio[ext=webm]',
        '-o', output_path,
        video_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"✅ 下載成功：{size_mb:.2f} MB")
        return output_path
    else:
        print(f"❌ 下載失敗：{result.stderr}")
        return None


def get_transcript(video_id):
    """嘗試提取 YouTube 字幕"""
    print(f"\n📝 嘗試提取字幕：{video_id}")
    
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # 直接獲取字幕（新 API）
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh', 'zh-Hans', 'zh-Hant', 'en', 'yue'])
        
        text = ' '.join([t['text'] for t in transcript])
        
        print(f"✅ 成功提取字幕：{len(text)} 字元")
        return text
        
    except Exception as e:
        print(f"❌ 無字幕：{e}")
        return None


def transcribe_audio(audio_path, model_size="tiny"):
    """使用 Faster Whisper 轉錄"""
    print(f"\n🎙️ 開始轉錄：{audio_path}")
    print(f"模型：{model_size}")
    
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, language="zh")
    
    print(f"語言：{info.language} ({info.language_probability:.2%})")
    
    # 組合文字
    text = ' '.join([segment.text for segment in segments])
    
    print(f"✅ 轉錄完成：{len(text)} 字元")
    return text


def ai_summarize(transcript, video_id):
    """使用 OpenClaw sub-agent 生成高質量摘要"""
    print(f"\n🤖 AI 分析中（OpenClaw sub-agent）...")
    
    # 截取前 15000 字
    transcript_preview = transcript[:15000]
    
    prompt = f"""請為這個 YouTube 影片創建專業級結構化摘要。

**轉錄內容：**
{transcript_preview}

---

請用繁體中文生成以下格式的摘要：

## 🎬 影片簡介

（一句話說明影片主題，50 字內）

## 📝 重點摘要

### 核心痛點
（列出 2-4 個影片討論的問題）

### 解決方案
（影片提出的核心解決方案）

### 關鍵技術/方法
（技術要點、架構、工具）

### 實際應用場景
（如果有，列出應用場景）

## ⚠️ 潛在風險與挑戰

（批判性思考：限制、風險、挑戰）

## 💡 關鍵洞察

（深度分析、洞察、趨勢判斷）

## 🔗 相關資源

（提到的數據、作者、項目、連結等）

---
注意：
1. 使用繁體中文
2. 格式整潔，使用 Markdown
3. 每個部分精簡，避免冗長
4. 如果某些部分不適用，可以省略
"""
    
    try:
        # 使用 sessions_send 調用 main session
        workspace = "/home/jeff/papertowne/Manager/Obsidian-AI-Notes"
        result = subprocess.run(
            ['openclaw', 'sessions_send', '--label', 'note', '--message', prompt],
            capture_output=True, text=True, timeout=180, cwd=workspace
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ AI 分析完成")
            return result.stdout.strip()
        else:
            print(f"⚠️ AI 分析失敗：{result.stderr[:200] if result.stderr else '無回應'}")
            return None
    except Exception as e:
        print(f"⚠️ AI 分析異常：{e}")
        return None


def create_note(video_id, transcript, video_url, ai_summary=None):
    """創建筆記"""
    print(f"\n📝 創建筆記...")
    
    # 建議的 MOC
    moc_suggestions = "[[🗺️ AI MOC]]"
    
    # 根據內容判斷 MOC
    if "OpenClaw" in transcript:
        moc_suggestions += " [[🗺️ OpenClaw MOC]]"
    if "Obsidian" in transcript or "筆記" in transcript:
        moc_suggestions += " [[🗺️ Obsidian MOC]]"
    if "Agent" in transcript or "框架" in transcript:
        moc_suggestions += " [[🗺️ AI MOC]]"
    
    # 筆記內容
    note_content = f"""# YouTube 影片摘要 - {video_id}

**影片連結：** {video_url}
**日期：** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**類型：** Sources
**標籤：** #YouTube #AI #摘要
**相關 MOC：** {moc_suggestions}
**轉錄方式：** {"字幕提取" if len(transcript) > 1000 else "Faster Whisper ASR"}
**字數：** {len(transcript):,} 字元

---

{ai_summary if ai_summary else "## 📝 重點整理\n\n（待補充）"}

---

## 🔍 完整轉錄

{transcript}

---

_自動生成於 {datetime.now().strftime('%Y-%m-%d %H:%M')}_
"""
    
    # 保存到 _Inbox
    output_dir = "/home/jeff/papertowne/Manager/Obsidian-AI-Notes/_Inbox"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"YouTube-{video_id}-摘要.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(note_content)
    
    print(f"✅ 筆記已保存：{filepath}")
    return filepath


def git_sync(filepath):
    """Git 同步"""
    print(f"\n🔄 Git 同步...")
    
    workspace = "/home/jeff/papertowne/Manager/Obsidian-AI-Notes"
    
    # Git add
    subprocess.run(['git', 'add', '.'], cwd=workspace, capture_output=True)
    
    # Git commit
    video_id = os.path.basename(filepath).split('-')[1]
    message = f"📝 YouTube 摘要：{video_id}"
    subprocess.run(['git', 'commit', '-m', message], cwd=workspace, capture_output=True)
    
    # Git push
    result = subprocess.run(['git', 'push'], cwd=workspace, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Git 同步成功")
    else:
        print(f"⚠️ Git push 失敗：{result.stderr}")


def process_video(video_url, model_size="tiny"):
    """處理 YouTube 影片的完整流程"""
    print("=" * 60)
    print("🎬 YouTube 摘要工作流")
    print("=" * 60)
    
    # 1. 提取 video ID
    video_id = extract_video_id(video_url)
    if not video_id:
        print(f"❌ 無法提取 video ID: {video_url}")
        return
    
    print(f"Video ID: {video_id}")
    
    # 2. 嘗試提取字幕
    transcript = get_transcript(video_id)
    
    # 3. 如果無字幕，下載音頻並轉錄
    if not transcript:
        audio_path = download_audio(video_url)
        if audio_path:
            transcript = transcribe_audio(audio_path, model_size)
            # 清理音頻文件
            os.remove(audio_path)
        else:
            print("❌ 無法處理影片")
            return
    
    # 4. AI 分析
    ai_summary = ai_summarize(transcript, video_id)
    
    # 5. 創建筆記
    filepath = create_note(video_id, transcript, video_url, ai_summary)
    
    # 6. Git 同步
    git_sync(filepath)
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式：python3 youtube-summarizer.py <YouTube_URL>")
        print("範例：python3 youtube-summarizer.py \"https://youtu.be/MtukF1C8epQ\"")
        sys.exit(1)
    
    video_url = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "tiny"
    
    process_video(video_url, model_size)
