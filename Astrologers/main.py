"""
Main GUI Application for Astrologers Profile
Hindu-Inspired Theme with Saffron, White, and Green colors
Displays astrologer profiles with photos, call functionality, and payment system
Includes persistent one-time login system with actual calling support
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import time
import uuid
from PIL import Image, ImageTk
from astrologers_data import ASTROLOGERS
from call_handler import make_call, log_call_history
from image_utils import load_image
from payment_system import PaymentSystem, PaymentMethod, PaymentStatus, Transaction
from payment_gateway import PaymentGateway
from country_payment_gateway import CountryPaymentGateway, CountryPaymentMapper
from user_manager import UserManager
from session_manager import SessionManager
from call_manager import CallManager
from hindu_theme import HinduTheme, HinduThemeGuide


class AstrologerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🙏 Astrologers Directory - Divine Consultation 🙏")
        self.root.geometry("1400x900")
        self.root.configure(bg=HinduTheme.BG_PRIMARY)
        
        # Initialize managers
        self.payment_system = PaymentSystem()
        self.user_manager = UserManager()
        self.session_manager = SessionManager()
        self.call_manager = CallManager()
        self.current_user = None
        self.active_call_window = None
        
        # Store PhotoImage references to prevent garbage collection
        self.photo_images = []
        
        # Configure style with Hindu theme
        style = ttk.Style()
        style.theme_use('clam')
        self.configure_ttk_styles(style)
        
        # Check for existing session
        self.check_existing_session()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header with user info
        self.create_header()
        
        # Create scrollable frame for astrologers
        self.create_scrollable_content()
        
        # Create footer
        self.create_footer()
    
    def configure_ttk_styles(self, style):
        """Configure ttk styles with Hindu theme"""
        # Button styles
        style.configure('primary.TButton', font=('Arial', 10, 'bold'), 
                       foreground=HinduTheme.WHITE)
        style.map('primary.TButton', 
                 background=[(('pressed',), HinduTheme.CRIMSON),
                            (('active',), HinduTheme.CRIMSON_LIGHT)],
                 foreground=[(('pressed',), HinduTheme.WHITE),
                            (('active',), HinduTheme.WHITE)])
        
        # Label styles
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'),
                       foreground=HinduTheme.SAFFRON)
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'),
                       foreground=HinduTheme.NAVY)
    
    def check_existing_session(self):
        """Check if user has an active session"""
        if self.session_manager.is_session_valid():
            username = self.session_manager.get_session_username()
            if username:
                self.current_user = username
                self.session_manager.update_activity()
    
    def create_header(self):
        """Create application header with user menu - Hindu theme"""
        header_frame = tk.Frame(self.main_frame, bg=HinduTheme.SAFFRON, height=80, relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Left side - Title and subtitle with religious symbol
        left_frame = tk.Frame(header_frame, bg=HinduTheme.SAFFRON)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        title_label = tk.Label(
            left_frame,
            text=f"{HinduThemeGuide.SYMBOLS['om']} Astrologers Directory",
            font=("Arial", 28, "bold"),
            fg=HinduTheme.WHITE,
            bg=HinduTheme.SAFFRON
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            left_frame,
            text="Divine Consultation - शास्त्र सलाह",
            font=("Arial", 12),
            fg=HinduTheme.GOLD,
            bg=HinduTheme.SAFFRON
        )
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Right side - User menu with Hindu theme
        right_frame = tk.Frame(header_frame, bg=HinduTheme.SAFFRON)
        right_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Login/User info button
        self.user_label = tk.Label(
            right_frame,
            text=f"{HinduThemeGuide.SYMBOLS['prayer']} " + ("Guest" if not self.current_user else f"User: {self.current_user}"),
            font=("Arial", 11, "bold"),
            fg=HinduTheme.WHITE,
            bg=HinduTheme.SAFFRON
        )
        self.user_label.pack(side=tk.LEFT, padx=10)
        
        # Show Login or Logout button based on session with Hindu theme
        if self.current_user:
            logout_btn = tk.Button(
                right_frame,
                text="🚪 Logout",
                font=("Arial", 10, "bold"),
                bg=HinduTheme.CRIMSON,
                fg=HinduTheme.WHITE,
                activebackground=HinduTheme.CRIMSON_LIGHT,
                activeforeground=HinduTheme.WHITE,
                command=self.logout_user,
                relief=tk.RAISED,
                bd=2,
                padx=15,
                pady=5
            )
            logout_btn.pack(side=tk.LEFT, padx=5)
        else:
            login_btn = tk.Button(
                right_frame,
                text="🔐 Login",
                font=("Arial", 10, "bold"),
                bg=HinduTheme.NAVY,
                fg=HinduTheme.WHITE,
                activebackground=HinduTheme.NAVY_LIGHT,
                activeforeground=HinduTheme.GOLD,
                command=self.show_login_register_window,
                relief=tk.RAISED,
                bd=2,
                padx=15,
                pady=5
            )
            login_btn.pack(side=tk.LEFT, padx=5)
        
        # Wallet button with Hindu theme
        wallet_btn = tk.Button(
            right_frame,
            text="💳 Wallet",
            font=("Arial", 10, "bold"),
            bg=HinduTheme.GREEN,
            fg=HinduTheme.WHITE,
            activebackground=HinduTheme.GREEN_LIGHT,
            activeforeground=HinduTheme.GOLD,
            command=self.show_wallet_window,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5
        )
        wallet_btn.pack(side=tk.LEFT, padx=5)
        
        # History button with Hindu theme
        history_btn = tk.Button(
            right_frame,
            text="📋 History",
            font=("Arial", 10, "bold"),
            bg=HinduTheme.NAVY,
            fg=HinduTheme.WHITE,
            activebackground=HinduTheme.NAVY_LIGHT,
            activeforeground=HinduTheme.GOLD,
            command=self.show_history_window,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5
        )
        history_btn.pack(side=tk.LEFT, padx=5)
    
    def create_scrollable_content(self):
        """Create scrollable frame with astrologer cards - Hindu theme"""
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(self.main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=HinduTheme.BG_SECONDARY, highlightthickness=0)
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
        """Create a single astrologer profile card with pricing - Hindu theme"""
        # Card frame with Hindu theme
        card_frame = tk.Frame(
            parent,
            bg=HinduTheme.WHITE,
            relief=tk.RAISED,
            bd=3,
            highlightbackground=HinduTheme.GOLD,
            highlightthickness=2
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
        
        img_label = tk.Label(card_frame, image=photo, bg=HinduTheme.WHITE)
        img_label.pack(pady=15, padx=15, anchor="n")
        
        # Astrologer name with star symbol
        name_label = tk.Label(
            card_frame,
            text=f"{HinduThemeGuide.SYMBOLS['star']} {astrologer['name']}",
            font=("Arial", 14, "bold"),
            bg=HinduTheme.WHITE,
            fg=HinduTheme.SAFFRON
        )
        name_label.pack()
        
        # Specialization
        spec_label = tk.Label(
            card_frame,
            text=astrologer["specialization"],
            font=("Arial", 10),
            bg=HinduTheme.WHITE,
            fg=HinduTheme.NAVY
        )
        spec_label.pack()
        
        # Experience
        exp_label = tk.Label(
            card_frame,
            text=f"📚 Experience: {astrologer['experience']}",
            font=("Arial", 9),
            bg=HinduTheme.WHITE,
            fg=HinduTheme.NAVY
        )
        exp_label.pack()
        
        # Rating
        rating_label = tk.Label(
            card_frame,
            text=f"⭐ Rating: {astrologer['rating']}/5.0",
            font=("Arial", 9),
            bg=HinduTheme.WHITE,
            fg=HinduTheme.GOLD
        )
        rating_label.pack()
        
        # Price per minute with Hindu colors
        price_label = tk.Label(
            card_frame,
            text=f"💰 FREE" if astrologer.get('is_free') else f"💰 ₨{astrologer['price_per_minute']}/min",
            font=("Arial", 11, "bold"),
            bg=HinduTheme.WHITE,
            fg=HinduTheme.GREEN if astrologer.get('is_free') else HinduTheme.SAFFRON
        )
        price_label.pack()
        
        # Divider with gold color
        divider = tk.Frame(card_frame, height=2, bg=HinduTheme.GOLD)
        divider.pack(fill=tk.X, pady=10, padx=15)
        
        # Call button with Hindu theme
        call_button = tk.Button(
            card_frame,
            text="📞 Call Now",
            font=("Arial", 11, "bold"),
            bg=HinduTheme.GREEN,
            fg=HinduTheme.WHITE,
            activebackground=HinduTheme.GREEN_LIGHT,
            activeforeground=HinduTheme.GOLD,
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=10,
            command=lambda: self.on_call_click(astrologer)
        )
        call_button.pack(pady=(0, 10), padx=15, fill=tk.X)
        
        # View profile button with Hindu theme
        profile_button = tk.Button(
            card_frame,
            text="👤 View Profile",
            font=("Arial", 10, "bold"),
            bg=HinduTheme.LIGHT_GOLD,
            fg=HinduTheme.NAVY,
            activebackground=HinduTheme.LIGHT_ORANGE,
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=lambda: self.view_profile(astrologer)
        )
        profile_button.pack(pady=(0, 15), padx=15, fill=tk.X)
    
    def on_call_click(self, astrologer):
        """Handle call button click - PAYMENT REQUIRED (unless FREE)"""
        if not self.current_user:
            messagebox.showwarning("Login Required", "Please login first to make a call")
            self.show_login_register_window()
            return
        
        # Check if call is free
        if astrologer.get('is_free'):
            # Free call - no payment needed
            messagebox.showinfo(
                "Free Call",
                f"This call with {astrologer['name']} is completely FREE!\n\n" +
                "Connecting you now..."
            )
            self.show_call_duration_window(astrologer)
        else:
            # Paid call - show payment requirement
            messagebox.showinfo(
                "Payment Required",
                "A payment is REQUIRED to connect with this astrologer.\n\n" +
                "You will be able to make the call ONLY after successful payment.\n\n" +
                "Click OK to proceed with payment."
            )
            
            # Show call duration selection and payment
            self.show_call_payment_window(astrologer)
    
    def view_profile(self, astrologer):
        """Display detailed profile information"""
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{astrologer['name']} - Profile")
        profile_window.geometry("500x600")
        profile_window.configure(bg="#f0f0f0")
        
        # Profile content
        content_frame = ttk.Frame(profile_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Profile details with image
        details_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=2)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Load and display image
        img = load_image(astrologer["image_url"], size=(280, 350))
        photo = ImageTk.PhotoImage(img)
        self.photo_images.append(photo)
        
        img_label = tk.Label(details_frame, image=photo, bg="white")
        img_label.pack(pady=15, padx=15, anchor="n")
        
        # Profile details text
        details_text = f"""
