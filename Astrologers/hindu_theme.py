"""
Hindu Religious Color Theme for Astrologers App
Inspired by Indian Flag colors and Hindu traditions
"""

class HinduTheme:
    """Color theme based on Hindu religious traditions"""
    
    # Primary Colors - Indian Flag Colors
    SAFFRON = "#FF9933"           # Orange/Saffron - Courage & Sacrifice
    WHITE = "#FFFFFF"             # White - Peace & Purity
    GREEN = "#138808"             # Green - Faith & Prosperity
    NAVY = "#000080"              # Dark Blue - Calm & Trust
    
    # Secondary Colors - Hindu Symbolism
    GOLD = "#D4AF37"              # Gold - Prosperity & Divinity
    MAROON = "#800000"            # Maroon - Sacred Power
    CRIMSON = "#DC143C"           # Crimson - Devotion
    LIGHT_ORANGE = "#FFE5CC"      # Light Saffron - Soft background
    LIGHT_GOLD = "#FFF8DC"        # Light Gold - Premium background
    
    # Functional Colors
    SUCCESS = "#27AE60"           # Green - Success (Hindu tradition)
    ERROR = "#E74C3C"             # Red - Error/Alert
    WARNING = "#F39C12"           # Orange - Warning
    INFO = "#3498DB"              # Blue - Information
    
    # Text Colors
    TEXT_PRIMARY = "#1A1A1A"      # Almost black - Main text
    TEXT_SECONDARY = "#555555"    # Gray - Secondary text
    TEXT_LIGHT = "#FFFFFF"        # White - On dark backgrounds
    TEXT_ON_SAFFRON = "#1A1A1A"   # Dark text on saffron
    TEXT_ON_GREEN = "#FFFFFF"     # White text on green
    
    # Background Colors
    BG_PRIMARY = "#F5F5F5"        # Very light gray - Main background
    BG_SECONDARY = "#FFFAF0"     # Floral white - Secondary backgrounds
    BG_DARK = "#2C3E50"           # Dark blue-gray - Dark sections
    BG_CARD = "#FFFFFF"           # White - Card backgrounds
    
    # Border Colors
    BORDER_LIGHT = "#E0E0E0"      # Light gray - Subtle borders
    BORDER_MEDIUM = "#D0D0D0"     # Medium gray - Standard borders
    BORDER_DARK = "#999999"       # Dark gray - Strong borders
    
    # Accent Colors
    ACCENT_1 = "#FF9933"          # Saffron - Primary accent
    ACCENT_2 = "#FFD700"          # Gold - Secondary accent
    ACCENT_3 = "#DC143C"          # Crimson - Tertiary accent
    
    # Hover/Active States
    HOVER_SAFFRON = "#FF7F00"     # Darker saffron on hover
    HOVER_GREEN = "#0D5206"       # Darker green on hover
    ACTIVE_GOLD = "#B8860B"       # Dark goldenrod - Active state
    
    # Light Variants for main.py compatibility
    GREEN_LIGHT = "#2ECC71"       # Light green for hover
    NAVY_LIGHT = "#34495E"        # Light navy for hover
    CRIMSON_LIGHT = "#E74C3C"     # Light crimson for hover
    
    # Special Effects
    SHADOW = "#00000020"          # Black with transparency
    HIGHLIGHT = "#FFFFFF80"       # White with transparency


