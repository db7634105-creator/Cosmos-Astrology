"""
Main GUI Application for Astrologers Profile
Displays astrologer profiles with photos and call functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from astrologers_data import ASTROLOGERS
from call_handler import make_call, log_call_history
from image_utils import load_image


class AstrologerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Astrologers Directory")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f0f0")
        
        # Store PhotoImage references to prevent garbage collection
        self.photo_images = []
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create scrollable frame for astrologers
        self.create_scrollable_content()
        
        # Create footer
        self.create_footer()
    
    def create_header(self):
        """Create application header"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="✨ Astrologers Directory ✨",
            font=("Arial", 28, "bold"),
            fg="#4a3f8f",
            bg="#f0f0f0"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Connect with expert astrologers for guidance",
            font=("Arial", 12),
            fg="#666666",
            bg="#f0f0f0"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
    
    def create_scrollable_content(self):
        """Create scrollable frame with astrologer cards"""
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(self.main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create grid of astrologer cards
        self.create_astrologer_cards(scrollable_frame)
    
    def create_astrologer_cards(self, parent):
        """Create individual astrologer profile cards"""
        # Create a grid layout (3 columns)
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for idx, astrologer in enumerate(ASTROLOGERS):
            row = idx // 3
            col = idx % 3
            
            self.create_astrologer_card(cards_frame, astrologer, row, col)
    
    def create_astrologer_card(self, parent, astrologer, row, col):
        """Create a single astrologer profile card"""
        # Card frame
        card_frame = tk.Frame(
            parent,
            bg="white",
            relief=tk.RAISED,
            bd=2
        )
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configure column weights for grid
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        
        # Load and display image
        img = load_image(astrologer["image_url"], size=(280, 280))
        photo = ImageTk.PhotoImage(img)
        self.photo_images.append(photo)  # Keep reference
        
        img_label = tk.Label(card_frame, image=photo, bg="white")
        img_label.pack(pady=15, padx=15, anchor="n")
        
        # Astrologer name
        name_label = tk.Label(
            card_frame,
            text=astrologer["name"],
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#4a3f8f"
        )
        name_label.pack()
        
        # Specialization
        spec_label = tk.Label(
            card_frame,
            text=astrologer["specialization"],
            font=("Arial", 10),
            bg="white",
            fg="#666666"
        )
        spec_label.pack()
        
        # Experience
        exp_label = tk.Label(
            card_frame,
            text=f"Experience: {astrologer['experience']}",
            font=("Arial", 9),
            bg="white",
            fg="#888888"
        )
        exp_label.pack()
        
        # Rating
        rating_label = tk.Label(
            card_frame,
            text=f"⭐ Rating: {astrologer['rating']}/5.0",
            font=("Arial", 9),
            bg="white",
            fg="#ff9800"
        )
        rating_label.pack()
        
        # Divider
        divider = tk.Frame(card_frame, height=1, bg="#cccccc")
        divider.pack(fill=tk.X, pady=10, padx=15)
        
        # Call button
        call_button = tk.Button(
            card_frame,
            text="📞 Call Now",
            font=("Arial", 11, "bold"),
            bg="#4a3f8f",
            fg="white",
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=10,
            command=lambda: self.on_call_click(astrologer)
        )
        call_button.pack(pady=(0, 15), padx=15, fill=tk.X)
        
        # View profile button (optional)
        profile_button = tk.Button(
            card_frame,
            text="View Profile",
            font=("Arial", 10),
            bg="#e0e0e0",
            fg="#333333",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=lambda: self.view_profile(astrologer)
        )
        profile_button.pack(pady=(0, 15), padx=15, fill=tk.X)
    
    def on_call_click(self, astrologer):
        """Handle call button click"""
        # Confirm dialog
        result = messagebox.askyesno(
            "Confirm Call",
            f"Do you want to call {astrologer['name']}?\n\nPhone: {astrologer['phone']}"
        )
        
        if result:
            success, message = make_call(astrologer['phone'], astrologer['name'])
            log_call_history(astrologer['name'], astrologer['phone'])
            
            if success:
                messagebox.showinfo("Call", message)
            else:
                messagebox.showerror("Call Failed", message)
    
    def view_profile(self, astrologer):
        """Display detailed profile information"""
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{astrologer['name']} - Profile")
        profile_window.geometry("500x600")
        profile_window.configure(bg="#f0f0f0")
        
        # Profile content
        content_frame = ttk.Frame(profile_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load image
        img = load_image(astrologer["image_url"], size=(300, 300))
        photo = ImageTk.PhotoImage(img)
        self.photo_images.append(photo)
        
        img_label = tk.Label(content_frame, image=photo, bg="white", relief=tk.RAISED, bd=2)
        img_label.pack(pady=10)
        
        # Profile details
        details_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        details_text = f"""
Name: {astrologer['name']}

Specialization: {astrologer['specialization']}

Experience: {astrologer['experience']}

Rating: {astrologer['rating']}/5.0 ⭐

Phone: {astrologer['phone']}

ID: {astrologer['id']}
        """
        
        details_label = tk.Label(
            details_frame,
            text=details_text,
            font=("Arial", 11),
            justify=tk.LEFT,
            bg="white",
            fg="#333333",
            padx=15,
            pady=15
        )
        details_label.pack(anchor="w")
        
        # Close button
        close_btn = tk.Button(
            content_frame,
            text="Close",
            font=("Arial", 10, "bold"),
            bg="#666666",
            fg="white",
            command=profile_window.destroy
        )
        close_btn.pack(pady=10, fill=tk.X)
    
    def create_footer(self):
        """Create application footer"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0), side=tk.BOTTOM)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2025 Astrologers Directory | All Rights Reserved",
            font=("Arial", 9),
            fg="#999999",
            bg="#f0f0f0"
        )
        footer_label.pack()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AstrologerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