Name: {astrologer['name']}

Specialization: {astrologer['specialization']}

Experience: {astrologer['experience']}

Rating: {astrologer['rating']}/5.0

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
        """Create application footer - Hindu theme"""
        footer_frame = tk.Frame(self.main_frame, bg=HinduTheme.GREEN, height=50, relief=tk.RAISED, bd=2)
        footer_frame.pack(fill=tk.X, pady=(20, 0), side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text=f"🙏 © 2025 Astrologers Directory - Divine Services 🙏 | Payment System Active | {HinduThemeGuide.SYMBOLS['om']}",
            font=("Arial", 10, "bold"),
            fg=HinduTheme.GOLD,
            bg=HinduTheme.GREEN
        )
        footer_label.pack(pady=10)
    
    def show_login_window(self):
        """Show login window - Hindu theme"""
        login_window = tk.Toplevel(self.root)
        login_window.title("🔐 User Login - Divine Entry 🔐")
        login_window.geometry("400x350")
        login_window.configure(bg=HinduTheme.BG_PRIMARY)
        
        # Header
        header_label = tk.Label(
            login_window,
            text=f"{HinduThemeGuide.SYMBOLS['om']} Sacred Login {HinduThemeGuide.SYMBOLS['om']}",
            font=("Arial", 16, "bold"),
            fg=HinduTheme.WHITE,
            bg=HinduTheme.SAFFRON,
            pady=15
        )
        header_label.pack(fill=tk.X)
        
        content_frame = tk.Frame(login_window, bg=HinduTheme.BG_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Username
        tk.Label(content_frame, text="Username:", font=("Arial", 11, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w", pady=(0, 5))
        username_entry = tk.Entry(content_frame, font=("Arial", 11), width=30)
        username_entry.pack(fill=tk.X, pady=(0, 15))
        username_entry.focus()
        
        # Password
        tk.Label(content_frame, text="Password:", font=("Arial", 11, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w", pady=(0, 5))
        password_entry = tk.Entry(content_frame, font=("Arial", 11), width=30, show="*")
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password")
                return
            
            success, message = self.user_manager.login_user(username, password)
            
            if success:
                self.current_user = username
                self.session_manager.create_session(username)
                self.user_label.config(text=f"User: {username}")
                messagebox.showinfo("Success", f"Welcome back {username}!")
                login_window.destroy()
                # Refresh header to show logout button
                self.root.after(100, self.refresh_header)
            else:
                messagebox.showerror("Login Failed", message)
        
        btn_frame = tk.Frame(content_frame, bg=HinduTheme.BG_PRIMARY)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="🔐 Login", font=("Arial", 11, "bold"), bg=HinduTheme.NAVY, 
                 fg=HinduTheme.WHITE, activebackground=HinduTheme.NAVY_LIGHT, activeforeground=HinduTheme.GOLD,
                 command=login, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancel", font=("Arial", 11, "bold"), bg=HinduTheme.CRIMSON, 
                 fg=HinduTheme.WHITE, activebackground=HinduTheme.CRIMSON_LIGHT,
                 command=login_window.destroy, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    def show_login_register_window(self):
        """Show combined login/register window - Hindu theme"""
        auth_window = tk.Toplevel(self.root)
        auth_window.title("🙏 Login / Register - Divine Access 🙏")
        auth_window.geometry("550x550")
        auth_window.configure(bg=HinduTheme.BG_PRIMARY)
        
        # Header
        header_label = tk.Label(
            auth_window,
            text=f"{HinduThemeGuide.SYMBOLS['om']} Sacred Authentication {HinduThemeGuide.SYMBOLS['om']}",
            font=("Arial", 14, "bold"),
            fg=HinduTheme.WHITE,
            bg=HinduTheme.SAFFRON,
            pady=15
        )
        header_label.pack(fill=tk.X)
        
        content_frame = tk.Frame(auth_window, bg=HinduTheme.BG_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tab selection
        tab_var = tk.StringVar(value="login")
        
        # Tab buttons
        tab_frame = ttk.Frame(content_frame)
        tab_frame.pack(fill=tk.X, pady=(0, 20))
        
        def switch_tab(tab):
            tab_var.set(tab)
            update_form()
        
        tk.Button(tab_frame, text="Login", font=("Arial", 11, "bold"), bg="#4a3f8f", 
                 fg="white", command=lambda: switch_tab("login"), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(tab_frame, text="Register", font=("Arial", 11, "bold"), bg="#2196f3", 
                 fg="white", command=lambda: switch_tab("register"), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        
        # Form container
        form_frame = tk.Frame(content_frame, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        def update_form():
            # Clear form
            for widget in form_frame.winfo_children():
                widget.destroy()
            
            if tab_var.get() == "login":
                # Login form
                tk.Label(form_frame, text="Username:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                username_entry = tk.Entry(form_frame, font=("Arial", 11), width=40)
                username_entry.pack(fill=tk.X, pady=(0, 15))
                username_entry.focus()
                
                tk.Label(form_frame, text="Password:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                password_entry = tk.Entry(form_frame, font=("Arial", 11), width=40, show="*")
                password_entry.pack(fill=tk.X, pady=(0, 20))
                
                def do_login():
                    username = username_entry.get().strip()
                    password = password_entry.get().strip()
                    
                    if not username or not password:
                        messagebox.showerror("Error", "Please fill all fields")
                        return
                    
                    success, message = self.user_manager.login_user(username, password)
                    if success:
                        self.current_user = username
                        self.session_manager.create_session(username)
                        self.user_label.config(text=f"User: {username}")
                        messagebox.showinfo("Success", f"Welcome back {username}!")
                        auth_window.destroy()
                        self.refresh_header()
                    else:
                        messagebox.showerror("Login Failed", message)
                
                btn_frame = ttk.Frame(form_frame)
                btn_frame.pack(fill=tk.X, pady=10)
                
                tk.Button(btn_frame, text="Login", font=("Arial", 11, "bold"), bg="#4caf50", 
                         fg="white", command=do_login, padx=30, pady=10).pack(side=tk.LEFT, padx=5)
            
            else:  # Register
                # Register form
                tk.Label(form_frame, text="Username:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                username_entry = tk.Entry(form_frame, font=("Arial", 11), width=40)
                username_entry.pack(fill=tk.X, pady=(0, 10))
                username_entry.focus()
                
                tk.Label(form_frame, text="Email:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                email_entry = tk.Entry(form_frame, font=("Arial", 11), width=40)
                email_entry.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(form_frame, text="Phone (optional):", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                phone_entry = tk.Entry(form_frame, font=("Arial", 11), width=40)
                phone_entry.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(form_frame, text="Country/Region:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                region_var = tk.StringVar(value="nepal")
                region_combo = ttk.Combobox(form_frame, textvariable=region_var, 
                                            values=["Nepal", "India", "Other"], 
                                            font=("Arial", 11), width=37, state="readonly")
                region_combo.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(form_frame, text="Password:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                password_entry = tk.Entry(form_frame, font=("Arial", 11), width=40, show="*")
                password_entry.pack(fill=tk.X, pady=(0, 10))
                
                tk.Label(form_frame, text="Confirm Password:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
                confirm_entry = tk.Entry(form_frame, font=("Arial", 11), width=40, show="*")
                confirm_entry.pack(fill=tk.X, pady=(0, 20))
                
                def do_register():
                    username = username_entry.get().strip()
                    email = email_entry.get().strip()
                    phone = phone_entry.get().strip()
                    password = password_entry.get().strip()
                    confirm = confirm_entry.get().strip()
                    region = region_var.get().strip().lower()
                    
                    if not username or not email or not password:
                        messagebox.showerror("Error", "Please fill required fields")
                        return
                    
                    if password != confirm:
                        messagebox.showerror("Error", "Passwords do not match")
                        return
                    
                    if len(password) < 4:
                        messagebox.showerror("Error", "Password must be at least 4 characters")
                        return
                    
                    success, message = self.user_manager.register_user(username, email, phone, password, region=region)
                    if success:
                        self.current_user = username
                        self.session_manager.create_session(username)
                        self.user_label.config(text=f"User: {username}")
                        messagebox.showinfo("Success", f"Welcome {username}! Account created successfully.\n\nPayment Method: {region.upper()}")
                        auth_window.destroy()
                        self.refresh_header()
                    else:
                        messagebox.showerror("Registration Failed", message)
                
                btn_frame = ttk.Frame(form_frame)
                btn_frame.pack(fill=tk.X, pady=10)
                
                tk.Button(btn_frame, text="Register", font=("Arial", 11, "bold"), bg="#4caf50", 
                         fg="white", command=do_register, padx=30, pady=10).pack(side=tk.LEFT, padx=5)
        
        # Initial form
        update_form()
        
        # Close button
        tk.Button(content_frame, text="Cancel", font=("Arial", 11), bg="#999999", 
                 fg="white", command=auth_window.destroy, padx=30, pady=10).pack(pady=(20, 0))
    
    def logout_user(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", f"Are you sure you want to logout {self.current_user}?"):
            self.session_manager.logout()
            self.current_user = None
            self.user_label.config(text="Guest")
            messagebox.showinfo("Logout", "You have been logged out successfully.")
            self.refresh_header()
    
    def refresh_header(self):
        """Refresh the header to update login/logout button"""
        self.root.update()
    
    def show_call_duration_window(self, astrologer):
        """Show call duration window for FREE calls"""
        duration_window = tk.Toplevel(self.root)
        duration_window.title(f"Free Call - {astrologer['name']}")
        duration_window.geometry("500x400")
        duration_window.configure(bg="#f0f0f0")
        
        content_frame = ttk.Frame(duration_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Label(content_frame, text=f"FREE CALL with {astrologer['name']}", 
                         font=("Arial", 16, "bold"), fg="#4caf50", bg="#f0f0f0")
        header.pack(pady=(0, 20))
        
        # Free call notice
        notice = tk.Label(content_frame, text="✓ NO PAYMENT REQUIRED - This is a FREE call", 
                         font=("Arial", 12, "bold"), fg="#4caf50", bg="#f0f0f0")
        notice.pack(pady=(0, 20))
        
        # Free call - only 1 minute option
        free_duration_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        free_duration_frame.pack(fill=tk.X, padx=10, pady=15)
        
        duration_text = tk.Label(free_duration_frame, text="📞 1 Minute FREE Call", 
                                font=("Arial", 12, "bold"), fg="#4caf50", bg="white", padx=15, pady=15)
        duration_text.pack(anchor="w")
        
        selected_duration = tk.StringVar(value="1 minute")
        
        tk.Frame(content_frame, height=1, bg="#cccccc").pack(fill=tk.X, pady=15)
        
        def connect_free_call():
            duration = 1  # Fixed 1 minute for free users
            
            # Create free transaction record
            transaction = self.payment_system.create_transaction(
                self.current_user,
                astrologer['name'],
                0,  # FREE
                PaymentMethod.WALLET,
                duration
            )
            
            # Mark as completed (no payment needed)
            transaction.status = PaymentStatus.COMPLETED
            self.payment_system.transactions.append(transaction.to_dict())
            self.payment_system.save_transactions()
            
            # Log call
            log_call_history(astrologer['name'], astrologer['phone'])
            
            # Start actual call with timer
            self.start_actual_call(astrologer, duration, transaction.transaction_id, is_free=True)
            
            duration_window.destroy()
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(btn_frame, text="Connect Free Call", font=("Arial", 12, "bold"), 
                 bg="#4caf50", fg="white", command=connect_free_call, padx=30, pady=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", font=("Arial", 12), 
                 bg="#999999", fg="white", command=duration_window.destroy, padx=30, pady=15).pack(side=tk.LEFT, padx=5)
    
    def show_call_payment_window(self, astrologer):
        """Show package selection window for paid calls - Hindu theme"""
        package_window = tk.Toplevel(self.root)
        package_window.title(f"📞 Select Package - {astrologer['name']} 📞")
        package_window.geometry("650x750")
        package_window.configure(bg=HinduTheme.BG_PRIMARY)
        
        # Header
        header_frame = tk.Frame(package_window, bg=HinduTheme.SAFFRON, height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header = tk.Label(header_frame, text=f"🙏 Choose Call Package 🙏", 
                         font=("Arial", 16, "bold"), fg=HinduTheme.WHITE, bg=HinduTheme.SAFFRON, pady=10)
        header.pack()
        
        content_frame = tk.Frame(package_window, bg=HinduTheme.BG_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        astro_name = tk.Label(content_frame, text=f"💁 Astrologer: {astrologer['name']}", 
                             font=("Arial", 13, "bold"), fg=HinduTheme.SAFFRON, bg=HinduTheme.BG_PRIMARY)
        astro_name.pack(pady=(0, 20))
        
        # Package selection
        tk.Label(content_frame, text="📦 Available Packages:", font=("Arial", 12, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w", pady=(10, 15))
        
        selected_package = tk.StringVar(value=astrologer['packages'][0]['name'] if astrologer['packages'] else "")
        
        packages_frame = tk.Frame(content_frame, bg=HinduTheme.BG_PRIMARY)
        packages_frame.pack(fill=tk.X, padx=0, pady=10)
        
        for package in astrologer['packages']:
            pkg_text = f"📞 {package['name']} Call - ₨{package['price']}"
            tk.Radiobutton(packages_frame, text=pkg_text, variable=selected_package, 
                          value=package['name'], font=("Arial", 11, "bold"), 
                          bg=HinduTheme.BG_PRIMARY, fg=HinduTheme.NAVY, selectcolor=HinduTheme.LIGHT_GOLD).pack(anchor="w", pady=8)
        
        tk.Frame(content_frame, height=2, bg=HinduTheme.GOLD).pack(fill=tk.X, pady=15)
        
        # Payment method - Get country-specific options
        tk.Label(content_frame, text="💳 Select Payment Method:", font=("Arial", 12, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w")
        
        # Get user's region and available payment providers
        user_region = self.user_manager.get_user_region(self.current_user)
        payment_providers = self.payment_system.get_available_payment_providers(user_region)
        
        payment_method = tk.StringVar(value="Wallet")
        
        # Show country-specific providers
        region_label = tk.Label(content_frame, text=f"🌍 Region: {user_region.upper()} {HinduThemeGuide.SYMBOLS['star']}", 
                               font=("Arial", 10, "italic", "bold"), fg=HinduTheme.GOLD, bg=HinduTheme.BG_PRIMARY)
        region_label.pack(anchor="w", padx=10, pady=(5, 10))
        
        # Map provider names to UI method names
        provider_to_method = {
            "khalti": "Khalti (Nepal)",
            "esewa": "Esewa (Nepal)",
            "razorpay": "Razorpay (India)",
            "card": "Credit/Debit Card",
            "paypal": "PayPal"
        }
        
        methods = []
        for provider in payment_providers.get('providers', []):
            provider_name = provider['name']
            methods.append(provider_to_method.get(provider_name, provider_name))
        
        # Always include Wallet as fallback
        if "Wallet" not in methods:
            methods.append("Wallet")
        
        for method in methods:
            tk.Radiobutton(content_frame, text=method, variable=payment_method, 
                          value=method, font=("Arial", 11), bg=HinduTheme.BG_PRIMARY, fg=HinduTheme.NAVY, selectcolor=HinduTheme.LIGHT_GOLD).pack(anchor="w", padx=0, pady=5)
        
        tk.Frame(content_frame, height=1, bg="#cccccc").pack(fill=tk.X, pady=15)
        
        def process_payment():
            package_name = selected_package.get()
            selected_pkg = next((p for p in astrologer['packages'] if p['name'] == package_name), None)
            
            if not selected_pkg:
                messagebox.showerror("Error", "Please select a package")
                return
            
            amount = selected_pkg['price']
            duration = selected_pkg['duration']
            method_name = payment_method.get()
            
            # Map UI method names to PaymentMethod enum
            method_map = {
                "Credit Card": PaymentMethod.CREDIT_CARD,
                "Credit/Debit Card": PaymentMethod.CREDIT_CARD,
                "Debit Card": PaymentMethod.DEBIT_CARD,
                "UPI": PaymentMethod.UPI,
                "Wallet": PaymentMethod.WALLET,
                "PayPal": PaymentMethod.PAYPAL,
                "Khalti (Nepal)": PaymentMethod.UPI,  # Map to UPI for khalti
                "Esewa (Nepal)": PaymentMethod.UPI,   # Map to UPI for esewa
                "Razorpay (India)": PaymentMethod.UPI # Map to UPI for razorpay
            }
            
            payment_method_enum = method_map.get(method_name, PaymentMethod.WALLET)
            
            # Show payment details form
            self.show_payment_details_window(astrologer, amount, duration, payment_method_enum, package_window, method_name)
        
        btn_frame = tk.Frame(content_frame, bg=HinduTheme.BG_SECONDARY)
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(btn_frame, text="✓ Continue to Payment", font=("Arial", 12, "bold"), 
                 bg=HinduTheme.GREEN, fg=HinduTheme.WHITE, activebackground=HinduTheme.GREEN_LIGHT,
                 activeforeground=HinduTheme.GOLD, command=process_payment, padx=30, pady=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancel", font=("Arial", 12, "bold"), bg=HinduTheme.CRIMSON, 
                 fg=HinduTheme.WHITE, activebackground=HinduTheme.CRIMSON_LIGHT,
                 command=package_window.destroy, padx=30, pady=15).pack(side=tk.LEFT, padx=5)
    
    def show_payment_details_window(self, astrologer, amount, duration, payment_method, parent_window, method_name=None):
        """Show payment details input window - Hindu theme"""
        details_window = tk.Toplevel(self.root)
        details_window.title("💳 Payment Details - Divine Transaction 💳")
        details_window.geometry("550x700")
        details_window.configure(bg=HinduTheme.BG_PRIMARY)
        
        # Header
        header_label = tk.Label(
            details_window,
            text=f"{HinduThemeGuide.SYMBOLS['om']} Secure Payment Gateway {HinduThemeGuide.SYMBOLS['om']}",
            font=("Arial", 12, "bold"),
            fg=HinduTheme.WHITE,
            bg=HinduTheme.SAFFRON,
            pady=10
        )
        header_label.pack(fill=tk.X)
        
        content_frame = tk.Frame(details_window, bg=HinduTheme.BG_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Summary with Hindu theme
        summary_frame = tk.Frame(content_frame, bg=HinduTheme.LIGHT_GOLD, relief=tk.RAISED, bd=2)
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        display_method = method_name if method_name else payment_method.value.replace('_', ' ').title()
        summary_text = f"""
💁 Astrologer: {astrologer['name']}
⏱️ Duration: {duration} minutes
💰 Amount: ₨{amount}
💳 Payment Method: {display_method}
        """
        
        tk.Label(summary_frame, text=summary_text, font=("Arial", 11, "bold"), 
                justify=tk.LEFT, bg=HinduTheme.LIGHT_GOLD, fg=HinduTheme.NAVY, padx=15, pady=15).pack(anchor="w")
        
        # Payment fields based on method
        if method_name and "Khalti" in method_name:
            # Khalti Payment for Nepal - Hindu theme
            notice_label = tk.Label(
                content_frame, 
                text="⚠️ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg=HinduTheme.WHITE,
                bg=HinduTheme.CRIMSON
            )
            notice_label.pack(pady=(0, 15), padx=10, fill=tk.X)
            
            tk.Label(content_frame, text="📱 Khalti Phone Number:", font=("Arial", 11, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w", pady=(0, 5))
            khalti_entry = tk.Entry(content_frame, font=("Arial", 11), width=40)
            khalti_entry.pack(fill=tk.X, pady=(0, 10))
            khalti_entry.insert(0, "+977-")
            
            info_label = tk.Label(content_frame, text="(Nepali phone: 98/97XXXXXXXX)", font=("Arial", 9, "italic"), fg=HinduTheme.GOLD, bg=HinduTheme.BG_PRIMARY)
            info_label.pack(anchor="w", pady=(0, 20))
            
            def complete_payment():
                phone = khalti_entry.get().strip()
                if not phone:
                    messagebox.showerror("Payment Required", "Please enter Khalti phone number. Payment is required to proceed.")
                    return
                
                # Process Khalti payment
                from country_payment_gateway import CountryPaymentGateway
                success, message = CountryPaymentGateway.process_payment(
                    country="nepal",
                    payment_provider="khalti",
                    amount=amount,
                    transaction_id=f"TXN_{self.current_user}_{int(__import__('time').time())}",
                    phone_number=phone
                )
                
                if success:
                    self.process_successful_payment(astrologer, amount, duration, payment_method, "Khalti")
                    details_window.destroy()
                    parent_window.destroy()
                else:
                    messagebox.showerror("Payment Failed", f"Payment could not be processed. Call will NOT be initiated.\n\nReason: {message}")
        
        elif method_name and "Esewa" in method_name:
            # Esewa Payment for Nepal - Hindu theme
            notice_label = tk.Label(
                content_frame, 
                text="⚠️ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg=HinduTheme.WHITE,
                bg=HinduTheme.CRIMSON
            )
            notice_label.pack(pady=(0, 15), padx=10, fill=tk.X)
            
            tk.Label(content_frame, text="📧 Esewa Email:", font=("Arial", 11, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w", pady=(0, 5))
            esewa_entry = tk.Entry(content_frame, font=("Arial", 11), width=40)
            esewa_entry.pack(fill=tk.X, pady=(0, 20))
            esewa_entry.insert(0, "user@example.com")
            
            def complete_payment():
                email = esewa_entry.get().strip()
                if not email:
                    messagebox.showerror("Payment Required", "Please enter Esewa email. Payment is required to proceed.")
                    return
                
                # Process Esewa payment
                from country_payment_gateway import CountryPaymentGateway
                success, message = CountryPaymentGateway.process_payment(
                    country="nepal",
                    payment_provider="esewa",
                    amount=amount,
                    transaction_id=f"TXN_{self.current_user}_{int(__import__('time').time())}",
                    email=email
                )
                
                if success:
                    self.process_successful_payment(astrologer, amount, duration, payment_method, "Esewa")
                    details_window.destroy()
                    parent_window.destroy()
                else:
                    messagebox.showerror("Payment Failed", f"Payment could not be processed. Call will NOT be initiated.\n\nReason: {message}")
        
        elif method_name and "Razorpay" in method_name:
            # Razorpay Payment for India - Hindu theme
            notice_label = tk.Label(
                content_frame, 
                text="⚠️ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg=HinduTheme.WHITE,
                bg=HinduTheme.CRIMSON
            )
            notice_label.pack(pady=(0, 15), padx=10, fill=tk.X)
            
            # Payment method selection
            tk.Label(content_frame, text="Select Payment Method:", font=("Arial", 11, "bold"), fg=HinduTheme.NAVY, bg=HinduTheme.BG_PRIMARY).pack(anchor="w", pady=(0, 10))
            
            razorpay_method = tk.StringVar(value="upi")
            tk.Radiobutton(content_frame, text="💳 UPI", variable=razorpay_method, value="upi", 
                          font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", padx=20)
            tk.Radiobutton(content_frame, text="📱 Phone", variable=razorpay_method, value="phone", 
                          font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", padx=20, pady=(0, 15))
            
            tk.Label(content_frame, text="Payment Details:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(10, 5))
            razorpay_entry = tk.Entry(content_frame, font=("Arial", 11), width=40)
            razorpay_entry.pack(fill=tk.X, pady=(0, 10))
            razorpay_entry.insert(0, "user@bank")
            
            info_label = tk.Label(content_frame, text="(UPI format: user@bank or Phone: +91-XXXXXXXXXX)", 
                                 font=("Arial", 9, "italic"), fg="#666666", bg="#f0f0f0")
            info_label.pack(anchor="w", pady=(0, 20))
            
            def complete_payment():
                method = razorpay_method.get()
                details = razorpay_entry.get().strip()
                
                if not details:
                    messagebox.showerror("Payment Required", "Please enter payment details. Payment is required to proceed.")
                    return
                
                # Process Razorpay payment
                from country_payment_gateway import CountryPaymentGateway
                kwargs = {
                    'payment_method': method,
                    'phone_number': details if method == 'phone' else None,
                    'upi_id': details if method == 'upi' else None
                }
                
                success, message = CountryPaymentGateway.process_payment(
                    country="india",
                    payment_provider="razorpay",
                    amount=amount,
                    transaction_id=f"TXN_{self.current_user}_{int(__import__('time').time())}",
                    **kwargs
                )
                
                if success:
                    self.process_successful_payment(astrologer, amount, duration, payment_method, "Razorpay")
                    details_window.destroy()
                    parent_window.destroy()
                else:
                    messagebox.showerror("Payment Failed", f"Payment could not be processed. Call will NOT be initiated.\n\nReason: {message}")
        
        elif payment_method == PaymentMethod.CREDIT_CARD or payment_method == PaymentMethod.DEBIT_CARD:
            # Add payment requirement notice
            notice_label = tk.Label(
                content_frame, 
                text="⚠ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg="#f44336",
                bg="#f0f0f0"
            )
            notice_label.pack(pady=(0, 15))
            
            tk.Label(content_frame, text="Card Number:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
            card_entry = tk.Entry(content_frame, font=("Arial", 11), width=40, show="*")
            card_entry.pack(fill=tk.X, pady=(0, 15))
            
            tk.Label(content_frame, text="Expiry (MM/YY):", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
            expiry_entry = tk.Entry(content_frame, font=("Arial", 11), width=20)
            expiry_entry.pack(anchor="w", pady=(0, 15))
            
            tk.Label(content_frame, text="CVV:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
            cvv_entry = tk.Entry(content_frame, font=("Arial", 11), width=10, show="*")
            cvv_entry.pack(anchor="w", pady=(0, 20))
            
            def complete_payment():
                card_number = card_entry.get().strip()
                expiry = expiry_entry.get().strip()
                cvv = cvv_entry.get().strip()
                
                if not card_number or not expiry or not cvv:
                    messagebox.showerror("Payment Required", "Please fill all fields. Payment is required to proceed.")
                    return
                
                parts = expiry.split('/')
                if len(parts) != 2:
                    messagebox.showerror("Invalid Payment Info", "Expiry must be in MM/YY format")
                    return
                
                success, message = PaymentGateway.process_credit_card(
                    card_number, parts[0], parts[1], cvv, amount
                )
                
                if success:
                    self.process_successful_payment(astrologer, amount, duration, payment_method)
                    details_window.destroy()
                    parent_window.destroy()
                else:
                    messagebox.showerror("Payment Failed", f"Payment could not be processed. Call will NOT be initiated.\n\nReason: {message}")
        
        elif payment_method == PaymentMethod.UPI:
            notice_label = tk.Label(
                content_frame, 
                text="⚠ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg="#f44336",
                bg="#f0f0f0"
            )
            notice_label.pack(pady=(0, 15))
            
            tk.Label(content_frame, text="UPI ID:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
            upi_entry = tk.Entry(content_frame, font=("Arial", 11), width=40)
            upi_entry.pack(fill=tk.X, pady=(0, 20))
            upi_entry.insert(0, "example@upi")
            
            def complete_payment():
                upi_id = upi_entry.get().strip()
                if not upi_id:
                    messagebox.showerror("Payment Required", "Please enter UPI ID. Payment is required to proceed.")
                    return
                
                success, message = PaymentGateway.process_upi_payment(upi_id, amount)
                if success:
                    self.process_successful_payment(astrologer, amount, duration, payment_method)
                    details_window.destroy()
                    parent_window.destroy()
                else:
                    messagebox.showerror("Payment Failed", f"Payment could not be processed. Call will NOT be initiated.\n\nReason: {message}")
        
        elif payment_method == PaymentMethod.PAYPAL:
            notice_label = tk.Label(
                content_frame, 
                text="⚠ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg="#f44336",
                bg="#f0f0f0"
            )
            notice_label.pack(pady=(0, 15))
            
            tk.Label(content_frame, text="PayPal Email:", font=("Arial", 11), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
            paypal_entry = tk.Entry(content_frame, font=("Arial", 11), width=40)
            paypal_entry.pack(fill=tk.X, pady=(0, 20))
            
            def complete_payment():
                paypal_email = paypal_entry.get().strip()
                if not paypal_email:
                    messagebox.showerror("Payment Required", "Please enter PayPal email. Payment is required to proceed.")
                    return
                
                success, message = PaymentGateway.process_paypal_payment(paypal_email, amount)
                if success:
                    self.process_successful_payment(astrologer, amount, duration, payment_method)
                    details_window.destroy()
                    parent_window.destroy()
                else:
                    messagebox.showerror("Payment Failed", f"Payment could not be processed. Call will NOT be initiated.\n\nReason: {message}")
        
        elif payment_method == PaymentMethod.WALLET:
            notice_label = tk.Label(
                content_frame, 
                text="⚠ PAYMENT IS MANDATORY TO PROCEED WITH CALL",
                font=("Arial", 10, "bold"),
                fg="#f44336",
                bg="#f0f0f0"
            )
            notice_label.pack(pady=(0, 15))
            
            balance = self.payment_system.get_wallet_balance(self.current_user)
            tk.Label(content_frame, text=f"Wallet Balance: ₨{balance}", 
                    font=("Arial", 12, "bold"), fg="#4caf50", bg="#f0f0f0").pack(pady=20)
            
            if balance < amount:
                tk.Label(content_frame, text=f"Insufficient balance! Need ₨{amount - balance} more", 
                        font=("Arial", 11), fg="#f44336", bg="#f0f0f0").pack(pady=10)
            
            def complete_payment():
                balance = self.payment_system.get_wallet_balance(self.current_user)
                if balance < amount:
                    messagebox.showerror("Payment Failed", f"Insufficient wallet balance. Call will NOT be initiated.\n\nNeed: ₨{amount}\nAvailable: ₨{balance}")
                    return
                
                self.process_successful_payment(astrologer, amount, duration, payment_method)
                details_window.destroy()
                parent_window.destroy()
        
        # Buttons
        btn_frame = ttk.Frame(content_frame)
        btn_frame = tk.Frame(details_window, bg=HinduTheme.BG_PRIMARY)
        btn_frame.pack(fill=tk.X, pady=(20, 15), padx=20)
        
        tk.Button(btn_frame, text="💳 Complete Payment & Call", font=("Arial", 12, "bold"), 
                 bg=HinduTheme.GREEN, fg=HinduTheme.WHITE, activebackground=HinduTheme.GREEN_LIGHT, 
                 activeforeground=HinduTheme.GOLD, command=complete_payment, padx=30, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel (No Call)", font=("Arial", 12, "bold"), 
                 bg=HinduTheme.CRIMSON, fg=HinduTheme.WHITE, activebackground=HinduTheme.CRIMSON_LIGHT,
                 command=details_window.destroy, padx=30, pady=10).pack(side=tk.LEFT, padx=5)
    
    def process_successful_payment(self, astrologer, amount, duration, payment_method, provider_name=None):
        """Process payment and initiate call ONLY on successful payment"""
        user_region = self.user_manager.get_user_region(self.current_user)
        
        transaction = self.payment_system.create_transaction(
            self.current_user,
            astrologer['name'],
            amount,
            payment_method,
            duration,
            country=user_region,
            payment_provider=provider_name.lower() if provider_name else None
        )
        
        success, message = self.payment_system.process_payment(transaction)
        
        if success:
            # Verify transaction was completed
            if transaction.status.value != 'completed':
                messagebox.showerror("Payment Verification Failed", 
                                    "Payment transaction did not complete successfully.\nCall cannot be initiated.")
                return
            
            # Show receipt
            provider_display = provider_name if provider_name else payment_method.value.replace('_', ' ').title()
            receipt = PaymentGateway.generate_receipt(
                transaction.transaction_id,
                self.current_user,
                astrologer['name'],
                amount,
                provider_display,
                transaction.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            )
            
            messagebox.showinfo("Payment Successful", 
                              f"✓ Payment processed successfully via {provider_display}!\n\n{receipt}")
            
            # Log call - ONLY after payment is confirmed
            log_call_history(astrologer['name'], astrologer['phone'])
            
            # Start actual call with timer - ONLY after payment
            self.start_actual_call(astrologer, duration, transaction.transaction_id, is_free=False)
        else:
            messagebox.showerror("Payment Failed - Call Cancelled", 
                                f"Payment could not be processed.\nCall will NOT be initiated.\n\nReason: {message}")
    
    def show_wallet_window(self):
        """Show wallet management window"""
        wallet_window = tk.Toplevel(self.root)
        wallet_window.title("Wallet Management")
        wallet_window.geometry("500x400")
        wallet_window.configure(bg="#f0f0f0")
        
        content_frame = ttk.Frame(wallet_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        if not self.current_user:
            tk.Label(content_frame, text="Please login first", 
                    font=("Arial", 12), fg="#f44336", bg="#f0f0f0").pack(pady=20)
            return
        
        # Current balance
        balance = self.payment_system.get_wallet_balance(self.current_user)
        balance_label = tk.Label(content_frame, text=f"Current Balance: ₨{balance}", 
                                font=("Arial", 16, "bold"), fg="#4caf50", bg="#f0f0f0")
        balance_label.pack(pady=20)
        
        # Add money
        tk.Label(content_frame, text="Add Money to Wallet:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 10))
        
        amount_frame = ttk.Frame(content_frame)
        amount_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(amount_frame, text="Amount (₨):", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 10))
        amount_entry = tk.Entry(amount_frame, font=("Arial", 11), width=15)
        amount_entry.pack(side=tk.LEFT)
        
        def add_money():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0")
                    return
                
                success, msg = self.payment_system.add_to_wallet(self.current_user, amount)
                if success:
                    messagebox.showinfo("Success", msg)
                    new_balance = self.payment_system.get_wallet_balance(self.current_user)
                    balance_label.config(text=f"Current Balance: ₹{new_balance}")
                    amount_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        tk.Button(amount_frame, text="Add", font=("Arial", 11, "bold"), 
                 bg="#2196f3", fg="white", command=add_money, padx=20, pady=8).pack(side=tk.LEFT, padx=10)
        
        # Quick add buttons
        tk.Label(content_frame, text="Quick Add:", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(20, 10))
        
        quick_frame = ttk.Frame(content_frame)
        quick_frame.pack(fill=tk.X)
        
        for amount_val in [100, 500, 1000, 2000]:
            tk.Button(quick_frame, text=f"₨{amount_val}", font=("Arial", 10), 
                     bg="#ff9800", fg="white", command=lambda a=amount_val: (
                         self.payment_system.add_to_wallet(self.current_user, a),
                         balance_label.config(text=f"Current Balance: ₨{self.payment_system.get_wallet_balance(self.current_user)}")
                     ),
                     padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    def start_actual_call(self, astrologer, duration_minutes, transaction_id, is_free=False):
        """Start an online call with real-time timer and astrologer photo"""
        # Create call ID
        call_id = str(uuid.uuid4())
        
        # Start call in call manager
        call_data = self.call_manager.start_call(
            call_id,
            self.current_user,
            astrologer['name'],
            astrologer['phone'],
            duration_minutes
        )
        
        # Create call window
        call_window = tk.Toplevel(self.root)
        call_window.title(f"ONLINE CALL - {astrologer['name']}")
        call_window.geometry("1000x700")
        call_window.configure(bg="#1a1a1a")
        self.active_call_window = call_window
        
        # Create main content frame with two columns
        main_frame = ttk.Frame(call_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT SIDE - Astrologer Video/Photo Display
        video_frame = tk.Frame(main_frame, bg="#000000", relief=tk.RAISED, bd=2)
        video_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Load and display astrologer image
        img = load_image(astrologer["image_url"], size=(400, 550))
        photo = ImageTk.PhotoImage(img)
        self.photo_images.append(photo)
        
        video_label = tk.Label(video_frame, image=photo, bg="#000000")
        video_label.pack(pady=10, padx=10)
        
        # Astrologer name on video
        name_on_video = tk.Label(video_frame, text=f"{astrologer['name']}", 
                                font=("Arial", 14, "bold"), fg="#4caf50", bg="#000000")
        name_on_video.pack(side=tk.BOTTOM, pady=10)
        
        # RIGHT SIDE - Call Controls and Info
        control_frame = tk.Frame(main_frame, bg="#f0f0f0", relief=tk.RAISED, bd=2)
        control_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        content_frame = ttk.Frame(control_frame, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Call header
        header = tk.Label(content_frame, text=f"ONLINE CALL ACTIVE", 
                         font=("Arial", 16, "bold"), fg="#4caf50", bg="#f0f0f0")
        header.pack(pady=(0, 20))
        
        # Astrologer info box
        info_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = f"""
Astrologer: {astrologer['name']}
Phone: {astrologer['phone']}
Specialization: {astrologer['specialization']}
Experience: {astrologer['experience']}
Status: 🟢 Connected
        """
        
        tk.Label(info_frame, text=info_text, font=("Arial", 10), justify=tk.LEFT, 
                bg="white", padx=15, pady=15, fg="#333333").pack(anchor="w")
        
        # Timer display
        timer_label = tk.Label(content_frame, text="00:00", 
                              font=("Arial", 42, "bold"), fg="#4caf50", bg="#f0f0f0")
        timer_label.pack(pady=20)
        
        # Duration info
        duration_info = tk.Label(content_frame, 
                                text=f"Duration: {duration_minutes} min | Payment: {'FREE' if is_free else f'₨0'}", 
                                font=("Arial", 9), fg="#666666", bg="#f0f0f0")
        duration_info.pack(pady=5)
        
        # Progress bar for call duration
        progress = ttk.Progressbar(content_frame, length=300, mode='determinate', maximum=100)
        progress.pack(pady=15, fill=tk.X)
        
        # Status label
        status_label = tk.Label(content_frame, text="📞 Call in progress...", 
                               font=("Arial", 11, "bold"), fg="#2196f3", bg="#f0f0f0")
        status_label.pack(pady=10)
        
        # Quality indicator
        quality_label = tk.Label(content_frame, text="📶 Network: Excellent", 
                                font=("Arial", 10), fg="#4caf50", bg="#f0f0f0")
        quality_label.pack(pady=5)
        
        # Button frame
        btn_frame = tk.Frame(content_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=20)
        
        # Mute/Unmute button
        mute_state = {"muted": False}
        
        def toggle_mute():
            mute_state["muted"] = not mute_state["muted"]
            mute_btn.config(text="🔊 Unmute" if mute_state["muted"] else "🔇 Mute",
                          bg="#ff9800" if mute_state["muted"] else "#2196f3")
        
        mute_btn = tk.Button(btn_frame, text="🔇 Mute", font=("Arial", 10, "bold"), 
                            bg="#2196f3", fg="white", command=toggle_mute, padx=20, pady=8)
        mute_btn.pack(side=tk.LEFT, padx=5)
        
        # Speaker button
        speaker_state = {"on": True}
        
        def toggle_speaker():
            speaker_state["on"] = not speaker_state["on"]
            speaker_btn.config(text="🔕 Speaker Off" if speaker_state["on"] else "🔉 Speaker On",
                             bg="#2196f3" if speaker_state["on"] else "#ff9800")
        
        speaker_btn = tk.Button(btn_frame, text="🔉 Speaker", font=("Arial", 10, "bold"), 
                               bg="#2196f3", fg="white", command=toggle_speaker, padx=20, pady=8)
        speaker_btn.pack(side=tk.LEFT, padx=5)
        
        # End call button
        def end_call():
            # End call in manager
            self.call_manager.end_call(call_id)
            
            # Show call summary
            call_data = self.call_manager.get_active_call(call_id)
            if call_data is None:
                # Call was already ended, get from history
                call_data = self.call_manager.call_history[-1] if self.call_manager.call_history else None
            
            if call_data:
                summary = f"""
CALL SUMMARY

Astrologer: {astrologer['name']}
Duration: {call_data.get('actual_duration_minutes', duration_minutes)} minutes
Amount Paid: {'₨0 (FREE)' if is_free else '₨0'}
Status: Call Ended ✓
Thank you for using our service!
                """
                messagebox.showinfo("Call Ended", summary)
            
            call_window.destroy()
            self.active_call_window = None
        
        end_btn = tk.Button(btn_frame, text="📞 End Call", font=("Arial", 11, "bold"), 
                           bg="#f44336", fg="white", command=end_call, padx=30, pady=10)
        end_btn.pack(side=tk.LEFT, padx=5)
        
        # Update timer in background
        def update_timer():
            while self.call_manager.is_call_active(call_id):
                if call_window.winfo_exists():
                    elapsed = self.call_manager.get_call_elapsed_time(call_id)
                    remaining = self.call_manager.get_call_time_remaining(call_id)
                    
                    # Format time
                    elapsed_str = self.call_manager.format_time(elapsed)
                    remaining_str = self.call_manager.format_time(remaining)
                    
                    # Update timer display using after() for thread-safe UI updates
                    def update_ui():
                        if call_window.winfo_exists():
                            timer_label.config(text=elapsed_str)
                            duration_info.config(text=f"Duration: {duration_minutes} min | Elapsed: {elapsed_str} | Remaining: {remaining_str}")
                            
                            # Update progress
                            progress_value = (elapsed / (duration_minutes * 60)) * 100
                            progress['value'] = min(100, progress_value)
                            
                            # Update status and quality dynamically
                            if remaining <= 60 and remaining > 0:
                                status_label.config(text="⚠️ Call ending soon...", fg="#ff9800")
                                quality_label.config(text="📶 Network: Good", fg="#ff9800")
                            elif remaining <= 0:
                                status_label.config(text="⏱ Time's up! Call ended automatically.", fg="#f44336")
                                quality_label.config(text="📶 Network: Unstable", fg="#f44336")
                                # Auto-end the call
                                call_window.after(500, end_call)
                    
                    call_window.after(0, update_ui)
                    time.sleep(1)
                else:
                    break
        
        # Start timer thread
        timer_thread = threading.Thread(target=update_timer, daemon=True)
        timer_thread.start()
    
    def show_history_window(self):
        """Show transaction history"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        history_window.geometry("800x500")
        history_window.configure(bg="#f0f0f0")
        
        content_frame = ttk.Frame(history_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        if not self.current_user:
            tk.Label(content_frame, text="Please login first", 
                    font=("Arial", 12), fg="#f44336", bg="#f0f0f0").pack(pady=20)
            return
        
        # Get history
        history = self.payment_system.get_transaction_history(self.current_user)
        
        if not history:
            tk.Label(content_frame, text="No transactions yet", 
                    font=("Arial", 12), fg="#999999", bg="#f0f0f0").pack(pady=20)
            return
        
        # Create treeview
        tree = ttk.Treeview(content_frame, columns=("Date", "Astrologer", "Amount", "Status", "Duration"), height=20)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tree.column("#0", width=150, minwidth=150, anchor=tk.W)
        tree.column("Date", width=150, minwidth=150)
        tree.column("Astrologer", width=150, minwidth=150)
        tree.column("Amount", width=100, minwidth=100)
        tree.column("Status", width=100, minwidth=100)
        tree.column("Duration", width=100, minwidth=100)
        
        tree.heading("#0", text="Transaction ID", anchor=tk.W)
        tree.heading("Date", text="Date", anchor=tk.W)
        tree.heading("Astrologer", text="Astrologer", anchor=tk.W)
        tree.heading("Amount", text="Amount", anchor=tk.W)
        tree.heading("Status", text="Status", anchor=tk.W)
        tree.heading("Duration", text="Duration", anchor=tk.W)
        
        for i, txn in enumerate(history):
            tree.insert("", "end", text=txn['transaction_id'],
                       values=(txn['timestamp'][:10], txn['astrologer_name'], 
                              f"₨{txn['amount']}", txn['status'], f"{txn['call_duration']}min"))



def main():
    """Main entry point"""
    root = tk.Tk()
    app = AstrologerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

