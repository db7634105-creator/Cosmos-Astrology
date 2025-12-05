"""
Astrology Compatibility Matcher for Boy & Girl
Implements Guna Milan (36 points system) based on Vedic Astrology
"""

from datetime import datetime
from typing import Dict, Tuple, List
import json


class AstrologyMatcher:
    """Main class for calculating astrological compatibility"""
    
    # Zodiac signs
    ZODIAC_SIGNS = {
        1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
        5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
        9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"
    }
    
    # Nadi (Nervous Temperament) - 8 points max
    NADIS = {
        "Vata": {"element": "Air", "nature": "Active, Creative"},
        "Pitta": {"element": "Fire", "nature": "Passionate, Intense"},
        "Kapha": {"element": "Earth/Water", "nature": "Calm, Stable"}
    }
    
    # Gana (Nature) - 6 points max
    GANAS = {
        "Deva": "Divine, Virtuous",
        "Manusha": "Human, Balanced",
        "Rakshasa": "Demon, Wild"
    }
    
    # Yoni (Sexual Compatibility) - 4 points max
    YONIS = {
        "Ashwa": {"animal": "Horse", "nature": "Strong, Active"},
        "Gaj": {"animal": "Elephant", "nature": "Calm, Wise"},
        "Mesha": {"animal": "Sheep", "nature": "Gentle, Timid"},
        "Sarpa": {"animal": "Snake", "nature": "Secretive, Passionate"},
        "Sinha": {"animal": "Lion", "nature": "Brave, Strong"},
        "Marjara": {"animal": "Cat", "nature": "Quick, Restless"},
        "Vrishabha": {"animal": "Bull", "nature": "Stable, Patient"},
        "Vrika": {"animal": "Dog", "nature": "Loyal, Protective"},
        "Simhika": {"animal": "Serpent", "nature": "Sharp, Intelligent"},
        "Kaka": {"animal": "Crow", "nature": "Quick, Alert"},
        "Khaga": {"animal": "Bird", "nature": "Free, Mobile"},
        "Mriga": {"animal": "Deer", "nature": "Gentle, Sensitive"},
        "Vanara": {"animal": "Monkey", "nature": "Playful, Social"},
        "Makar": {"animal": "Crocodile", "nature": "Mysterious, Deep"}
    }
    
    # Rajju (Family Line) - 8 points max
    RAJJUS = {
        "Parivartana": "Exchanged",
        "Parivartana": "Exchanged",
        "Adi": "Beginning",
        "Madhya": "Middle",
        "Anta": "End"
    }
    
    # Rashi (Zodiac Sign Compatibility) - 7 points max
    RASHI_COMPATIBILITY = {
        "Aries": ["Leo", "Sagittarius", "Libra"],
        "Taurus": ["Virgo", "Capricorn", "Pisces"],
        "Gemini": ["Libra", "Aquarius", "Aries"],
        "Cancer": ["Scorpio", "Pisces", "Taurus"],
        "Leo": ["Sagittarius", "Aries", "Gemini"],
        "Virgo": ["Capricorn", "Taurus", "Cancer"],
        "Libra": ["Aquarius", "Gemini", "Leo"],
        "Scorpio": ["Pisces", "Cancer", "Virgo"],
        "Sagittarius": ["Aries", "Leo", "Libra"],
        "Capricorn": ["Taurus", "Virgo", "Scorpio"],
        "Aquarius": ["Gemini", "Libra", "Sagittarius"],
        "Pisces": ["Cancer", "Scorpio", "Taurus"]
    }
    
    # Bhakut (Nature Compatibility) - 7 points max
    BHAKUT_COMPATIBILITY = {
        "Aries": ["Leo", "Sagittarius"],
        "Taurus": ["Virgo", "Capricorn"],
        "Gemini": ["Libra", "Aquarius"],
        "Cancer": ["Scorpio", "Pisces"],
        "Leo": ["Sagittarius", "Aries"],
        "Virgo": ["Capricorn", "Taurus"],
        "Libra": ["Aquarius", "Gemini"],
        "Scorpio": ["Pisces", "Cancer"],
        "Sagittarius": ["Aries", "Leo"],
        "Capricorn": ["Taurus", "Virgo"],
        "Aquarius": ["Gemini", "Libra"],
        "Pisces": ["Cancer", "Scorpio"]
    }
    
    def __init__(self):
        """Initialize the matcher"""
        self.boy_data = {}
        self.girl_data = {}
        self.match_results = {}
    
    def get_zodiac_sign(self, month: int, day: int) -> str:
        """Get zodiac sign from birth date"""
        dates = {
            (1, 20, 2, 18): "Aquarius",
            (2, 19, 3, 20): "Pisces",
            (3, 21, 4, 19): "Aries",
            (4, 20, 5, 20): "Taurus",
            (5, 21, 6, 20): "Gemini",
            (6, 21, 7, 22): "Cancer",
            (7, 23, 8, 22): "Leo",
            (8, 23, 9, 22): "Virgo",
            (9, 23, 10, 22): "Libra",
            (10, 23, 11, 21): "Scorpio",
            (11, 22, 12, 21): "Sagittarius",
            (12, 22, 1, 19): "Capricorn"
        }
        
        for (m1, d1, m2, d2), sign in dates.items():
            if (month == m1 and day >= d1) or (month == m2 and day <= d2):
                return sign
        return "Unknown"
    
    def calculate_nadi_guna(self, birth_time: str) -> str:
        """Calculate Nadi from birth time (simplified)"""
        hour = int(birth_time.split(":")[0])
        if hour < 8:
            return "Vata"
        elif hour < 16:
            return "Pitta"
        else:
            return "Kapha"
    
    def calculate_nadi_compatibility(self, boy_nadi: str, girl_nadi: str) -> int:
        """Calculate Nadi compatibility - 8 points max"""
        if boy_nadi == girl_nadi:
            return 0  # Same Nadi is incompatible
        elif boy_nadi != girl_nadi:
            return 8  # Different Nadi is highly compatible
        return 4
    
    def calculate_gana_compatibility(self, boy_gana: str, girl_gana: str) -> int:
        """Calculate Gana (Nature) compatibility - 6 points max"""
        if boy_gana == girl_gana:
            return 6  # Same Gana is perfect
        elif (boy_gana == "Deva" and girl_gana == "Manusha") or \
             (boy_gana == "Manusha" and girl_gana == "Deva"):
            return 6  # Deva-Manusha is good
        elif (boy_gana == "Manusha" and girl_gana == "Rakshasa") or \
             (boy_gana == "Rakshasa" and girl_gana == "Manusha"):
            return 0  # Manusha-Rakshasa is bad
        else:
            return 3  # Moderate compatibility
    
    def calculate_yoni_compatibility(self, boy_yoni: str, girl_yoni: str) -> int:
        """Calculate Yoni (Sexual) compatibility - 4 points max"""
        # Friendly Yonis
        friendly = {
            "Ashwa": ["Gaj", "Mesha"],
            "Gaj": ["Ashwa", "Sarpa"],
            "Mesha": ["Ashwa", "Vrishabha"],
            "Sarpa": ["Gaj", "Marjara"],
            "Sinha": ["Mesha", "Vrika"],
            "Marjara": ["Sarpa", "Simhika"],
            "Vrishabha": ["Mesha", "Vrika"],
            "Vrika": ["Sinha", "Vrishabha"],
            "Simhika": ["Marjara", "Kaka"],
            "Kaka": ["Simhika", "Khaga"],
            "Khaga": ["Kaka", "Mriga"],
            "Mriga": ["Khaga", "Vanara"],
            "Vanara": ["Mriga", "Makar"],
            "Makar": ["Vanara", "Ashwa"]
        }
        
        if boy_yoni == girl_yoni:
            return 4  # Same Yoni is excellent
        elif girl_yoni in friendly.get(boy_yoni, []):
            return 3  # Friendly Yoni
        else:
            return 1  # Unfriendly Yoni
    
    def calculate_rashi_compatibility(self, boy_rashi: str, girl_rashi: str) -> int:
        """Calculate Rashi (Zodiac) compatibility - 7 points max"""
        if boy_rashi == girl_rashi:
            return 7  # Same Rashi
        elif girl_rashi in self.RASHI_COMPATIBILITY.get(boy_rashi, []):
            return 7  # Very compatible signs
        elif self._is_trine(boy_rashi, girl_rashi):
            return 6  # Trine (120 degrees)
        elif self._is_sextile(boy_rashi, girl_rashi):
            return 5  # Sextile (60 degrees)
        elif self._is_opposition(boy_rashi, girl_rashi):
            return 2  # Opposition (180 degrees)
        else:
            return 3  # Other combinations
    
    def _is_trine(self, sign1: str, sign2: str) -> bool:
        """Check if signs are trine (120 degrees apart)"""
        sign_order = list(self.ZODIAC_SIGNS.values())
        idx1 = sign_order.index(sign1)
        idx2 = sign_order.index(sign2)
        diff = abs(idx1 - idx2)
        return diff == 4 or diff == 8
    
    def _is_sextile(self, sign1: str, sign2: str) -> bool:
        """Check if signs are sextile (60 degrees apart)"""
        sign_order = list(self.ZODIAC_SIGNS.values())
        idx1 = sign_order.index(sign1)
        idx2 = sign_order.index(sign2)
        diff = abs(idx1 - idx2)
        return diff == 2 or diff == 10
    
    def _is_opposition(self, sign1: str, sign2: str) -> bool:
        """Check if signs are in opposition (180 degrees apart)"""
        sign_order = list(self.ZODIAC_SIGNS.values())
        idx1 = sign_order.index(sign1)
        idx2 = sign_order.index(sign2)
        diff = abs(idx1 - idx2)
        return diff == 6
    
    def calculate_bhakut_compatibility(self, boy_rashi: str, girl_rashi: str) -> int:
        """Calculate Bhakut (Nature/Strength) compatibility - 7 points max"""
        if girl_rashi in self.BHAKUT_COMPATIBILITY.get(boy_rashi, []):
            return 7
        elif boy_rashi in self.BHAKUT_COMPATIBILITY.get(girl_rashi, []):
            return 6
        else:
            return 3
    
    def calculate_rajju_compatibility(self, boy_rajju: str, girl_rajju: str) -> int:
        """Calculate Rajju (Family Line) compatibility - 8 points max"""
        if boy_rajju == girl_rajju:
            return 0  # Same Rajju is problematic
        else:
            return 8  # Different Rajju is good
    
    def input_person_details(self, person_type: str = "Boy") -> Dict:
        """Input details for a person"""
        print(f"\n{'='*50}")
        print(f"Enter {person_type}'s Details")
        print(f"{'='*50}\n")
        
        data = {}
        data["name"] = input(f"Enter {person_type}'s name: ").strip()
        
        while True:
            try:
                birth_date = input(f"Enter {person_type}'s birth date (DD/MM/YYYY): ").strip()
                day, month, year = map(int, birth_date.split("/"))
                datetime(year, month, day)
                break
            except ValueError:
                print("Invalid date format. Please use DD/MM/YYYY")
        
        data["day"] = day
        data["month"] = month
        data["year"] = year
        data["zodiac_sign"] = self.get_zodiac_sign(month, day)
        
        while True:
            birth_time = input(f"Enter {person_type}'s birth time (HH:MM in 24-hour format): ").strip()
            try:
                hour, minute = map(int, birth_time.split(":"))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    data["birth_time"] = birth_time
                    break
                else:
                    print("Invalid time. Please use 24-hour format (00:00 - 23:59)")
            except ValueError:
                print("Invalid format. Please use HH:MM")
        
        print("\nSelect Gana (Nature):")
        for i, gana in enumerate(self.GANAS.keys(), 1):
            print(f"{i}. {gana} - {self.GANAS[gana]}")
        while True:
            try:
                gana_choice = int(input("Enter choice (1-3): "))
                if 1 <= gana_choice <= 3:
                    data["gana"] = list(self.GANAS.keys())[gana_choice - 1]
                    break
            except ValueError:
                pass
            print("Invalid choice. Please enter 1-3.")
        
        print("\nSelect Yoni (Sexual Nature):")
        yoni_list = list(self.YONIS.keys())
        for i, yoni in enumerate(yoni_list, 1):
            print(f"{i}. {yoni} - {self.YONIS[yoni]['animal']} ({self.YONIS[yoni]['nature']})")
        while True:
            try:
                yoni_choice = int(input(f"Enter choice (1-{len(yoni_list)}): "))
                if 1 <= yoni_choice <= len(yoni_list):
                    data["yoni"] = yoni_list[yoni_choice - 1]
                    break
            except ValueError:
                pass
            print(f"Invalid choice. Please enter 1-{len(yoni_list)}.")
        
        print("\nSelect Rajju (Family Line):")
        rajju_list = list(self.RAJJUS.keys())
        for i, rajju in enumerate(rajju_list, 1):
            print(f"{i}. {rajju} - {self.RAJJUS[rajju]}")
        while True:
            try:
                rajju_choice = int(input(f"Enter choice (1-{len(rajju_list)}): "))
                if 1 <= rajju_choice <= len(rajju_list):
                    data["rajju"] = rajju_list[rajju_choice - 1]
                    break
            except ValueError:
                pass
            print(f"Invalid choice. Please enter 1-{len(rajju_list)}.")
        
        # Calculate Nadi automatically
        data["nadi"] = self.calculate_nadi_guna(data["birth_time"])
        
        return data
    
    def calculate_compatibility(self, boy_data: Dict, girl_data: Dict) -> Dict:
        """Calculate overall compatibility between boy and girl"""
        results = {
            "boy_name": boy_data["name"],
            "girl_name": girl_data["name"],
            "details": {}
        }
        
        # 1. Nadi Compatibility (8 points)
        nadi_score = self.calculate_nadi_compatibility(boy_data["nadi"], girl_data["nadi"])
        results["details"]["nadi"] = {
            "score": nadi_score,
            "max": 8,
            "boy_nadi": boy_data["nadi"],
            "girl_nadi": girl_data["nadi"],
            "description": "Nervous Temperament Compatibility"
        }
        
        # 2. Gana Compatibility (6 points)
        gana_score = self.calculate_gana_compatibility(boy_data["gana"], girl_data["gana"])
        results["details"]["gana"] = {
            "score": gana_score,
            "max": 6,
            "boy_gana": boy_data["gana"],
            "girl_gana": girl_data["gana"],
            "description": "Nature/Character Compatibility"
        }
        
        # 3. Yoni Compatibility (4 points)
        yoni_score = self.calculate_yoni_compatibility(boy_data["yoni"], girl_data["yoni"])
        results["details"]["yoni"] = {
            "score": yoni_score,
            "max": 4,
            "boy_yoni": boy_data["yoni"],
            "girl_yoni": girl_data["yoni"],
            "description": "Sexual/Physical Compatibility"
        }
        
        # 4. Rashi Compatibility (7 points)
        rashi_score = self.calculate_rashi_compatibility(boy_data["zodiac_sign"], girl_data["zodiac_sign"])
        results["details"]["rashi"] = {
            "score": rashi_score,
            "max": 7,
            "boy_rashi": boy_data["zodiac_sign"],
            "girl_rashi": girl_data["zodiac_sign"],
            "description": "Zodiac Sign Compatibility"
        }
        
        # 5. Bhakut Compatibility (7 points)
        bhakut_score = self.calculate_bhakut_compatibility(boy_data["zodiac_sign"], girl_data["zodiac_sign"])
        results["details"]["bhakut"] = {
            "score": bhakut_score,
            "max": 7,
            "description": "Nature/Strength Compatibility"
        }
        
        # 6. Rajju Compatibility (8 points)
        rajju_score = self.calculate_rajju_compatibility(boy_data["rajju"], girl_data["rajju"])
        results["details"]["rajju"] = {
            "score": rajju_score,
            "max": 8,
            "boy_rajju": boy_data["rajju"],
            "girl_rajju": girl_data["rajju"],
            "description": "Family Line Compatibility"
        }
        
        # Calculate total
        total_score = sum(d["score"] for d in results["details"].values())
        results["total_score"] = total_score
        results["max_score"] = 36
        results["percentage"] = round((total_score / 36) * 100, 2)
        
        return results
    
    def get_compatibility_interpretation(self, score: int) -> Tuple[str, str]:
        """Get interpretation based on score"""
        if score >= 32:
            return "Excellent", "Outstanding compatibility - Highly recommended match"
        elif score >= 28:
            return "Very Good", "Strong compatibility - A very good match"
        elif score >= 24:
            return "Good", "Decent compatibility - Good match with some considerations"
        elif score >= 18:
            return "Average", "Moderate compatibility - Requires mutual understanding"
        elif score >= 12:
            return "Below Average", "Low compatibility - Significant challenges ahead"
        else:
            return "Poor", "Very poor compatibility - Not recommended match"
    
    def display_results(self, results: Dict):
        """Display compatibility results in a formatted way"""
        print(f"\n{'='*70}")
        print(f"{'COMPATIBILITY REPORT':^70}")
        print(f"{'='*70}\n")
        
        print(f"Boy: {results['boy_name']:<30} Girl: {results['girl_name']}")
        print(f"\n{'─'*70}")
        
        compatibility_type, interpretation = self.get_compatibility_interpretation(results["total_score"])
        
        print(f"\nOVERALL COMPATIBILITY: {results['total_score']}/36 ({results['percentage']}%)")
        print(f"Rating: {compatibility_type} - {interpretation}")
        
        print(f"\n{'─'*70}")
        print(f"{'DETAILED BREAKDOWN':^70}")
        print(f"{'─'*70}\n")
        
        details_order = ["nadi", "gana", "yoni", "rashi", "bhakut", "rajju"]
        
        for detail_key in details_order:
            detail = results["details"][detail_key]
            score = detail["score"]
            max_score = detail["max"]
            description = detail["description"]
            
            # Create a visual bar
            bar_length = 20
            filled = int((score / max_score) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"{description:.<35} {bar} {score}/{max_score}")
            
            # Print specific details
            if detail_key == "nadi":
                print(f"  → Boy's Nadi: {detail['boy_nadi']}, Girl's Nadi: {detail['girl_nadi']}")
            elif detail_key == "gana":
                print(f"  → Boy's Gana: {detail['boy_gana']}, Girl's Gana: {detail['girl_gana']}")
            elif detail_key == "yoni":
                print(f"  → Boy's Yoni: {detail['boy_yoni']}, Girl's Yoni: {detail['girl_yoni']}")
            elif detail_key == "rashi":
                print(f"  → Boy's Rashi: {detail['boy_rashi']}, Girl's Rashi: {detail['girl_rashi']}")
            elif detail_key == "rajju":
                print(f"  → Boy's Rajju: {detail['boy_rajju']}, Girl's Rajju: {detail['girl_rajju']}")
            
            print()
        
        print(f"{'─'*70}\n")
    
    def save_results(self, results: Dict, filename: str = "match_results.json"):
        """Save results to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {filename}")
    
    def run(self):
        """Run the complete matching program"""
        print("\n" + "="*70)
        print(f"{'VEDIC ASTROLOGY COMPATIBILITY MATCHER':^70}")
        print(f"{'Guna Milan (36 Point System)':^70}")
        print("="*70)
        
        # Input boy's details
        self.boy_data = self.input_person_details("Boy")
        
        # Input girl's details
        self.girl_data = self.input_person_details("Girl")
        
        # Calculate compatibility
        self.match_results = self.calculate_compatibility(self.boy_data, self.girl_data)
        
        # Display results
        self.display_results(self.match_results)
        
        # Ask to save results
        save = input("Would you like to save the results to a file? (yes/no): ").strip().lower()
        if save in ['yes', 'y']:
            filename = input("Enter filename (default: match_results.json): ").strip()
            if not filename:
                filename = "match_results.json"
            self.save_results(self.match_results, filename)
        
        # Ask for another match
        another = input("\nWould you like to check another match? (yes/no): ").strip().lower()
        if another in ['yes', 'y']:
            self.run()
        else:
            print("\nThank you for using Vedic Astrology Compatibility Matcher!")
            print("="*70)


import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os


class AstrologyMatcherGUI:
    """GUI Interface for Astrology Matcher"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Vedic Astrology Love Matcher ✨")
        self.root.geometry("1200x900")
        self.root.configure(bg="#001a4d")
        
        # Colors - Navy Blue & Orange Gradient theme
        self.bg_dark = "#001a4d"
        self.bg_card = "#0d2e66"
        self.bg_light_card = "#1a4d99"
        self.accent_orange = "#ff8c00"
        self.accent_orange_light = "#ffa500"
        self.accent_gold = "#ffc107"
        self.text_light = "#e0e0e0"
        self.text_white = "#ffffff"
        
        self.matcher = AstrologyMatcher()
        self.boy_data = None
        self.girl_data = None
        self.results = None
        
        self.create_gui()
    
    def create_gui(self):
        """Create the main GUI"""
        # Header with gradient effect
        header = tk.Frame(self.root, bg=self.bg_card, height=90)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="💫 VEDIC ASTROLOGY LOVE MATCHER 💫", 
                        font=("Arial", 26, "bold"), fg=self.accent_orange, bg=self.bg_card)
        title.pack(pady=(15, 5))
        
        subtitle = tk.Label(header, text="✨ Find Your Cosmic Connection Through Guna Milan ✨",
                           font=("Arial", 13, "italic"), fg=self.accent_gold, bg=self.bg_card)
        subtitle.pack(pady=(0, 15))
        
        # Main content area with notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', font=("Arial", 11, "bold"))
        
        # Tab 1: Input Boy's Data
        self.boy_frame = ttk.Frame(notebook)
        notebook.add(self.boy_frame, text="👨 Boy's Details")
        self.create_input_frame(self.boy_frame, "Boy", self.on_boy_data_saved)
        
        # Tab 2: Input Girl's Data
        self.girl_frame = ttk.Frame(notebook)
        notebook.add(self.girl_frame, text="👩 Girl's Details")
        self.create_input_frame(self.girl_frame, "Girl", self.on_girl_data_saved)
        
        # Tab 3: Results
        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame, text="💕 Compatibility Results")
        self.create_results_frame(self.results_frame)
    
    def create_input_frame(self, parent, person_type, save_callback):
        """Create input frame for person details - simplified"""
        container = tk.Frame(parent, bg=self.bg_dark)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(container, bg=self.bg_dark, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_dark)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card container
        card = tk.Frame(scrollable_frame, bg=self.bg_card, relief=tk.RAISED, bd=2)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Inner padding frame
        inner = tk.Frame(card, bg=self.bg_card)
        inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Title
        title = tk.Label(inner, text=f"Enter {person_type}'s Details", 
                        font=("Arial", 18, "bold"), fg=self.accent_orange, bg=self.bg_card)
        title.pack(pady=(0, 25))
        
        # Name
        tk.Label(inner, text="👤 Full Name:", font=("Arial", 12, "bold"), 
                fg=self.accent_gold, bg=self.bg_card).pack(anchor="w", pady=(15, 8))
        name_entry = tk.Entry(inner, font=("Arial", 12), bg="#1a3d66", fg=self.text_light,
                             insertbackground=self.accent_orange, width=40, bd=2)
        name_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Birth Date
        tk.Label(inner, text="📅 Birth Date (DD/MM/YYYY):", font=("Arial", 12, "bold"),
                fg=self.accent_gold, bg=self.bg_card).pack(anchor="w", pady=(15, 8))
        date_entry = tk.Entry(inner, font=("Arial", 12), bg="#1a3d66", fg=self.text_light,
                             insertbackground=self.accent_orange, width=40, bd=2)
        date_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Birth Time
        tk.Label(inner, text="🕐 Birth Time (HH:MM - 24hr format):", font=("Arial", 12, "bold"),
                fg=self.accent_gold, bg=self.bg_card).pack(anchor="w", pady=(15, 8))
        time_entry = tk.Entry(inner, font=("Arial", 12), bg="#1a3d66", fg=self.text_light,
                             insertbackground=self.accent_orange, width=40, bd=2)
        time_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        
        # Birth Place / Location
        tk.Label(inner, text="📍 Birth Place (City/Location):", font=("Arial", 12, "bold"),
                fg=self.accent_gold, bg=self.bg_card).pack(anchor="w", pady=(15, 8))
        place_entry = tk.Entry(inner, font=("Arial", 12), bg="#1a3d66", fg=self.text_light,
                              insertbackground=self.accent_orange, width=40, bd=2)
        place_entry.pack(fill=tk.X, pady=(0, 30), ipady=8)
        
        # Save Button
        def save_data():
            try:
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", f"Please enter {person_type}'s name")
                    return
                
                birth_date = date_entry.get().strip()
                day, month, year = map(int, birth_date.split("/"))
                datetime(year, month, day)
                
                birth_time = time_entry.get().strip()
                hour, minute = map(int, birth_time.split(":"))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError("Invalid time")
                
                birthplace = place_entry.get().strip()
                if not birthplace:
                    birthplace = "Unknown"
                
                data = {
                    "name": name,
                    "day": day,
                    "month": month,
                    "year": year,
                    "birth_time": birth_time,
                    "birthplace": birthplace,
                    "zodiac_sign": self.matcher.get_zodiac_sign(month, day),
                    "gana": self.matcher.GANAS.keys().__iter__().__next__(),  # Default: Deva
                    "yoni": list(self.matcher.YONIS.keys())[0],  # Default: Ashwa
                    "rajju": list(self.matcher.RAJJUS.keys())[2],  # Default: Adi
                    "nadi": self.matcher.calculate_nadi_guna(birth_time)
                }
                
                save_callback(data)
                messagebox.showinfo("Success", f"✅ {person_type}'s details saved!\n\nZodiac: {data['zodiac_sign']}")
                
            except ValueError as e:
                messagebox.showerror("Invalid Input", f"Please enter valid details.\n\nError: {str(e)}")
        
        btn_frame = tk.Frame(inner, bg=self.bg_card)
        btn_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(btn_frame, text=f"💾 Save {person_type}'s Data", 
                            font=("Arial", 13, "bold"), bg=self.accent_orange, fg=self.text_white,
                            command=save_data, padx=30, pady=12, relief=tk.RAISED, bd=2,
                            cursor="hand2", activebackground=self.accent_orange_light)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_boy_data_saved(self, data):
        """Callback when boy's data is saved"""
        self.boy_data = data
    
    def on_girl_data_saved(self, data):
        """Callback when girl's data is saved"""
        self.girl_data = data
    
    def create_results_frame(self, parent):
        """Create results display frame with auto-calculation"""
        container = tk.Frame(parent, bg=self.bg_dark)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Calculate button
        btn_frame = tk.Frame(container, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        def calculate():
            if not self.boy_data or not self.girl_data:
                messagebox.showwarning("Missing Data", 
                    "Please fill in both Boy's and Girl's details first!")
                return
            
            self.results = self.matcher.calculate_compatibility(self.boy_data, self.girl_data)
            display_results()
        
        calc_btn = tk.Button(btn_frame, text="💕 Calculate Compatibility", 
                            font=("Arial", 14, "bold"), bg=self.accent_orange, fg=self.text_white,
                            command=calculate, padx=35, pady=14, relief=tk.RAISED, bd=2,
                            cursor="hand2", activebackground=self.accent_orange_light)
        calc_btn.pack(side=tk.LEFT)
        
        # Results display area with scrolling
        results_scroll_frame = tk.Frame(container, bg=self.bg_card, relief=tk.RAISED, bd=2)
        results_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_scroll_frame, font=("Courier", 11),
                                                      bg=self.bg_card, fg=self.text_light,
                                                      insertbackground=self.accent_orange,
                                                      wrap=tk.WORD, padx=18, pady=18,
                                                      relief=tk.FLAT, bd=0)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colors
        self.results_text.tag_config("title", font=("Courier", 15, "bold"), foreground=self.accent_orange)
        self.results_text.tag_config("header", font=("Courier", 13, "bold"), foreground=self.accent_gold)
        self.results_text.tag_config("excellent", foreground="#00ff41", font=("Courier", 11, "bold"))
        self.results_text.tag_config("very_good", foreground="#00ff88", font=("Courier", 11, "bold"))
        self.results_text.tag_config("good", foreground="#ffff00", font=("Courier", 11, "bold"))
        self.results_text.tag_config("average", foreground=self.accent_orange, font=("Courier", 11, "bold"))
        self.results_text.tag_config("poor", foreground="#ff6b6b", font=("Courier", 11, "bold"))
        
        def display_results():
            self.results_text.delete(1.0, tk.END)
            
            if not self.results:
                return
            
            res = self.results
            boy = res['boy_name']
            girl = res['girl_name']
            score = res['total_score']
            percentage = res['percentage']
            compat_type, interpretation = self.matcher.get_compatibility_interpretation(score)
            
            # Title
            self.results_text.insert(tk.END, "✨ COMPATIBILITY ANALYSIS ✨\n", "title")
            self.results_text.insert(tk.END, "═" * 80 + "\n\n")
            
            # Names and scores
            self.results_text.insert(tk.END, f"💙 {boy:<35} 💗 {girl}\n", "header")
            self.results_text.insert(tk.END, "─" * 80 + "\n\n")
            
            # Overall score with colored tag
            self.results_text.insert(tk.END, f"Overall Compatibility Score: {score}/36 ({percentage}%)\n", "header")
            
            if score >= 32:
                tag = "excellent"
                emoji = "🌟🌟🌟🌟🌟"
            elif score >= 28:
                tag = "very_good"
                emoji = "🌟🌟🌟🌟"
            elif score >= 24:
                tag = "good"
                emoji = "🌟🌟🌟"
            elif score >= 18:
                tag = "average"
                emoji = "🌟🌟"
            else:
                tag = "poor"
                emoji = "🌟"
            
            self.results_text.insert(tk.END, f"Rating: {compat_type} - {emoji}\n", tag)
            self.results_text.insert(tk.END, f"Interpretation: {interpretation}\n\n")
            
            self.results_text.insert(tk.END, "=" * 80 + "\n")
            self.results_text.insert(tk.END, "DETAILED BREAKDOWN\n", "header")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            
            details_order = ["nadi", "gana", "yoni", "rashi", "bhakut", "rajju"]
            detail_names = {
                "nadi": "🌬️ Nadi (Nervous Temperament)",
                "gana": "🎭 Gana (Nature/Character)",
                "yoni": "🐾 Yoni (Sexual/Physical)",
                "rashi": "♈ Rashi (Zodiac Sign)",
                "bhakut": "⚡ Bhakut (Nature/Strength)",
                "rajju": "👑 Rajju (Family Line)"
            }
            
            for detail_key in details_order:
                detail = res["details"][detail_key]
                score_val = detail["score"]
                max_val = detail["max"]
                
                # Bar visualization
                filled = int((score_val / max_val) * 25)
                bar = "█" * filled + "░" * (25 - filled)
                
                self.results_text.insert(tk.END, f"{detail_names[detail_key]}\n")
                self.results_text.insert(tk.END, f"[{bar}] {score_val}/{max_val}\n")
                
                if detail_key == "nadi":
                    self.results_text.insert(tk.END, f"  Boy: {detail['boy_nadi']} | Girl: {detail['girl_nadi']}\n")
                elif detail_key == "gana":
                    self.results_text.insert(tk.END, f"  Boy: {detail['boy_gana']} | Girl: {detail['girl_gana']}\n")
                elif detail_key == "yoni":
                    self.results_text.insert(tk.END, f"  Boy: {detail['boy_yoni']} | Girl: {detail['girl_yoni']}\n")
                elif detail_key == "rashi":
                    self.results_text.insert(tk.END, f"  Boy: {detail['boy_rashi']} | Girl: {detail['girl_rashi']}\n")
                elif detail_key == "rajju":
                    self.results_text.insert(tk.END, f"  Boy: {detail['boy_rajju']} | Girl: {detail['girl_rajju']}\n")
                
                self.results_text.insert(tk.END, "\n")
            
            self.results_text.insert(tk.END, "=" * 80 + "\n")
            self.results_text.insert(tk.END, "💕 May Your Love Story Shine Like the Stars 💕\n", "header")


def main_gui():
    """Launch GUI application"""
    root = tk.Tk()
    app = AstrologyMatcherGUI(root)
    root.mainloop()


def main():
    """Main entry point"""
    # Check if running with GUI or CLI
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Command line mode
        matcher = AstrologyMatcher()
        matcher.run()
    else:
        # GUI mode (default)
        main_gui()


if __name__ == "__main__":
    main()
