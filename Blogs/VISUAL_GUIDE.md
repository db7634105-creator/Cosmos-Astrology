# 🎬 YouTube Viewer - Visual Guide

## 🖥️ Application Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ YouTube Channel Video Viewer                                    │
├─────────────────────────────────────────────────────────────────┤
│ YouTube Channel Videos                                          │
│ Dinesh Bohara's Channel - All Videos                           │
│ Loading videos from channel...                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   VIDEO 1    │  │   VIDEO 2    │  │   VIDEO 3    │         │
│  │ [Thumbnail]  │  │ [Thumbnail]  │  │ [Thumbnail]  │         │
│  │  ▶ PLAY      │  │  ▶ PLAY      │  │  ▶ PLAY      │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ Video Title  │  │ Video Title  │  │ Video Title  │         │
│  │ Views • Date │  │ Views • Date │  │ Views • Date │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ 👍Like       │  │ 👍Like       │  │ 👍Like       │         │
│  │ 💬 Comments  │  │ 💬 Comments  │  │ 💬 Comments  │         │
│  │ ⭐Reviews    │  │ ⭐Reviews    │  │ ⭐Reviews    │         │
│  │ 🔗Share      │  │ 🔗Share      │  │ 🔗Share      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   VIDEO 4    │  │   VIDEO 5    │  │   VIDEO 6    │         │
│  │ [Thumbnail]  │  │ [Thumbnail]  │  │ [Thumbnail]  │         │
│  │  ▶ PLAY      │  │  ▶ PLAY      │  │  ▶ PLAY      │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ Video Title  │  │ Video Title  │  │ Video Title  │         │
│  │ Views • Date │  │ Views • Date │  │ Views • Date │         │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│  │ 👍Like       │  │ 👍Like       │  │ 👍Like       │         │
│  │ 💬 Comments  │  │ 💬 Comments  │  │ 💬 Comments  │         │
│  │ ⭐Reviews    │  │ ⭐Reviews    │  │ ⭐Reviews    │         │
│  │ 🔗Share      │  │ 🔗Share      │  │ 🔗Share      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ ← Previous    Page 1 of 5              Next →   [Refresh]     │
└─────────────────────────────────────────────────────────────────┘
```

## 💬 Comments Window

```
┌─────────────────────────────────────────┐
│ Comments - Video Title                  │
├─────────────────────────────────────────┤
│ 💬 Comments for: Video Title...         │
├─────────────────────────────────────────┤
│                                         │
│ 👤 John Smith                           │
│ This is an amazing video! I loved it.   │
│ ──────────────────────────────────────  │
│                                         │
│ 👤 Sarah Johnson                        │
│ Great explanation, thanks for sharing! │
│ ──────────────────────────────────────  │
│                                         │
│ [Scrollable Area]                       │
│                                         │
├─────────────────────────────────────────┤
│ Name:                                   │
│ [_____________________________]          │
│                                         │
│ Your Comment:                           │
│ [_____________________________]          │
│ [_____________________________]          │
│ [_____________________________]          │
│ [_____________________________]          │
│                                         │
│ [📤 Post Comment]                       │
└─────────────────────────────────────────┘
```

## ⭐ Reviews Window

```
┌─────────────────────────────────────────┐
│ Reviews - Video Title                   │
├─────────────────────────────────────────┤
│ ⭐ Reviews for: Video Title...          │
├─────────────────────────────────────────┤
│                                         │
│ 👤 Alice Cooper - ⭐⭐⭐⭐⭐ (5/5)      │
│ Excellent tutorial! Must watch.         │
│ ──────────────────────────────────────  │
│                                         │
│ 👤 Bob Wilson - ⭐⭐⭐⭐ (4/4)         │
│ Good content but needs more examples.   │
│ ──────────────────────────────────────  │
│                                         │
│ [Scrollable Area]                       │
│                                         │
├─────────────────────────────────────────┤
│ Name:                                   │
│ [_____________________________]          │
│                                         │
│ Rating (1-5 stars):                     │
│ ○1⭐  ○2⭐  ○3⭐  ○4⭐  ●5⭐           │
│                                         │
│ Your Review:                            │
│ [_____________________________]          │
│ [_____________________________]          │
│ [_____________________________]          │
│ [_____________________________]          │
│                                         │
│ [📤 Post Review]                        │
└─────────────────────────────────────────┘
```

## 🎯 User Interaction Flow

### Flow 1: Liking a Video
```
Start
  ↓
User sees video card
  ↓
Click "👍 Like" button
  ↓
System checks if video already liked
  ├─ If liked: Remove from set → "You unliked this video!"
  └─ If not liked: Add to set → "You liked this video! 👍"
  ↓
Refresh video display
  ↓
Like button status updates
  ↓
End
```

### Flow 2: Adding a Comment
```
Start
  ↓
User clicks "💬 Comments (X)" button
  ↓
Comments window opens
  ↓
User enters name
  ↓
User types comment
  ↓
User clicks "📤 Post Comment"
  ↓
System validates inputs
  ├─ Invalid: Show error, ask to retry
  └─ Valid: Add to comments storage
  ↓
Update comments display
  ↓
Show success message
  ↓
Refresh main window
  ↓
Comment count updates on main video card
  ↓
End
```

### Flow 3: Adding a Review
```
Start
  ↓
