#!/usr/bin/env python3
"""
YouTube 摘要工作流 - 自動處理有字幕/無字幕影片

功能：
1. 自動檢測字幕
2. 有字幕 → 直接提取
3. 無字幕 → Faster Whisper 轉錄
4. AI 分析並創建筆記
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
    """使用關鍵詞提取 + 模板生成結構化摘要"""
    print(f"\n🤖 AI 分析中（關鍵詞提取模式）...")
    
    # 提取關鍵詞和短語
    import re
    from collections import Counter
    
    # 中英文停用詞列表
    stopwords = set(['the', 'and', 'can', 'that', 'you', 'this', 'have', 'here', 'see', 'just', 
                     'is', 'are', 'was', 'were', 'be', 'been', 'being', 'to', 'of', 'in', 'for',
                     'on', 'with', 'at', 'by', 'from', 'as', 'it', 'i', 'my', 'we', 'he', 'she',
                     'they', 'them', 'their', 'what', 'so', 'if', 'but', 'or', 'about', 'into',
                     'would', 'could', 'should', 'will', 'going', 'get', 'got', 'like', 'now',
                     'then', 'when', 'where', 'which', 'who', 'how', 'all', 'each', 'every',
                     'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'not', 'only',
                     'same', 'than', 'too', 'very', 's', 't', 'd', 'll', 've', 're', 'm', 'll',
                     '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一個',
                     '上', '也', '很', '到', '說', '要', '去', '你', '會', '著', '沒有', '看', '好',
                     '自己', '這', '那', '他', '她', '它', '們', '這個', '那個', '什麼', '怎麼', '可以'])
    
    # 判斷語言（中文 or 英文）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', transcript))
    is_chinese = chinese_chars > len(transcript) * 0.3
    
    if is_chinese:
        # 中文關鍵詞提取（名詞短語，2-6 字）
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,6}', transcript)
    else:
        # 英文關鍵詞提取（名詞短語，2-4 詞）
        # 提取大寫專有名詞
        proper_nouns = re.findall(r'\b[A-Z][a-zA-Z0-9+_.-]{2,30}\b', transcript)
        # 提取名詞短語（2-4 詞）
        noun_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b', transcript)
        # 合併
        keywords = proper_nouns + noun_phrases
    
    # 過濾停用詞和太短的詞
    keywords = [w for w in keywords if w.lower() not in stopwords and len(w) >= 3]
    
    # 統計頻率
    word_freq = Counter(keywords)
    
    # 獲取最頻繁的 10-15 個關鍵詞
    top_keywords = [word for word, count in word_freq.most_common(25) if count >= 2][:15]
    
    # 提取數字和統計數據
    numbers = re.findall(r'(\d+[.,]?\d*)\s*(%|K|M|B|萬 | 億 | 小時 | 分鐘 | 天 | 年 | 個月 | 美元 | 元 | agents | jobs)?', transcript)
    numbers_filtered = [(n[0], n[1]) for n in numbers if n[0] and len(n[0]) <= 6][:10]
    
    # 提取問題（英文 + 中文）
    if is_chinese:
        questions = re.findall(r'([^\?？]{10,50}[\?？])', transcript[:8000])
    else:
        questions = re.findall(r'([^\?]{10,50}\?)', transcript[:8000])
    questions_filtered = [q.strip() for q in questions if len(q.strip()) > 15][:5]
    
    # 提取章節/主題線索
    if is_chinese:
        topics = re.findall(r'(?:首先 | 第一 | 第二 | 第三 | 接下來 | 然後 | 最後 | 總結 | 重點).{0,30}', transcript[:8000])
    else:
        topics = re.findall(r'(?:First|Second|Third|Next|Then|Finally|In conclusion|The first|The second|Now let|Today I|I\'m going to).{0,40}', transcript[:8000], re.IGNORECASE)
    topics_filtered = list(set([t.strip() for t in topics]))[:5]
    
    # 生成結構化摘要
    summary = f"""### 1. 核心主題
（待補充 - 轉錄字數：{len(transcript):,}）

### 2. 關鍵詞
{', '.join(top_keywords) if top_keywords else '（待補充）'}

### 3. 重要數據
{chr(10).join(f'- {num[0]}{num[1]}' for num in numbers_filtered) if numbers_filtered else '（待補充）'}

### 4. 提到的問題
{chr(10).join(f'- {q}' for q in questions_filtered) if questions_filtered else '（待補充）'}

### 5. 章節/主題線索
{chr(10).join(f'- {t}' for t in topics_filtered) if topics_filtered else '（待補充）'}

## 💡 洞察與反思

（待手動補充）

## 🔗 相關主題

（待手動補充）
"""
    
    print(f"✅ 關鍵詞分析完成（提取 {len(top_keywords)} 個關鍵詞，語言：{'中文' if is_chinese else '英文'}）")
    return summary


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

**影片連結：** https://youtu.be/{video_id}
**日期：** {datetime.now().strftime('%Y-%m-%d')}
**類型：** Sources
**標籤：** #YouTube #AI #摘要
**相關 MOC：** {moc_suggestions}
**轉錄方式：** {"字幕提取" if len(transcript) > 1000 else "Faster Whisper ASR"}
**字數：** {len(transcript)} 字元

---

## 📝 重點整理

{ai_summary if ai_summary else "（待補充）"}

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
    
    # 4. AI 分析（可選，如果太長則跳過）
    ai_summary = None
    if len(transcript) <= 50000:  # 超過 50000 字跳過 AI 分析
        ai_summary = ai_summarize(transcript, video_id)
    else:
        print("\n⚠️ 轉錄內容過長，跳過 AI 分析")
    
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
