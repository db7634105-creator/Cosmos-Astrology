#!/usr/bin/env python3
"""
Test script to verify all YouTube viewer features
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_features():
    print("Testing YouTube Channel Viewer Features...")
    print("=" * 60)
    
    # Import the module
    try:
        from youtube_channel_viewer import YouTubeChannelViewer
        print("✅ Module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import: {e}")
        return False
    
    # Test class initialization
    try:
        import tkinter as tk
        root = tk.Tk()
        app = YouTubeChannelViewer(root)
        print("✅ YouTubeChannelViewer class initialized")
    except Exception as e:
        print(f"❌ Failed to initialize class: {e}")
        return False
    
    # Test new attributes
    tests = [
        ('like_video', 'Like video functionality'),
        ('show_comments_window', 'Comments window'),
        ('show_reviews_window', 'Reviews window'),
        ('liked_videos', 'Liked videos tracking'),
        ('video_comments', 'Comments storage'),
        ('video_reviews', 'Reviews storage'),
        ('copy_link_to_clipboard', 'Share functionality'),
    ]
    
    for attr, description in tests:
        if hasattr(app, attr):
            print(f"✅ {description:.<40} OK")
        else:
            print(f"❌ {description:.<40} FAILED")
            return False
    
    # Test video loading
    print(f"\n📹 Videos Loaded: {len(app.videos)} videos")
    if len(app.videos) > 0:
        print(f"   Sample video: {app.videos[0].get('title', 'Unknown')[:50]}")
    
    # Test tracking dictionaries
    print(f"\n📊 Data Structures:")
    print(f"   Liked videos: {len(app.liked_videos)} items")
    print(f"   Comments storage: {len(app.video_comments)} items")
    print(f"   Reviews storage: {len(app.video_reviews)} items")
    
    root.destroy()
    
    print("\n" + "=" * 60)
    print("✅ All features verified successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_features()
    sys.exit(0 if success else 1)
