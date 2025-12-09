"""
Enhanced Tkinter GUI Client - Real Backend Integration
Connects to the Astrology Consultation Platform Backend
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import tkinter.font as tkFont
import requests
import json
from datetime import datetime
import threading
import websocket
from typing import Optional

# Backend Configuration
API_URL = "http://localhost:8000/api"
WS_URL = "ws://localhost:8000/ws"


class AstrologyClientApp:
    """Enhanced Astrology Consultation Client"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cosmos Astrology - Real-Time Consultations")
        self.root.geometry("1000x700")
        
        # Authentication
        self.auth_token = None
        self.current_user = None
        self.questions = []
        self.current_question = None
        self.ws = None
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Show login screen initially
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ==================== Login Screen ====================
    
    def show_login_screen(self):
        """Display login/registration screen"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        center_frame = tk.Frame(main_frame, bg="white")
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)
        
        # Title
        title_label = tk.Label(
            center_frame,
            text="Cosmos Astrology",
            font=("Georgia", 28, "bold"),
            bg="white",
            fg="#8B008B"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(
            center_frame,
            text="Real-Time Consultation Platform",
            font=("Georgia", 12),
            bg="white",
            fg="#666"
        )
        subtitle.pack()
        
        # Notebook for tabs
        notebook = ttk.Notebook(center_frame)
        notebook.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Login Tab
        login_frame = tk.Frame(notebook, bg="white")
        notebook.add(login_frame, text="Login")
        
        tk.Label(login_frame, text="Username:", bg="white").pack(pady=5)
        username_entry = tk.Entry(login_frame, width=40)
        username_entry.pack(pady=5)
        
        tk.Label(login_frame, text="Password:", bg="white").pack(pady=5)
        password_entry = tk.Entry(login_frame, width=40, show="*")
        password_entry.pack(pady=5)
        
        login_btn = tk.Button(
            login_frame,
            text="Login",
            font=("Helvetica", 12, "bold"),
            bg="#8B008B",
            fg="white",
            command=lambda: self.handle_login(username_entry.get(), password_entry.get())
        )
        login_btn.pack(pady=20)
        
        # Register Tab
        register_frame = tk.Frame(notebook, bg="white")
        notebook.add(register_frame, text="Register")
        
        tk.Label(register_frame, text="Username:", bg="white").pack(pady=5)
        reg_username = tk.Entry(register_frame, width=40)
        reg_username.pack(pady=5)
        
        tk.Label(register_frame, text="Email:", bg="white").pack(pady=5)
        reg_email = tk.Entry(register_frame, width=40)
        reg_email.pack(pady=5)
        
        tk.Label(register_frame, text="Full Name:", bg="white").pack(pady=5)
        reg_fullname = tk.Entry(register_frame, width=40)
        reg_fullname.pack(pady=5)
        
        tk.Label(register_frame, text="Password:", bg="white").pack(pady=5)
        reg_password = tk.Entry(register_frame, width=40, show="*")
        reg_password.pack(pady=5)
        
        register_btn = tk.Button(
            register_frame,
            text="Register",
            font=("Helvetica", 12, "bold"),
            bg="#20B2AA",
            fg="white",
            command=lambda: self.handle_register(
                reg_username.get(), reg_email.get(), 
                reg_fullname.get(), reg_password.get()
            )
        )
        register_btn.pack(pady=20)
    
    def handle_login(self, username: str, password: str):
        """Handle login request"""
        if not username or not password:
            messagebox.showwarning("Validation", "Please enter username and password")
            return
        
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data['access_token']
                self.current_user = data.get('user')
                
                # Save token to local storage (file-based for Tkinter)
                with open('.auth_token', 'w') as f:
                    f.write(self.auth_token)
                
                self.show_main_screen()
            else:
                error = response.json().get('detail', 'Login failed')
                messagebox.showerror("Login Error", error)
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", "Cannot connect to backend. Is the server running?")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def handle_register(self, username: str, email: str, fullname: str, password: str):
        """Handle registration request"""
        if not all([username, email, password]):
            messagebox.showwarning("Validation", "Please fill all required fields")
            return
        
        try:
            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "full_name": fullname,
                    "password": password
                },
                timeout=10
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Registration successful! Please login.")
            else:
                error = response.json().get('detail', 'Registration failed')
                messagebox.showerror("Registration Error", error)
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Connection Error", "Cannot connect to backend")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== Main Screen ====================
    
    def show_main_screen(self):
        """Display main consultation interface"""
        self.clear_window()
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="My Profile", command=self.show_profile)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Cosmos Astrology v1.0"))
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main_frame, bg="white")
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header,
            text=f"Welcome, {self.current_user.get('full_name', self.current_user['username'])}",
            font=("Georgia", 18, "bold"),
            bg="white",
            fg="#8B008B"
        ).pack(anchor="w", padx=15, pady=10)
        
        # Notebook for views
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Ask Question Tab
        ask_frame = tk.Frame(notebook)
        notebook.add(ask_frame, text="Ask a Question")
        self.create_ask_question_tab(ask_frame)
        
        # My Questions Tab
        my_q_frame = tk.Frame(notebook)
        notebook.add(my_q_frame, text="My Questions")
        self.create_my_questions_tab(my_q_frame)
        
        # Find Astrologers Tab
        astro_frame = tk.Frame(notebook)
        notebook.add(astro_frame, text="Find Astrologers")
        self.create_astrologers_tab(astro_frame)
    
    def create_ask_question_tab(self, parent):
        """Create tab for asking new questions"""
        tk.Label(parent, text="Ask an Astrological Question", font=("Georgia", 16, "bold")).pack(pady=10)
        
        # Category
        tk.Label(parent, text="Category:").pack(anchor="w", padx=20)
        category_var = tk.StringVar()
        categories = ["Marriage", "Everyday Life", "Education", "Work", "Money", "Self"]
        category_combo = ttk.Combobox(parent, textvariable=category_var, values=categories, width=50)
        category_combo.pack(padx=20, pady=5)
        
        # Title
        tk.Label(parent, text="Question Title:").pack(anchor="w", padx=20, pady=(10, 0))
        title_entry = tk.Entry(parent, width=70)
        title_entry.pack(padx=20, pady=5)
        
        # Description
        tk.Label(parent, text="Description:").pack(anchor="w", padx=20, pady=(10, 0))
        desc_text = tk.Text(parent, width=70, height=6)
        desc_text.pack(padx=20, pady=5)
        
        # Birth Info
        info_frame = tk.Frame(parent)
        info_frame.pack(padx=20, pady=10, fill=tk.X)
        
        tk.Label(info_frame, text="Birth Date (YYYY-MM-DD):").pack(side=tk.LEFT)
        birth_date = tk.Entry(info_frame, width=20)
        birth_date.pack(side=tk.LEFT, padx=10)
        
        tk.Label(info_frame, text="Birth Place:").pack(side=tk.LEFT)
        birth_place = tk.Entry(info_frame, width=20)
        birth_place.pack(side=tk.LEFT, padx=10)
        
        # Submit button
        submit_btn = tk.Button(
            parent,
            text="Submit Question",
            font=("Helvetica", 12, "bold"),
            bg="#8B008B",
            fg="white",
            command=lambda: self.submit_question(
                category_var.get(),
                title_entry.get(),
                desc_text.get("1.0", tk.END),
                birth_date.get(),
                birth_place.get()
            )
        )
        submit_btn.pack(pady=20)
    
    def create_my_questions_tab(self, parent):
        """Create tab for user's questions"""
        # Buttons frame
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_btn = tk.Button(
            btn_frame,
            text="Refresh",
            bg="#20B2AA",
            fg="white",
            command=self.load_user_questions
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Questions list with scrollbar
        list_frame = tk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.questions_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.questions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.questions_listbox.bind("<<ListboxSelect>>", self.on_question_select)
        scrollbar.config(command=self.questions_listbox.yview)
        
        # Details frame
        details_frame = tk.LabelFrame(parent, text="Question Details", padx=10, pady=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.question_details = tk.Text(details_frame, height=8, width=80)
        self.question_details.pack(fill=tk.BOTH, expand=True)
        self.question_details.config(state=tk.DISABLED)
        
        # Chat area
        chat_frame = tk.LabelFrame(parent, text="Messages", padx=10, pady=10)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = tk.Text(chat_frame, height=5, width=80)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Message input
        input_frame = tk.Frame(parent)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.message_input = tk.Entry(input_frame, width=70)
        self.message_input.pack(side=tk.LEFT, padx=5)
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            bg="#8B008B",
            fg="white",
            command=self.send_message
        )
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Load questions
        self.load_user_questions()
    
    def create_astrologers_tab(self, parent):
        """Create tab for finding astrologers"""
        tk.Label(parent, text="Find Experienced Astrologers", font=("Georgia", 14, "bold")).pack(pady=10)
        
        # Filter
        filter_frame = tk.Frame(parent)
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(filter_frame, text="Specialization:").pack(side=tk.LEFT)
        spec_var = tk.StringVar()
        spec_combo = ttk.Combobox(
            filter_frame,
            textvariable=spec_var,
            values=["All", "Vedic Astrology", "Love & Relationships", "Career", "Finance", "Health"]
        )
        spec_combo.pack(side=tk.LEFT, padx=10)
        
        search_btn = tk.Button(
            filter_frame,
            text="Search",
            bg="#20B2AA",
            fg="white",
            command=lambda: self.load_astrologers(spec_var.get())
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Astrologers list
        list_frame = tk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.astrologers_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.astrologers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.astrologers_listbox.yview)
        
        # Load astrologers
        self.load_astrologers()
    
    def submit_question(self, category: str, title: str, description: str, birth_date: str, birth_place: str):
        """Submit a new question to the backend"""
        if not category or not title:
            messagebox.showwarning("Validation", "Please fill category and title")
            return
        
        try:
            payload = {
                "category": category,
                "title": title,
                "description": description.strip(),
                "is_public": True
            }
            
            if birth_date:
                payload["birth_date"] = birth_date
            if birth_place:
                payload["birth_place"] = birth_place
            
            response = requests.post(
                f"{API_URL}/questions",
                json=payload,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Question submitted! An astrologer will respond soon.")
                # Clear form
                # (would need references to widgets)
            else:
                error = response.json().get('detail', 'Failed to submit')
                messagebox.showerror("Error", error)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_user_questions(self):
        """Load user's questions from backend"""
        try:
            response = requests.get(
                f"{API_URL}/questions",
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.questions = data.get('items', [])
                
                self.questions_listbox.delete(0, tk.END)
                for q in self.questions:
                    status = q.get('status', 'pending').upper()
                    self.questions_listbox.insert(
                        tk.END,
                        f"{q['title']} [{status}]"
                    )
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {str(e)}")
    
    def on_question_select(self, event):
        """Handle question selection"""
        selection = self.questions_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        self.current_question = self.questions[idx]
        
        # Display details
        self.question_details.config(state=tk.NORMAL)
        self.question_details.delete("1.0", tk.END)
        
        details = f"""
        Title: {self.current_question['title']}
        Category: {self.current_question['category']}
        Status: {self.current_question['status']}
        Created: {self.current_question['created_at']}
        
        Description:
        {self.current_question.get('description', 'N/A')}
        """
        
        self.question_details.insert("1.0", details)
        self.question_details.config(state=tk.DISABLED)
        
        # Load chat messages
        self.load_messages()
    
    def load_messages(self):
        """Load messages for current question"""
        if not self.current_question:
            return
        
        try:
            response = requests.get(
                f"{API_URL}/questions/{self.current_question['id']}",
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                question = response.json()
                
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.delete("1.0", tk.END)
                
                for msg in question.get('messages', []):
                    sender = "You" if msg.get('user_id') == self.current_user['id'] else "Astrologer"
                    self.chat_display.insert(
                        tk.END,
                        f"[{sender}] {msg['content']}\n\n"
                    )
                
                self.chat_display.config(state=tk.DISABLED)
        
        except Exception as e:
            print(f"Error loading messages: {e}")
    
    def send_message(self):
        """Send a message in current question thread"""
        if not self.current_question:
            messagebox.showwarning("Error", "Please select a question first")
            return
        
        content = self.message_input.get().strip()
        if not content:
            return
        
        try:
            response = requests.post(
                f"{API_URL}/questions/{self.current_question['id']}/messages",
                json={"content": content, "message_type": "follow_up"},
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                self.message_input.delete(0, tk.END)
                self.load_messages()
            else:
                messagebox.showerror("Error", "Failed to send message")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_astrologers(self, specialization: str = None):
        """Load available astrologers"""
        try:
            params = {}
            if specialization and specialization != "All":
                params["specialization"] = specialization
            
            response = requests.get(
                f"{API_URL}/astrologers",
                params=params,
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                astrologers = response.json()
                
                self.astrologers_listbox.delete(0, tk.END)
                for ast in astrologers:
                    info = f"{ast['full_name']} | {ast['specialization']} | Rating: {ast['average_rating']}/5"
                    self.astrologers_listbox.insert(tk.END, info)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load astrologers: {str(e)}")
    
    def show_profile(self):
        """Show user profile"""
        profile_info = f"""
        Username: {self.current_user['username']}
        Email: {self.current_user['email']}
        Full Name: {self.current_user.get('full_name', 'N/A')}
        Role: {self.current_user['role']}
        Joined: {self.current_user['created_at']}
        """
        
        messagebox.showinfo("My Profile", profile_info)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_token = None
            self.current_user = None
            try:
                import os
                os.remove('.auth_token')
            except:
                pass
            self.show_login_screen()


def main():
    root = tk.Tk()
    app = AstrologyClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