User clicks "⭐ Reviews (X)" button
  ↓
Reviews window opens
  ↓
User enters name
  ↓
User selects star rating (1-5)
  ↓
User types review text
  ↓
User clicks "📤 Post Review"
  ↓
System validates inputs
  ├─ Invalid: Show error
  └─ Valid: Add to reviews storage with rating
  ↓
Update reviews display (with stars)
  ↓
Show success message
  ↓
Refresh main window
  ↓
Review count updates
  ↓
End
```

### Flow 4: Sharing a Video
```
Start
  ↓
User clicks "🔗 Share" button
  ↓
System gets video ID
  ↓
Construct YouTube URL
  ↓
Copy to clipboard
  ↓
Show confirmation: "Video link copied!"
  ↓
User can paste anywhere
  ↓
End
```

### Flow 5: Playing a Video
```
Start
  ↓
User clicks "▶ PLAY" button
  ↓
System gets video ID
  ↓
Construct YouTube URL
  ↓
Open in default browser
  ↓
Show confirmation message
  ↓
Video loads on YouTube
  ↓
User can watch
  ↓
End
```

## 🎨 Color Scheme

### Button Colors:
```
Like Button:
Background: #e3f2fd (Light Blue)
Text: #1976d2 (Blue)
Hover: Darker blue

Comments Button:
Background: #f3e5f5 (Light Purple)
Text: #7b1fa2 (Purple)
Hover: Darker purple

Reviews Button:
Background: #fff3e0 (Light Orange)
Text: #f57c00 (Orange)
Hover: Darker orange

Share Button:
Background: #e8f5e9 (Light Green)
Text: #388e3c (Green)
Hover: Darker green

Play Button:
Background: #ff0000 (Red)
Text: White
Hover: #cc0000 (Dark Red)
```

### Window Headers:
```
Comments Window: Purple theme (#f3e5f5)
Reviews Window: Orange theme (#fff3e0)
Main Window: Light gray (#ffffff)
```

## 📊 Data Display Examples

### Video Card Display:
```
TITLE: "Astrology Basics - Understanding Your Zodiac Sign"
VIEWS: "2,100,000 views"
DATE: "02 Jan 2024"

BUTTONS:
👍 Like          💬 Comments (3)
⭐ Reviews (2)   🔗 Share
```

### Comment Display:
```
👤 John Smith
This video is incredibly helpful for beginners!
Really appreciate the clear explanation.

👤 Sarah Johnson
Thanks for breaking down complex concepts!
I'll definitely recommend this to my friends.

👤 Mike Johnson
Best astrology tutorial I've found. Well done!
```

### Review Display:
```
👤 Alice Cooper - ⭐⭐⭐⭐⭐ (5/5)
Excellent content! Crystal clear explanations.
Perfect for both beginners and experienced astrology enthusiasts.

👤 Bob Wilson - ⭐⭐⭐⭐ (4/5)
Good information but could use more visual aids.
Overall a solid educational video.
```

## 🔄 State Transitions

### Like State Machine:
```
     NOT_LIKED
        ↓  ↑
        │  │ Click Like again
        │  │
        ↓  ↑
      LIKED
```

### Comment Display State:
```
CLOSED WINDOW → User clicks Comments → OPEN WINDOW
                                           ↓
                                    Display comments
                                    Show input fields
                                    User posts comment
                                           ↓
                                    Comment added
                                    Count updates
```

### Review Display State:
```
CLOSED WINDOW → User clicks Reviews → OPEN WINDOW
                                           ↓
                                    Display reviews
                                    Show rating selector
                                    Show input fields
                                    User posts review
                                           ↓
                                    Review added
                                    Count updates
```

## 📱 Responsive Design

### Large Screen (1920x1080+):
```
Full 3-column grid
All details visible
Comfortable spacing
Easy navigation
```

### Medium Screen (1200x800):
```
Still 3-column grid
Good proportions
Readable text
All features accessible
```

### Small Screen (800x600):
```
Might adjust to 2 columns
Scrolling required
All features still available
Mobile-friendly
```

## ⌨️ Keyboard & Mouse Interactions

### Mouse Interactions:
- Click video thumbnail → (Currently shows play option)
- Click "▶ PLAY" button → Opens video on YouTube
- Click "👍 Like" → Likes/Unlikes video
- Click "💬 Comments" → Opens comments window
- Click "⭐ Reviews" → Opens reviews window
- Click "🔗 Share" → Copies link to clipboard
- Scroll wheel → Navigate through video list
- Click "Previous/Next" → Change pages
- Click "Refresh" → Reload videos

### Input Interactions:
- Type in Name field → Enter username
- Type in Comment/Review area → Enter content
- Select star rating → Choose 1-5 stars
- Click "📤 Post" → Submit content

## 🎬 Window Management

### Main Window:
- Title: "YouTube Channel Video Viewer"
- Size: 1200x700 (minimum 1000x600)
- Resizable: Yes
- Maximizable: Yes

### Comments Window:
- Title: "Comments - [Video Title]"
- Size: 600x500
- Resizable: Yes
- Modal: No (can interact with other windows)

### Reviews Window:
- Title: "Reviews - [Video Title]"
- Size: 600x500
- Resizable: Yes
- Modal: No

---

**Visual Guide Version**: 2.0  
**Last Updated**: December 2024
