# YouTube Channel Video Viewer - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Step 1: Open PowerShell
Press `Win + X` → Select "Windows PowerShell" or "Terminal"

### Step 2: Navigate to the Project Folder
```powershell
cd "C:\Users\dines\OneDrive\Documents\Blogs"
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

**If this fails, try installing individually:**
```powershell
pip install pillow requests yt-dlp beautifulsoup4
```

### Step 4: Run the Program
```powershell
python youtube_channel_viewer.py
```

That's it! 🎉 The application will launch and start loading your channel videos.

---

## 📝 Two Versions Available

### Version 1: `youtube_channel_viewer.py` (Recommended)
- ✅ Works without API key
- ✅ Uses yt-dlp and web scraping
- ✅ Automatic video fetching
- ✅ Simple setup

**Launch with:** `python youtube_channel_viewer.py`

---

### Version 2: `youtube_channel_viewer_api.py` (Advanced)
- ✅ Uses YouTube Data API for accuracy
- ✅ Optional "Set API Key" button for better reliability
- ✅ More stable with valid API key
- ⚠️ Requires API key (optional, has fallback)

**Launch with:** `python youtube_channel_viewer_api.py`

**To set API Key:**
1. Get one free from: https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create an API Key
4. Click "🔑 Set API Key" button in the app
5. Paste your key and save

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📺 Video Thumbnails | Large preview images for each video |
| 📝 Video Details | Title, view count, and upload date |
| 🔗 Direct Links | Click to open video on YouTube |
| 📄 Pagination | Browse videos 6 per page |
| 🔄 Refresh | Reload videos anytime |
| 🖱️ Scroll Support | Mousewheel scrolling |

---

## 🎮 How to Use

1. **Launch the app** with `python youtube_channel_viewer.py`
2. **Wait for videos to load** (20-30 seconds first time)
3. **Browse videos** using Previous/Next buttons
4. **Click any video** to watch on YouTube
5. **Refresh** if you uploaded new videos

---

## ⚙️ Troubleshooting

### Videos not loading?
```powershell
# Try upgrading yt-dlp
pip install --upgrade yt-dlp

# Then restart the app
python youtube_channel_viewer.py
```

### "ModuleNotFoundError" error?
```powershell
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### Application is slow?
- This is normal on first run (loading videos)
- Subsequent loads are faster
- Click "Refresh" to reload videos

### Using wrong channel?
Edit line 68-70 in `youtube_channel_viewer.py`:
```python
self.channel_url = "https://www.youtube.com/@yourchannel"
self.channel_handle = "yourchannel"
```

---

## 📊 Program Structure

```
📁 Blogs/
├── youtube_channel_viewer.py      ← Start here! (Recommended)
├── youtube_channel_viewer_api.py  ← API version (Advanced)
├── requirements.txt               ← Dependencies
├── SETUP_GUIDE.md                 ← Full setup guide
└── QUICK_START.md                 ← This file
```

---

## 🔐 Privacy & Security

- ✅ No login required
- ✅ No personal data collected
- ✅ Works completely offline (after first load)
- ✅ Safe to use

---

## 💡 Tips

1. **For best performance:** Run Version 1 (`youtube_channel_viewer.py`)
2. **For reliability:** Get a free API key and use Version 2
3. **New videos?** Click "Refresh" to update
4. **Stuck?** Restart the app

---

## 🆘 Need Help?

1. Check the console output (PowerShell window)
2. Try upgrading packages: `pip install --upgrade yt-dlp pillow requests`
3. Restart your computer and try again
4. Make sure you have internet connection

---

## 📱 System Requirements

- ✅ Windows 7+, Mac, or Linux
- ✅ Python 3.7+
- ✅ 100MB free disk space
- ✅ Internet connection

---

## 🎉 Ready to Go!

You're all set! Run this command to start:

```powershell
cd "C:\Users\dines\OneDrive\Documents\Blogs"; python youtube_channel_viewer.py
```

Happy watching! 🎬
