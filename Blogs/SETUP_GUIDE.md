# YouTube Channel Video Viewer - Setup Guide

## Overview
This is a standalone Python program that displays all videos from your YouTube channel with thumbnails and details. Click on any video thumbnail to open it on YouTube.

## Features
✅ Displays all videos from your channel with thumbnails
✅ Shows video title, view count, and upload date
✅ Click on any video to open it directly on YouTube
✅ Pagination to browse through videos
✅ Automatic refresh functionality
✅ Responsive UI with mousewheel scrolling
✅ No API key required (uses multiple fallback methods)

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Installation

### Step 1: Install Required Packages
Open PowerShell and run:

```powershell
cd "C:\Users\dines\OneDrive\Documents\Blogs"
pip install -r requirements.txt
```

If you face any issues, install packages individually:
```powershell
pip install pillow
pip install requests
pip install yt-dlp
pip install beautifulsoup4
```

### Step 2: Run the Application
```powershell
cd "C:\Users\dines\OneDrive\Documents\Blogs"
python youtube_channel_viewer.py
```

## Usage
1. Launch the application - it will automatically load all videos from your channel
2. Browse through video cards displaying:
   - Video thumbnail
   - Video title
   - View count and upload date
3. Click on any video card to open it on YouTube
4. Use navigation buttons:
   - **Previous**: Go to the previous page
   - **Next**: Go to the next page
   - **Refresh**: Reload videos from the channel

## How It Works
The application uses multiple methods to fetch videos:
1. **Primary**: Uses yt-dlp library to extract video information
2. **Fallback**: Web scraping with BeautifulSoup
3. **Fallback**: Sample videos for demonstration

No YouTube API key is required! The program works by extracting data from the public channel page.

## Video Card Information
Each video card displays:
- **Thumbnail**: Preview image (click to open on YouTube)
- **Title**: Video title (wraps if too long)
- **View Count**: Total views on the video
- **Upload Date**: When the video was published

## Features
- **Auto-refresh**: Click the "Refresh" button to reload videos
- **Pagination**: Displays 6 videos per page
- **Mousewheel Support**: Scroll with mouse wheel
- **Direct Links**: Opening videos takes you directly to YouTube

## Troubleshooting

### Videos not loading?
1. Check your internet connection
2. Click "Refresh" button
3. Make sure yt-dlp is installed: `pip install --upgrade yt-dlp`

### Thumbnails not showing?
- The app will show placeholder text if thumbnails can't be downloaded
- This usually means a temporary network issue

### Application crashes?
1. Make sure all requirements are installed
2. Try running with: `python youtube_channel_viewer.py`
3. Check the console output for error messages

## Advanced: Customizing the Channel
To use a different YouTube channel, edit `youtube_channel_viewer.py`:

Find these lines (around line 68-70):
```python
self.channel_url = "https://www.youtube.com/@dineshbohara2918"
self.channel_handle = "dineshbohara2918"
```

Replace with your channel:
```python
self.channel_url = "https://www.youtube.com/@yourchannel"
self.channel_handle = "yourchannel"
```

Then restart the application.

## System Requirements
- **OS**: Windows, Mac, or Linux
- **RAM**: Minimum 512MB
- **Disk Space**: ~100MB for dependencies
- **Internet**: Required for video loading

## License
Created for Dinesh Bohara's YouTube Channel
Free to use and modify.

## Support
For issues or feature requests, check the YouTube channel documentation or modify the code as needed.