class HinduThemeGuide:
    """Guide for applying colors in the application"""
    
    # Color Combinations
    COMBINATIONS = {
        "primary": {
            "bg": HinduTheme.LIGHT_ORANGE,
            "fg": HinduTheme.SAFFRON,
            "text": HinduTheme.TEXT_PRIMARY
        },
        "secondary": {
            "bg": HinduTheme.LIGHT_GOLD,
            "fg": HinduTheme.GOLD,
            "text": HinduTheme.TEXT_PRIMARY
        },
        "success": {
            "bg": HinduTheme.GREEN,
            "fg": HinduTheme.WHITE,
            "text": HinduTheme.TEXT_ON_GREEN
        },
        "card": {
            "bg": HinduTheme.BG_CARD,
            "border": HinduTheme.BORDER_LIGHT,
            "text": HinduTheme.TEXT_PRIMARY
        },
        "header": {
            "bg": HinduTheme.SAFFRON,
            "fg": HinduTheme.WHITE,
            "text": HinduTheme.TEXT_LIGHT
        },
        "footer": {
            "bg": HinduTheme.GREEN,
            "fg": HinduTheme.GOLD,
            "text": HinduTheme.TEXT_ON_GREEN
        }
    }
    
    # Symbol Decorations
    SYMBOLS = {
        "om": "ॐ",
        "star": "⭐",
        "moon": "🌙",
        "sun": "☀️",
        "lotus": "🪷",
        "prayer": "🙏",
        "temple": "🏛️",
        "chakra": "☸️",
        "dharma": "☸️",
        "peace": "☮️",
        "flame": "🔥",
        "water": "💧",
    }
    
    # Apply Colors
    @staticmethod
    def get_button_style(button_type="primary"):
        """Get button styling based on type"""
        styles = {
            "primary": {
                "bg": HinduTheme.SAFFRON,
                "fg": HinduTheme.TEXT_LIGHT,
                "activebackground": HinduTheme.HOVER_SAFFRON,
                "activeforeground": HinduTheme.TEXT_LIGHT,
                "relief": "raised",
                "bd": 2
            },
            "secondary": {
                "bg": HinduTheme.GOLD,
                "fg": HinduTheme.TEXT_PRIMARY,
                "activebackground": HinduTheme.ACTIVE_GOLD,
                "activeforeground": HinduTheme.TEXT_LIGHT,
                "relief": "raised",
                "bd": 2
            },
            "success": {
                "bg": HinduTheme.GREEN,
                "fg": HinduTheme.TEXT_ON_GREEN,
                "activebackground": HinduTheme.HOVER_GREEN,
                "activeforeground": HinduTheme.TEXT_LIGHT,
                "relief": "raised",
                "bd": 2
            },
            "danger": {
                "bg": HinduTheme.ERROR,
                "fg": HinduTheme.TEXT_LIGHT,
                "activebackground": "#C0392B",
                "activeforeground": HinduTheme.TEXT_LIGHT,
                "relief": "raised",
                "bd": 2
            },
            "neutral": {
                "bg": HinduTheme.NAVY,
                "fg": HinduTheme.TEXT_LIGHT,
                "activebackground": "#000050",
                "activeforeground": HinduTheme.TEXT_LIGHT,
                "relief": "raised",
                "bd": 2
            }
        }
        return styles.get(button_type, styles["primary"])
    
    @staticmethod
    def get_label_style(label_type="primary"):
        """Get label styling based on type"""
        styles = {
            "title": {
                "bg": HinduTheme.BG_PRIMARY,
                "fg": HinduTheme.SAFFRON,
                "font": ("Arial", 24, "bold")
            },
            "heading": {
                "bg": HinduTheme.BG_PRIMARY,
                "fg": HinduTheme.GREEN,
                "font": ("Arial", 14, "bold")
            },
            "subheading": {
                "bg": HinduTheme.BG_PRIMARY,
                "fg": HinduTheme.NAVY,
                "font": ("Arial", 12, "bold")
            },
            "normal": {
                "bg": HinduTheme.BG_PRIMARY,
                "fg": HinduTheme.TEXT_PRIMARY,
                "font": ("Arial", 10)
            },
            "info": {
                "bg": HinduTheme.LIGHT_GOLD,
                "fg": HinduTheme.MAROON,
                "font": ("Arial", 10)
            }
        }
        return styles.get(label_type, styles["normal"])
    
    @staticmethod
    def get_frame_style(frame_type="card"):
        """Get frame styling based on type"""
        styles = {
            "card": {
                "bg": HinduTheme.BG_CARD,
                "relief": "raised",
                "bd": 1,
                "highlightbackground": HinduTheme.BORDER_LIGHT,
                "highlightthickness": 1
            },
            "section": {
                "bg": HinduTheme.LIGHT_ORANGE,
                "relief": "flat",
                "bd": 0
            },
            "accent": {
                "bg": HinduTheme.LIGHT_GOLD,
                "relief": "flat",
                "bd": 0
            },
            "dark": {
                "bg": HinduTheme.BG_DARK,
                "relief": "flat",
                "bd": 0
            }
        }
        return styles.get(frame_type, styles["card"])


# Quick Reference for Developers
"""
HOW TO USE HINDU THEME:

1. Import the theme:
   from hindu_theme import HinduTheme, HinduThemeGuide

2. Use primary colors:
   header_frame.configure(bg=HinduTheme.SAFFRON)
   label.configure(fg=HinduTheme.WHITE)

3. Use predefined button styles:
   button = tk.Button(parent, text="Pay", **HinduThemeGuide.get_button_style("primary"))

4. Use predefined label styles:
   title = tk.Label(parent, text="Title", **HinduThemeGuide.get_label_style("title"))

5. Add religious symbols:
   om_label = tk.Label(parent, text=HinduThemeGuide.SYMBOLS["om"], font=("Arial", 20))

6. Use combinations:
   frame.configure(**HinduThemeGuide.COMBINATIONS["header"])

SYMBOL EXAMPLES:
   ॐ (OM)      - ☸️ (Dharma Wheel)   - 🙏 (Prayer Hands)
   🌙 (Moon)   - ☀️ (Sun)             - 🪷 (Lotus)
   ⭐ (Star)   - 🏛️ (Temple)         - 🔥 (Fire)

COLOR COMBINATIONS:
   - Saffron (ACCENT) + White (TEXT) = Patriotic
   - Gold (ACCENT) + Dark (BG) = Luxury
   - Green (PRIMARY) + Gold (ACCENT) = Traditional
   - Saffron + Green = Indian Flag
"""
