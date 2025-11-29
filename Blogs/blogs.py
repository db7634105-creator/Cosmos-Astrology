import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pytube import YouTube
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("500x300")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=60)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.url_entry.insert(0, "https://youtube.com/shorts/ZiBwS_lIVlI?si=F-wzO9ZYSgmL-bmT")
        
        # Download path
        ttk.Label(main_frame, text="Download Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.path_entry = ttk.Entry(main_frame, width=50)
        self.path_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        self.path_entry.insert(0, os.path.join(os.getcwd(), "downloaded_videos"))
        
        ttk.Button(main_frame, text="Browse", command=self.browse_folder).grid(row=3, column=1, padx=5)
        
        # Download options
        self.download_type = tk.StringVar(value="video")
        ttk.Radiobutton(main_frame, text="Download Video", variable=self.download_type, value="video").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(main_frame, text="Download Audio Only", variable=self.download_type, value="audio").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to download")
        self.status_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
    
    def start_download(self):
        url = self.url_entry.get().strip()
        download_path = self.path_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_video, args=(url, download_path))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url, download_path):
        try:
            self.download_btn.config(state='disabled')
            self.progress.start()
            self.status_label.config(text="Connecting to YouTube...")
            
            yt = YouTube(url)
            
            self.status_label.config(text=f"Downloading: {yt.title}")
            
            if self.download_type.get() == "video":
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if not stream:
                    stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
            else:
                stream = yt.streams.filter(only_audio=True).first()
            
            if not stream:
                raise Exception("No suitable stream found")
            
            os.makedirs(download_path, exist_ok=True)
            output_file = stream.download(output_path=download_path)
            
            # If audio only, rename to .mp3
            if self.download_type.get() == "audio":
                base, ext = os.path.splitext(output_file)
                if ext != '.mp3':
                    new_file = base + '.mp3'
                    os.rename(output_file, new_file)
                    output_file = new_file
            
            self.status_label.config(text=f"Download completed: {os.path.basename(output_file)}")
            messagebox.showinfo("Success", f"Download completed!\nFile saved as: {output_file}")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")
        finally:
            self.progress.stop()
            self.download_btn.config(state='normal')

def run_gui_app():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

# Uncomment the following line to run the GUI version
# run_gui_app()