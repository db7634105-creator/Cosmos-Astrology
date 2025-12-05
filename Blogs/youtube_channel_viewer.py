"""
YouTube Channel Video Viewer
A standalone Python program that fetches and displays all videos from a YouTube channel
with thumbnails and video details. Click on any video to open it on YouTube.

Author: Dinesh Bohara
Channel: https://youtube.com/@dineshbohara2918
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
import os
from datetime import datetime
import re

# Try to import yt-dlp as fallback, or use requests with beautifulsoup
try:
    import yt_dlp
    HAS_YT_DLP = True
except ImportError:
    HAS_YT_DLP = False

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False


class YouTubeChannelViewer:
    """
    Main application class for viewing YouTube channel videos
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Channel Video Viewer")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configuration
        self.channel_url = "https://www.youtube.com/@DineshBohara"  # Using channel handle for yt-dlp
        self.channel_id = "UCh7uyJchI-WGkTm1o78Xvkg"
        self.videos = []
        self.current_page = 0
        self.videos_per_page = 6
        self.is_loading = False
        self.liked_videos = set()  # Track liked videos
        self.video_comments = {}  # Store comments for each video
        self.video_reviews = {}  # Store reviews for each video
        
        # Configure style
        self.setup_styles()
        
        # Setup UI
        self.setup_ui()
        
        # Load videos on startup
        self.load_videos_thread()
    
    def setup_styles(self):
        """Configure the application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background="#0f0f1c")
        style.configure('TLabel', background="#FFFFFF", foreground='#333')
        style.configure('Header.TLabel', background="#7c3005", foreground='white', font=('Helvetica', 14, 'bold'))
        style.configure('TButton', font=('Helvetica', 10))
        style.map('TButton', background=[('active', '#0066cc')])
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_container)
        
        # Content area with scrollbar
        self.create_content_area(main_container)
        
        # Footer with pagination
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="YouTube Channel Videos", font=('Helvetica', 16, 'bold'))
        title_label.pack(anchor=tk.W, pady=5)
        
        subtitle_label = ttk.Label(header_frame, text="Dinesh Bohara's Channel - All Videos", font=('Helvetica', 10))
        subtitle_label.pack(anchor=tk.W)
        
        # Status label
        self.status_label = ttk.Label(header_frame, text="Loading videos...", foreground='#0066cc')
        self.status_label.pack(anchor=tk.W, pady=5)
    
    def create_content_area(self, parent):
        """Create the main content area with video thumbnails"""
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', yscrollcommand=scrollbar.set, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Frame inside canvas (use tk.Frame instead of ttk.Frame for background support)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind canvas resize to update scroll region
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        
        # Bind mousewheel
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
        
        # Refresh button
        refresh_btn = ttk.Button(button_frame, text="Refresh", command=self.load_videos_thread)
        refresh_btn.pack(side=tk.LEFT, padx=20)
    
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
                self.status_label.config(text="Could not load videos. Check internet connection or API key.")
                messagebox.showwarning("Warning", "Could not load videos from the channel. Please check your internet connection.")
            else:
                self.status_label.config(text=f"Loaded {len(self.videos)} videos from channel")
            
            self.display_current_page()
            
        except Exception as e:
            print(f"Error loading videos: {e}")
            self.status_label.config(text=f"Error: {str(e)}")
        finally:
            self.is_loading = False
    
    def fetch_channel_videos(self):
        """
        Fetch the specific video
        """
        # Use the specific video provided
        video_id = 'CpqQFCIQURY'
        video = {
            'id': video_id,
            'title': 'Featured Video',
            'thumbnail': self.get_youtube_thumbnail_url(video_id, 'high'),
            'duration': 0,
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'upload_date': 'Recent',
            'view_count': 0,
            'likes': 0,
            'comments': 0,
            'reviews': 0,
        }
        return [video]
    

    

    

    
    def get_youtube_thumbnail_url(self, video_id, quality='medium'):
        """
        Generate YouTube thumbnail URL from video ID
        quality options: 'default' (120x90), 'medium' (320x180), 'high' (480x360), 'standard' (640x480), 'maxres' (1280x720)
        Returns URL with fallback quality if primary isn't available
        """
        quality_map = {
            'default': f'https://i.ytimg.com/vi/{video_id}/default.jpg',
            'medium': f'https://i.ytimg.com/vi/{video_id}/mqdefault.jpg',
            'high': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
            'standard': f'https://i.ytimg.com/vi/{video_id}/sddefault.jpg',
            'maxres': f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg',
        }
        return quality_map.get(quality, quality_map['medium'])
    

    

    

    
    def display_current_page(self):
        """Display videos for the current page"""
        # Clear the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.videos:
            no_videos_label = ttk.Label(self.scrollable_frame, text="No videos found", font=('Helvetica', 12))
            no_videos_label.pack(pady=50)
            return
        
        # Calculate pagination
        start_idx = self.current_page * self.videos_per_page
        end_idx = start_idx + self.videos_per_page
        page_videos = self.videos[start_idx:end_idx]
        
        # Update page label
        total_pages = (len(self.videos) + self.videos_per_page - 1) // self.videos_per_page
        self.page_label.config(text=f"Page {self.current_page + 1} of {total_pages}")
        
        # Update button states
        self.prev_btn.config(state=tk.DISABLED if self.current_page == 0 else tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED if end_idx >= len(self.videos) else tk.NORMAL)
        
        # Display videos in a grid (use tk.Frame for background support)
        videos_frame = tk.Frame(self.scrollable_frame, bg='white')
        videos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for idx, video in enumerate(page_videos):
            col = idx % 3
            row = idx // 3
            self.create_video_card(videos_frame, video, row, col)
    
    def create_video_card(self, parent, video, row, col):
        """Create a video card widget with likes, comments, and reviews"""
        card_frame = tk.Frame(parent, relief=tk.RAISED, borderwidth=2, bg='white')
        card_frame.grid(row=row, column=col, padx=8, pady=8, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Hover effect
        def on_enter(e):
            card_frame.config(relief=tk.SUNKEN, bg='#f0f0f0')
        
        def on_leave(e):
            card_frame.config(relief=tk.RAISED, bg='white')
        
        card_frame.bind('<Enter>', on_enter)
        card_frame.bind('<Leave>', on_leave)
        
        try:
            # Download and display thumbnail
            response = requests.get(video['thumbnail'], timeout=5)
            img = Image.open(BytesIO(response.content))
            img = img.resize((320, 180), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Thumbnail with play button
            thumb_frame = tk.Frame(card_frame, bg='black', height=180)
            thumb_frame.pack(fill=tk.X)
            
            thumb_label = tk.Label(thumb_frame, image=photo, cursor="hand2")
            thumb_label.image = photo
            thumb_label.pack()
            
            # Play button overlay
            play_btn = tk.Button(thumb_frame, text="▶ PLAY", font=('Helvetica', 12, 'bold'), 
                               bg='#ff0000', fg='white', padx=15, pady=5,
                               command=lambda: self.open_video_on_youtube(video),
                               cursor="hand2", activebackground='#cc0000')
            play_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            thumb_label.bind('<Button-1>', lambda e: self.open_video_on_youtube(video))
        
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            placeholder = tk.Label(card_frame, text="[No Image]", bg='#cccccc', width=40, height=10)
            placeholder.pack()
        
        # Title
        title_label = tk.Label(card_frame, text=video['title'], wraplength=310, justify=tk.LEFT, 
                              font=('Helvetica', 10, 'bold'), bg='white', fg='#000000', padx=8, pady=8)
        title_label.pack(fill=tk.X)
        
        # Details frame
        details_frame = tk.Frame(card_frame, bg='white')
        details_frame.pack(padx=8, pady=3, fill=tk.X)
        
        # Format upload date
        upload_date = video.get('upload_date', 'Unknown')
        if upload_date != 'Unknown' and len(upload_date) == 8:
            try:
                dt = datetime.strptime(upload_date, '%Y%m%d')
                upload_date = dt.strftime('%d %b %Y')
            except:
                pass
        
        # Views and date
        view_count = video.get('view_count', 0)
        if view_count > 0:
            views_text = f"{view_count:,} views"
        else:
            views_text = "Recent"
        
        details_label = tk.Label(details_frame, text=f"{views_text} • {upload_date}", font=('Helvetica', 8), 
                               bg='white', fg='#666666')
        details_label.pack(fill=tk.X)
        
        # Engagement stats section (likes, comments, reviews)
        engagement_frame = tk.Frame(card_frame, bg='#f9f9f9', height=70)
        engagement_frame.pack(fill=tk.X, padx=0, pady=5)
        
        # Get engagement stats
        video_id = video.get('id')
        likes = len([vid for vid in self.liked_videos if vid == video_id])
        comments = video.get('comments', 0)
        reviews = video.get('reviews', 0)
        
        # Engagement row 1: Likes and Comments
        engagement_row1 = tk.Frame(engagement_frame, bg='#f9f9f9')
        engagement_row1.pack(fill=tk.X, padx=5, pady=3)
        
        like_btn = tk.Button(engagement_row1, text=f"👍 Like", bg='#e3f2fd', fg='#1976d2', 
                            font=('Helvetica', 9), relief=tk.FLAT, cursor="hand2", padx=8, pady=4,
                            command=lambda: self.like_video(video, card_frame))
        like_btn.pack(side=tk.LEFT, padx=3)
        
        comment_btn = tk.Button(engagement_row1, text=f"💬 Comments ({len(self.video_comments.get(video_id, []))})", bg='#f3e5f5', fg='#7b1fa2', 
                               font=('Helvetica', 9), relief=tk.FLAT, cursor="hand2", padx=8, pady=4,
                               command=lambda: self.show_comments_window(video))
        comment_btn.pack(side=tk.LEFT, padx=3)
        
        # Engagement row 2: Reviews and Rating
        engagement_row2 = tk.Frame(engagement_frame, bg='#f9f9f9')
        engagement_row2.pack(fill=tk.X, padx=5, pady=3)
        
        review_btn = tk.Button(engagement_row2, text=f"⭐ Reviews ({len(self.video_reviews.get(video_id, []))})", bg='#fff3e0', fg='#f57c00', 
                              font=('Helvetica', 9), relief=tk.FLAT, cursor="hand2", padx=8, pady=4,
                              command=lambda: self.show_reviews_window(video))
        review_btn.pack(side=tk.LEFT, padx=3)
        
        share_btn = tk.Button(engagement_row2, text="🔗 Share", bg='#e8f5e9', fg='#388e3c', 
                             font=('Helvetica', 9), relief=tk.FLAT, cursor="hand2", padx=8, pady=4,
                             command=lambda: self.copy_link_to_clipboard(video))
        share_btn.pack(side=tk.LEFT, padx=3)
        
        # Divider
        divider = tk.Frame(card_frame, bg='#e0e0e0', height=1)
        divider.pack(fill=tk.X, padx=5, pady=3)
    
    def open_video(self, video):
        """Open the video on YouTube"""
        self.open_video_on_youtube(video)
    
    def open_video_on_youtube(self, video):
        """Open the exact video on YouTube"""
        video_id = video.get('id')
        if video_id and video_id != 'sample1' and video_id != 'sample2':
            url = f"https://www.youtube.com/watch?v={video_id}"
        else:
            url = video.get('url')
        
        if url:
            webbrowser.open(url)
            messagebox.showinfo("Opening Video", f"Opening video in YouTube...\n\n{video.get('title', 'Video')}")
        else:
            messagebox.showerror("Error", "Could not get video URL")
    
    def copy_link_to_clipboard(self, video):
        """Copy video link to clipboard"""
        video_id = video.get('id')
        if video_id:
            url = f"https://www.youtube.com/watch?v={video_id}"
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            messagebox.showinfo("Copied", f"Video link copied to clipboard!\n\n{url}")
    
    def like_video(self, video, card_frame):
        """Like/Unlike a video"""
        video_id = video.get('id')
        if video_id in self.liked_videos:
            self.liked_videos.remove(video_id)
            messagebox.showinfo("Like Removed", "You unliked this video!")
        else:
            self.liked_videos.add(video_id)
            messagebox.showinfo("Liked", "You liked this video! 👍")
        
        # Refresh the display
        self.display_current_page()
    
    def show_comments_window(self, video):
        """Show comments window for a video"""
        video_id = video.get('id')
        video_title = video.get('title', 'Video')
        
        # Create new window
        comments_window = tk.Toplevel(self.root)
        comments_window.title(f"Comments - {video_title[:50]}")
        comments_window.geometry("600x500")
        comments_window.resizable(True, True)
        
        # Header
        header = tk.Label(comments_window, text=f"💬 Comments for: {video_title[:60]}", 
                         font=('Helvetica', 12, 'bold'), bg='#f3e5f5', fg='#7b1fa2', padx=10, pady=10)
        header.pack(fill=tk.X)
        
        # Comments display area
        comments_frame = tk.Frame(comments_window)
        comments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(comments_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        comments_text = tk.Text(comments_frame, font=('Helvetica', 10), yscrollcommand=scrollbar.set,
                               wrap=tk.WORD, bg='#ffffff', fg='#333333')
        comments_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=comments_text.yview)
        comments_text.config(state=tk.DISABLED)
        
        # Display existing comments
        if video_id in self.video_comments:
            comments_text.config(state=tk.NORMAL)
            for comment in self.video_comments[video_id]:
                comments_text.insert(tk.END, f"👤 {comment['user']}\n{comment['text']}\n" + "-"*60 + "\n\n")
            comments_text.config(state=tk.DISABLED)
        else:
            comments_text.config(state=tk.NORMAL)
            comments_text.insert(tk.END, "No comments yet. Be the first to comment!")
            comments_text.config(state=tk.DISABLED)
        
        # Comment input area
        input_frame = tk.Frame(comments_window, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User name input
        name_label = tk.Label(input_frame, text="Name:", font=('Helvetica', 10), bg='#f0f0f0')
        name_label.pack(anchor=tk.W, pady=(0, 5))
        name_entry = tk.Entry(input_frame, font=('Helvetica', 10), width=50)
        name_entry.pack(anchor=tk.W, fill=tk.X)
        
        # Comment text input
        comment_label = tk.Label(input_frame, text="Your Comment:", font=('Helvetica', 10), bg='#f0f0f0')
        comment_label.pack(anchor=tk.W, pady=(10, 5))
        comment_text = tk.Text(input_frame, font=('Helvetica', 10), height=4, wrap=tk.WORD, bg='#ffffff')
        comment_text.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # Post button
        def post_comment():
            user_name = name_entry.get().strip()
            comment_content = comment_text.get("1.0", tk.END).strip()
            
            if not user_name or not comment_content:
                messagebox.showwarning("Empty Fields", "Please enter both name and comment!")
                return
            
            # Add comment to storage
            if video_id not in self.video_comments:
                self.video_comments[video_id] = []
            
            self.video_comments[video_id].append({
                'user': user_name,
                'text': comment_content,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            
            # Clear inputs
            name_entry.delete(0, tk.END)
            comment_text.delete("1.0", tk.END)
            
            # Update display
            comments_text.config(state=tk.NORMAL)
            comments_text.delete("1.0", tk.END)
            for comment in self.video_comments[video_id]:
                comments_text.insert(tk.END, f"👤 {comment['user']}\n{comment['text']}\n" + "-"*60 + "\n\n")
            comments_text.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", "Comment posted successfully!")
            
            # Refresh main window
            self.display_current_page()
        
        post_btn = tk.Button(input_frame, text="📤 Post Comment", bg='#7b1fa2', fg='white',
                            font=('Helvetica', 10, 'bold'), cursor="hand2", command=post_comment)
        post_btn.pack(pady=10, fill=tk.X)
    
    def show_reviews_window(self, video):
        """Show reviews window for a video"""
        video_id = video.get('id')
        video_title = video.get('title', 'Video')
        
        # Create new window
        reviews_window = tk.Toplevel(self.root)
        reviews_window.title(f"Reviews - {video_title[:50]}")
        reviews_window.geometry("600x500")
        reviews_window.resizable(True, True)
        
        # Header
        header = tk.Label(reviews_window, text=f"⭐ Reviews for: {video_title[:60]}", 
                         font=('Helvetica', 12, 'bold'), bg='#fff3e0', fg='#f57c00', padx=10, pady=10)
        header.pack(fill=tk.X)
        
        # Reviews display area
        reviews_frame = tk.Frame(reviews_window)
        reviews_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(reviews_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        reviews_text = tk.Text(reviews_frame, font=('Helvetica', 10), yscrollcommand=scrollbar.set,
                              wrap=tk.WORD, bg='#ffffff', fg='#333333')
        reviews_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=reviews_text.yview)
        reviews_text.config(state=tk.DISABLED)
        
        # Display existing reviews
        if video_id in self.video_reviews:
            reviews_text.config(state=tk.NORMAL)
            for review in self.video_reviews[video_id]:
                rating_stars = "⭐" * review['rating']
                reviews_text.insert(tk.END, f"👤 {review['user']} - {rating_stars} ({review['rating']}/5)\n{review['text']}\n" + "-"*60 + "\n\n")
            reviews_text.config(state=tk.DISABLED)
        else:
            reviews_text.config(state=tk.NORMAL)
            reviews_text.insert(tk.END, "No reviews yet. Be the first to review!")
            reviews_text.config(state=tk.DISABLED)
        
        # Review input area
        input_frame = tk.Frame(reviews_window, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User name input
        name_label = tk.Label(input_frame, text="Name:", font=('Helvetica', 10), bg='#f0f0f0')
        name_label.pack(anchor=tk.W, pady=(0, 5))
        name_entry = tk.Entry(input_frame, font=('Helvetica', 10), width=50)
        name_entry.pack(anchor=tk.W, fill=tk.X)
        
        # Rating input
        rating_label = tk.Label(input_frame, text="Rating (1-5 stars):", font=('Helvetica', 10), bg='#f0f0f0')
        rating_label.pack(anchor=tk.W, pady=(10, 5))
        rating_frame = tk.Frame(input_frame, bg='#f0f0f0')
        rating_frame.pack(anchor=tk.W, fill=tk.X)
        
        rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            rb = tk.Radiobutton(rating_frame, text=f"{i} ⭐", variable=rating_var, value=i,
                              font=('Helvetica', 10), bg='#f0f0f0')
            rb.pack(side=tk.LEFT, padx=5)
        
        # Review text input
        review_label = tk.Label(input_frame, text="Your Review:", font=('Helvetica', 10), bg='#f0f0f0')
        review_label.pack(anchor=tk.W, pady=(10, 5))
        review_text = tk.Text(input_frame, font=('Helvetica', 10), height=4, wrap=tk.WORD, bg='#ffffff')
        review_text.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        # Post button
        def post_review():
            user_name = name_entry.get().strip()
            review_content = review_text.get("1.0", tk.END).strip()
            rating = rating_var.get()
            
            if not user_name or not review_content:
                messagebox.showwarning("Empty Fields", "Please enter both name and review!")
                return
            
            # Add review to storage
            if video_id not in self.video_reviews:
                self.video_reviews[video_id] = []
            
            self.video_reviews[video_id].append({
                'user': user_name,
                'text': review_content,
                'rating': rating,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            
            # Clear inputs
            name_entry.delete(0, tk.END)
            review_text.delete("1.0", tk.END)
            
            # Update display
            reviews_text.config(state=tk.NORMAL)
            reviews_text.delete("1.0", tk.END)
            for review in self.video_reviews[video_id]:
                rating_stars = "⭐" * review['rating']
                reviews_text.insert(tk.END, f"👤 {review['user']} - {rating_stars} ({review['rating']}/5)\n{review['text']}\n" + "-"*60 + "\n\n")
            reviews_text.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", "Review posted successfully!")
            
            # Refresh main window
            self.display_current_page()
        
        post_btn = tk.Button(input_frame, text="📤 Post Review", bg='#f57c00', fg='white',
                            font=('Helvetica', 10, 'bold'), cursor="hand2", command=post_review)
        post_btn.pack(pady=10, fill=tk.X)
    
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
    app = YouTubeChannelViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()


