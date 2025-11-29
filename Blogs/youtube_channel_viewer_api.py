"""
YouTube Channel Video Viewer - API Version
Enhanced version with YouTube Data API support for more reliable video fetching
Set up your API key for best results, or the app will use fallback methods
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
import os
from datetime import datetime
from pathlib import Path

try:
    import yt_dlp
    HAS_YT_DLP = True
except ImportError:
    HAS_YT_DLP = False


class YouTubeChannelViewerAPI:
    """
    YouTube Channel Viewer with API support
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Channel Video Viewer - API Edition")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configuration
        self.channel_handle = "@5MinutesEngineering"
        self.api_key = self.load_api_key()
        self.videos = []
        self.current_page = 0
        self.videos_per_page = 6
        self.is_loading = False
        
        # Setup style
        self.setup_styles()
        
        # Setup UI
        self.setup_ui()
        
        # Load videos on startup
        self.load_videos_thread()
    
    def setup_styles(self):
        """Configure application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', foreground='#333')
    
    def setup_ui(self):
        """Setup the user interface"""
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_header(main_container)
        self.create_content_area(main_container)
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="📺 YouTube Channel Videos", font=('Helvetica', 16, 'bold'))
        title_label.pack(anchor=tk.W, pady=5)
        
        subtitle_label = ttk.Label(header_frame, text="Dinesh Bohara - All Channel Videos", font=('Helvetica', 10))
        subtitle_label.pack(anchor=tk.W)
        
        self.status_label = ttk.Label(header_frame, text="Loading videos...", foreground='#0066cc')
        self.status_label.pack(anchor=tk.W, pady=5)
    
    def create_content_area(self, parent):
        """Create the main content area"""
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', yscrollcommand=scrollbar.set, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Use tk.Frame instead of ttk.Frame for background support
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)
    
    def on_frame_configure(self, event=None):
        """Update scroll region"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def create_footer(self, parent):
        """Create the footer with pagination"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        button_frame = ttk.Frame(footer_frame)
        button_frame.pack()
        
        self.prev_btn = ttk.Button(button_frame, text="← Previous", command=self.previous_page)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.page_label = ttk.Label(button_frame, text="Page 1", font=('Helvetica', 10))
        self.page_label.pack(side=tk.LEFT, padx=20)
        
        self.next_btn = ttk.Button(button_frame, text="Next →", command=self.next_page)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.load_videos_thread)
        refresh_btn.pack(side=tk.LEFT, padx=20)
        
        api_btn = ttk.Button(button_frame, text="Set API Key", command=self.set_api_key)
        api_btn.pack(side=tk.LEFT, padx=5)
    
    def load_api_key(self):
        """Load API key from file or return None"""
        api_key_file = Path(__file__).parent / ".youtube_api_key"
        if api_key_file.exists():
            with open(api_key_file, 'r') as f:
                return f.read().strip()
        return None
    
    def get_youtube_thumbnail_url(self, video_id, quality='high'):
        """
        Generate YouTube thumbnail URL from video ID
        quality options: 'default', 'medium', 'high', 'standard', 'maxres'
        """
        quality_map = {
            'default': f'https://i.ytimg.com/vi/{video_id}/default.jpg',
            'medium': f'https://i.ytimg.com/vi/{video_id}/mqdefault.jpg',
            'high': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
            'standard': f'https://i.ytimg.com/vi/{video_id}/sddefault.jpg',
            'maxres': f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg',
        }
        return quality_map.get(quality, quality_map['high'])
    
    def save_api_key(self, api_key):
        """Save API key to file"""
        api_key_file = Path(__file__).parent / ".youtube_api_key"
        with open(api_key_file, 'w') as f:
            f.write(api_key)
        self.api_key = api_key
    
    def set_api_key(self):
        """Open dialog to set YouTube API key"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Set YouTube API Key")
        dialog.geometry("500x200")
        
        ttk.Label(dialog, text="Enter your YouTube Data API key:").pack(pady=10)
        ttk.Label(dialog, text="Get one from: https://console.cloud.google.com/", foreground='#0066cc').pack()
        
        entry = ttk.Entry(dialog, width=50, show="*")
        entry.pack(pady=10, padx=20)
        
        if self.api_key:
            entry.insert(0, self.api_key)
        
        def save():
            api_key = entry.get().strip()
            if api_key:
                self.save_api_key(api_key)
                messagebox.showinfo("Success", "API key saved!")
                dialog.destroy()
                self.load_videos_thread()
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=5)
    
    def load_videos_thread(self):
        """Load videos in a separate thread"""
        if self.is_loading:
            return
        
        self.is_loading = True
        self.status_label.config(text="Loading videos from channel...")
        self.root.update()
        
        thread = threading.Thread(target=self.load_videos, daemon=True)
        thread.start()
    
    def load_videos(self):
        """Fetch videos from YouTube channel"""
        try:
            self.videos = self.fetch_channel_videos()
            self.current_page = 0
            
            if not self.videos:
                self.status_label.config(text="Could not load videos")
                messagebox.showwarning("Warning", "Could not load videos. Please check your connection or set an API key.")
            else:
                self.status_label.config(text=f"Loaded {len(self.videos)} videos")
            
            self.display_current_page()
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            print(f"Error loading videos: {e}")
        finally:
            self.is_loading = False
    
    def fetch_channel_videos(self):
        """Fetch videos using API or fallback methods"""
        videos = []
        
        # Try API method first
        if self.api_key:
            try:
                videos = self.fetch_with_api()
                if videos:
                    return videos
            except Exception as e:
                print(f"API method failed: {e}")
        
        # Try yt-dlp
        if HAS_YT_DLP:
            try:
                videos = self.fetch_with_ytdlp()
                if videos:
                    return videos
            except Exception as e:
                print(f"yt-dlp method failed: {e}")
        
        return []
    
    def fetch_with_api(self):
        """Fetch videos using YouTube Data API"""
        videos = []
        try:
            # Get channel ID from username
            channel_response = requests.get(
                'https://www.googleapis.com/youtube/v3/search',
                params={
                    'part': 'snippet',
                    'q': self.channel_handle,
                    'type': 'channel',
                    'key': self.api_key,
                },
                timeout=10
            )
            channel_response.raise_for_status()
            
            channel_id = channel_response.json()['items'][0]['id']['channelId']
            
            # Get videos from channel
            videos_response = requests.get(
                'https://www.googleapis.com/youtube/v3/search',
                params={
                    'part': 'snippet',
                    'channelId': channel_id,
                    'type': 'video',
                    'maxResults': 50,
                    'order': 'date',
                    'key': self.api_key,
                },
                timeout=10
            )
            videos_response.raise_for_status()
            
            items = videos_response.json().get('items', [])
            
            for item in items:
                snippet = item['snippet']
                video_id = item['id']['videoId']
                video = {
                    'id': video_id,
                    'title': snippet['title'],
                    'thumbnail': self.get_youtube_thumbnail_url(video_id, 'high'),
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'upload_date': snippet['publishedAt'],
                    'view_count': 0,
                }
                videos.append(video)
        
        except Exception as e:
            print(f"Error in fetch_with_api: {e}")
        
        return videos
    
    def fetch_with_ytdlp(self):
        """Fetch videos using yt-dlp"""
        videos = []
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                channel_url = f"https://www.youtube.com/{self.channel_handle}/videos"
                info = ydl.extract_info(channel_url, download=False)
                
                if 'entries' in info:
                    for entry in info['entries'][:50]:
                        video_id = entry.get('id')
                        video = {
                            'id': video_id,
                            'title': entry.get('title', 'Unknown'),
                            'thumbnail': self.get_youtube_thumbnail_url(video_id, 'high'),
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'upload_date': entry.get('upload_date', 'Unknown'),
                            'view_count': entry.get('view_count', 0),
                        }
                        videos.append(video)
        
        except Exception as e:
            print(f"Error in fetch_with_ytdlp: {e}")
        
        return videos
    
    def display_current_page(self):
        """Display videos for the current page"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.videos:
            no_videos_label = ttk.Label(self.scrollable_frame, text="No videos found", font=('Helvetica', 12))
            no_videos_label.pack(pady=50)
            return
        
        start_idx = self.current_page * self.videos_per_page
        end_idx = start_idx + self.videos_per_page
        page_videos = self.videos[start_idx:end_idx]
        
        total_pages = (len(self.videos) + self.videos_per_page - 1) // self.videos_per_page
        self.page_label.config(text=f"Page {self.current_page + 1} of {total_pages}")
        
        self.prev_btn.config(state=tk.DISABLED if self.current_page == 0 else tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED if end_idx >= len(self.videos) else tk.NORMAL)
        
        # Use tk.Frame for background support
        videos_frame = tk.Frame(self.scrollable_frame, bg='white')
        videos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for idx, video in enumerate(page_videos):
            col = idx % 3
            row = idx // 3
            self.create_video_card(videos_frame, video, row, col)
    
    def create_video_card(self, parent, video, row, col):
        """Create a video card widget"""
        card_frame = ttk.Frame(parent, relief=tk.RIDGE, borderwidth=1)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        card_frame.bind('<Button-1>', lambda e: self.open_video(video))
        card_frame.bind('<Enter>', lambda e: card_frame.config(relief=tk.RAISED))
        card_frame.bind('<Leave>', lambda e: card_frame.config(relief=tk.RIDGE))
        
        try:
            response = requests.get(video['thumbnail'], timeout=5)
            img = Image.open(BytesIO(response.content))
            img = img.resize((320, 180), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            thumb_label = tk.Label(card_frame, image=photo, cursor="hand2")
            thumb_label.image = photo
            thumb_label.pack()
            
            thumb_label.bind('<Button-1>', lambda e: self.open_video(video))
            thumb_label.bind('<Enter>', lambda e: card_frame.config(relief=tk.RAISED))
            thumb_label.bind('<Leave>', lambda e: card_frame.config(relief=tk.RIDGE))
        
        except Exception as e:
            placeholder = tk.Label(card_frame, text="[No Image]", bg='#cccccc', width=40, height=10)
            placeholder.pack()
        
        title_label = ttk.Label(card_frame, text=video['title'], wraplength=300, justify=tk.LEFT, font=('Helvetica', 9, 'bold'))
        title_label.pack(padx=5, pady=5, fill=tk.X)
        title_label.bind('<Button-1>', lambda e: self.open_video(video))
        
        details_frame = ttk.Frame(card_frame)
        details_frame.pack(padx=5, pady=3, fill=tk.X)
        
        upload_date = video.get('upload_date', 'Unknown')
        if upload_date != 'Unknown':
            try:
                dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                upload_date = dt.strftime('%d %b %Y')
            except:
                pass
        
        view_count = video.get('view_count', 0)
        views_text = f"{view_count:,} views" if view_count > 0 else "Recent"
        
        details_label = ttk.Label(details_frame, text=f"{views_text} • {upload_date}", font=('Helvetica', 8), foreground='#666')
        details_label.pack(fill=tk.X)
        details_label.bind('<Button-1>', lambda e: self.open_video(video))
    
    def open_video(self, video):
        """Open the video on YouTube"""
        url = video.get('url')
        if url:
            webbrowser.open(url)
        else:
            messagebox.showerror("Error", "Could not get video URL")
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()
            self.canvas.yview_moveto(0)
    
    def next_page(self):
        """Go to next page"""
        total_pages = (len(self.videos) + self.videos_per_page - 1) // self.videos_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.display_current_page()
            self.canvas.yview_moveto(0)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = YouTubeChannelViewerAPI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

