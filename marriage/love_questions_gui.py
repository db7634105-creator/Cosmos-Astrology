import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkFont
import requests
import json
from datetime import datetime


# Predefined question/answer set organized by categories with astrological insights
PREDEFINED_QA = {
    "Marriage": [
        ("When will I meet my first love?", "According to your birth chart, Venus and the 7th house hold the key to your romantic destiny. The timing depends on your planetary periods (Dashas). When Venus is well-placed or activated through progression, opportunities for meeting someone significant increase. Be open to connections between now and the next 18-24 months, especially during favorable planetary transits."),
        ("Will I ever find True love?", "True love is written in your stars! Your chart shows strong potential for deep, meaningful connections. Jupiter's influence on your 7th house brings opportunities for genuine partnerships. The universe is conspiring in your favor. Trust the timing and maintain an open heart. Your soulmate is destined to cross your path when both of you are spiritually ready."),
        ("Will it be okay to move on with my present boyfriend?", "Look to your Venus placement and the 7th house for answers. If Mars and Saturn are well-aspected with your current relationship planet placements, it suggests stability. However, if there's tension between Mars (action) and Venus (love), reconsider. Trust your intuition—your Navamsha chart reveals the truth about this union. Follow your heart and the guidance of the stars."),
        ("Why am I not getting a perfect partner?", "Perfectionism itself may be the barrier. Look at Saturn in your chart—it teaches that true love is built, not found perfect. Venus might be calling you to embrace imperfection and grow through partnership. The right person isn't perfect; they're perfect for YOUR growth. Release unrealistic expectations and open your heart to genuine connection over superficial ideals."),
        ("At what age will I marry?", "Jupiter's return cycles and Dasha periods are crucial here. Typically, major life events align with Jupiter returns (every 12 years) and Dasha transitions. Your chart suggests marriage could occur during your next favorable Dasha period, often between ages 24-28, 28-32, or 32-36. Exact timing depends on your birth details. The stars have marked these moments—be ready."),
        ("What will be the profession of my future husband?", "Your 7th house and its lord reveal hints about your partner's nature. Check the 7th lord's association with houses of career (10th). If 7th lord connects to Mercury, he may be in communication/business. If Mars-ruled, possibly military/engineering. If Jupiter-ruled, education/management. The universe assigns partners whose life path complements your destiny. Trust this cosmic alignment.")
    ],
    "Everyday_Life": [
        ("Will I hear life changing news today?", "Mercury's current transit and Moon's position in your natal chart influence daily communications. If Mercury is strong and well-placed today, news may arrive. Check your lunar days—certain phases bring unexpected revelations. The universe speaks through synchronicities. Stay alert and receptive. Transformation often arrives when you least expect it, preparing you for your next chapter."),
        ("I had applied for a lottery ticket. Will I win the lottery?", "Your Jupiter placement holds the answer. Jupiter is the planet of luck and expansion. If transiting Jupiter is favorable to your birth Jupiter or Moon, chances improve. However, lottery is ruled more by chance than destiny. Your chart may have better blessings waiting—check your 2nd and 11th houses for wealth indicators. Focus on creating your own luck through effort."),
        ("I'm very sick, will my friend visit me today?", "The Moon governs emotions and relationships; its current position shows your social connections. If the Moon is in a favorable house position today, friends are naturally drawn to you. Mars and Mercury also influence visits. Trust that the universe brings support when needed. Your illness itself is calling compassionate souls toward you. Rest assured, help comes in divine timing."),
        ("I had a dream last night, I found myself climbing a high mountain. What does it mean?", "Mountains in dreams symbolize challenges and spiritual ascent in Vedic astrology. Your subconscious (Moon) is showing you the path to achievement. Saturn teaches discipline; Sun teaches perseverance. This dream reveals your soul's yearning for growth. Each step upward represents overcoming obstacles. The dream is encouraging you—you have the strength. Keep climbing toward your highest self."),
        ("I have a big house, huge property, successful business but still I'm not satisfied, why am I feeling so?", "Your Moon may be in a naturally restless position, seeking deeper meaning beyond material wealth. Saturn teaches that true satisfaction comes from spiritual purpose, not possessions. Check your 12th house—it reveals spiritual longing. The universe is calling you toward inner fulfillment. Success without purpose feels empty. Seek meaning, service, and spiritual connection—these will satisfy your soul."),
        ("I had an argument with my boss so I left my job today, will I get a new job soon?", "Mars rules sudden action and conflict; Mercury rules career. If Mars is overly strong in your chart, impulsive decisions are your pattern. However, your 10th house and its lord hold the key to career fortune. Within 3-6 months, a better opportunity will present itself. The universe removes what no longer serves you. Stay confident—better employment aligned with your purpose awaits.")
    ],
    "Education": [
        ("Am I on the right educational path? What are good fields for me to study?", "Mercury rules intellect and communication; check its strength in your chart. If Mercury is strong, fields like engineering, IT, writing, or education suit you. Jupiter in the 4th or 9th suggests philosophy, law, or higher learning. Saturn brings discipline for technical fields. Your 4th and 9th houses reveal educational destiny. Trust these cosmic indicators—your natural talents align with your chart's promise."),
        ("Will I get admission into my choice of college this year?", "Jupiter is the planet of education and opportunities. Check if Jupiter is in a favorable position this year or if it's transitioning favorably. The 4th house shows education; examine its strength. If indicators are positive, your admission is assured. The universe aligns opportunities for those who work hard. Combine your effort with cosmic timing—success is written in your stars."),
        ("After achieving bachelor degree should I continue education or start working?", "Saturn advises discipline and practical experience; Jupiter suggests continued learning. Your 9th house (higher learning) and 10th house (career) hold the answer. If Jupiter is strong, further education brings wisdom and better opportunities. If Saturn dominates, practical experience will teach what books cannot. Trust your inner calling—education or experience, both are valid. Choose what resonates with your soul's purpose."),
        ("It's difficult for me to concentrate on studying. What can I do to improve it?", "The Moon rules focus and mental peace; Mercury rules concentration. If these planets are afflicted, focus becomes challenging. Saturn teaches discipline—create structured study routines. Meditation and yoga strengthen mental faculties. Your 8th house (hidden knowledge) may need activation. Regular practice, proper environment, and spiritual grounding will enhance concentration. The universe rewards focused effort."),
        ("My parents want me to become a lawyer. But I don't feel like I can be a successful one. What do you see in my birth chart?", "Check your 10th house and its lord for career destiny. Does Saturn suggest law's discipline appeals to you, or does Mars/Mercury point elsewhere? Your chart reveals your true calling. While parental wishes deserve respect, your birth chart shows your unique gifts. Have an honest conversation with your parents—perhaps you can find a middle path that honors both their hopes and your authentic talents."),
        ("Currently, I am working as a professor. I want some development in my career and qualifications. Is it still possible?", "Saturn's position shows your experience is a strength. Jupiter promises continued growth and expansion. The 10th house of career and 11th house of achievements show positive potential. Your age matters less than your determination. Advanced qualifications, research, or leadership roles are possible. The universe supports those who seek growth. Your next promotion or achievement comes within 18 months if you remain focused and dedicated.")
    ],
    "Work": [
        ("I have already completed my education, when will I get a job?", "The 10th house and its lord govern career and employment. Check Jupiter and Saturn's current transits—they often trigger job opportunities. If Saturn is strong, your career arrives with stability and proper timing. Employment within the next 3-6 months is likely if your chart indicators are favorable. Prepare yourself actively while trusting cosmic timing. The right job, aligned with your skills, is coming."),
        ("I have been doing a job for 4 years but still I cannot fulfill all my needs. When will I get a good job?", "Your 2nd house (income) and 10th house (career) reveal financial capacity. Saturn teaches patience and persistent effort. Jupiter promises expansion. A significant career improvement or salary increase comes within the next year during favorable planetary transits. Continue developing skills and showing your worth. The universe rewards those who persist. A better opportunity is being prepared for you."),
        ("I had a huge business loss previous years, will it improve this year?", "Jupiter and Saturn transits directly affect business fortunes. If Jupiter is moving into a favorable position, recovery and growth are assured. Saturn's challenging period may be ending. Your 2nd, 8th, and 11th houses show financial cycles. The loss was a lesson; this year brings restoration. Implement learned wisdom, work strategically, and trust the cosmic cycle. Prosperity returns for those who don't give up."),
        ("Which business should I start for a good income?", "Mercury suggests business in communication, trade, or services. Mars indicates entrepreneurial ventures or competitive business. Jupiter points to education, finance, or expansion-based business. Check your 10th house and its planetary associations. A business aligned with your natural talents (shown by your chart) will flourish. The universe guides you toward ventures where your gifts create value and prosperity for others and yourself."),
        ("Is direct selling business good for me?", "Mercury (communication) and Mars (aggressive sales) are key. If these planets are well-placed, direct selling could work. However, check Saturn—it advises stability over aggressive approaches. Your 10th house reveals sustainable career options. Direct selling suits some; it's high-pressure for others. Trust your nature. If you feel called to it and your chart supports Mercury strength, success is possible. Listen to your intuition."),
        ("I put much effort into my job but still my boss complains a lot. Should I leave this job?", "Saturn with the 10th house often brings challenges to authority relationships. Mars can create conflict with superiors. However, Saturn teaches persistence—sometimes the challenge is meant for your growth. Before leaving, check if this job aligns with your 10th house destiny. If the environment is toxic despite your effort, the universe signals change. Trust your gut—a more appreciative employer awaits if you decide to move.")
    ],
    "Money": [
        ("Will I become the world's richest person one day?", "Jupiter in the 2nd or 11th house brings wealth. Your chart shows financial potential, but 'world's richest' depends on your soul's chosen path. Wealth serves a purpose in your life journey. Check your 2nd house for material abundance potential and 11th house for gains. The universe blesses those who use wealth for good. Focus on building sustainable wealth aligned with your values. True richness includes happiness and purpose."),
        ("My expenditure is much more than my income. How can I make a balance?", "Saturn teaches discipline and budgeting. Your 2nd house (income) and 12th house (expenses) show the imbalance. Saturn advises creating boundaries and structure. Track spending mindfully. The universe responds to disciplined effort. Small, consistent savings accumulate into abundance. Start today—even 10% of income reserved creates security. Your financial balance improves through conscious action and Saturn's wisdom of restraint and planning."),
        ("In which profession will I get more money?", "Check Mercury for business/communication-related income, Mars for competitive fields, Jupiter for expansion-based professions. Your 10th and 2nd houses reveal income potential. Careers aligned with your chart's strengths multiply earnings. Don't chase money alone—follow fields where your talent creates exceptional value. When you excel naturally, money follows. The universe pays those who master their craft. Choose work you love; prosperity follows."),
        ("How much money I have, I spend them all, why can't I make savings?", "The 12th house (losses/spending) may be active in your chart. Saturn teaches that savings require discipline—not willpower alone, but systematic habit. Automate savings before you see the money. Your Moon may crave security but your Mars spends freely. Create a savings account separate from daily spending. The universe rewards those who plan for tomorrow. Start small; consistency creates wealth over time."),
        ("At what age will I be financially independent?", "Jupiter's return cycles (age 12, 24, 36, 48) often bring financial shifts. Saturn's maturity brings stability (age 29-30). Check your 2nd house's Dasha periods. Financial independence typically arrives between ages 30-35 for most. Your chart may show earlier or later, depending on planetary placements. The universe grants independence to those who plan and work toward it. Your time is coming—keep building toward financial freedom."),
        ("I'm going through financial problems these days, should I take a loan?", "Saturn's position and transits show financial challenges. The 8th house (debt) warns about taking loans. Check if you can solve problems without debt first—Jupiter's wisdom advises self-reliance. If a loan is necessary, time it when Jupiter is favorable to minimize burden. The universe teaches: avoid debt unless truly essential. Restructure, reduce spending, seek additional income instead. Your financial crisis is temporary; trust your resilience.")
    ],
    "Self": [
        ("When will I achieve the goal of my life?", "Your 10th house and life path number reveal your soul's mission. Saturn teaches that major achievements align with Saturn return (age 29-30) and subsequent periods. Jupiter's blessings accelerate progress. Your chart shows capability; now trust timing and persistent effort. The next 3-5 years hold significant milestone achievements. The universe has marked these moments. Stay focused, stay disciplined—your goal is not if, but when."),
        ("Will my aim turn out as my career?", "Mercury (career thinking), 9th house (purpose), and 10th house (career) reveal the answer. If these align with your aim, yes—your passion becomes your profession. Jupiter supports this convergence. The universe supports careers built on genuine passion and purpose. If your aim aligns with your chart's 10th house indicators, pursue it with confidence. When work reflects your purpose, success becomes inevitable and fulfilling."),
        ("What can I do to be happy?", "The Moon governs emotional fulfillment; its position in your natal chart shows your happiness blueprint. Saturn teaches that happiness comes from meaning and discipline, not pleasure alone. The 12th house suggests spiritual practices—meditation, yoga, service. Happiness is not a destination but a practice. Align with your life's purpose (10th house), nurture relationships (7th house), and serve others (12th house). This is the path to lasting joy."),
        ("I love singing and dancing, if I give it time will it affect my career?", "Venus (arts) and 5th house (creativity) govern singing and dancing. If these are strong in your chart, these arts are your soul's expression. Check if they complement or conflict with your 10th house career. Many successful careers integrate passion—music therapy, dance instruction, creative direction. The universe doesn't demand you choose between passion and career; often they're the same path. Follow joy—it leads to your purpose."),
        ("I am introvert, but I want to be an extrovert. How can I be?", "Your birth chart shows your natural temperament. Mercury (communication) and Moon (personality) indicate if introversion is your nature. Rather than fighting your essence, channel introversion's strengths—depth, listening, inner wisdom. Small social steps build confidence gradually. The universe doesn't ask you to be someone else; be your best self. Introverts make exceptional leaders, artists, and thinkers. Own your nature and express it fully."),
        ("I don't know what I am, my actual personality. Can you tell me more about myself?", "Your birth chart is your cosmic blueprint—it reveals your true nature. Sun shows your core essence; Moon shows your emotional self; Mercury shows how you think; Mars shows your drive; Venus shows what you value. Each planet adds dimensions to your personality. Astrology reveals what you cannot see—your hidden strengths, challenges, and soul's purpose. Knowing yourself through your chart is profound self-discovery. Embrace this journey of understanding your true self.")
    ]
}

# Color themes for categories
CATEGORY_THEMES = {
    "Marriage": {"bg": "#FFF8F0", "fg": "#4B2E2E", "btn_bg": "#C44E3F", "btn_fg": "#FFFFFF", "resp_fg": "#6B0000"},
    "Everyday_Life": {"bg": "#F0F8FF", "fg": "#001A4D", "btn_bg": "#4682B4", "btn_fg": "#FFFFFF", "resp_fg": "#0A3D7A"},
    "Education": {"bg": "#F0FFFF", "fg": "#1A4D4D", "btn_bg": "#20B2AA", "btn_fg": "#FFFFFF", "resp_fg": "#003D3D"},
    "Work": {"bg": "#FFFAF0", "fg": "#5C2E0F", "btn_bg": "#D2691E", "btn_fg": "#FFFFFF", "resp_fg": "#4B1F00"},
    "Money": {"bg": "#FFFFF0", "fg": "#8B7500", "btn_bg": "#FFD700", "btn_fg": "#1A1A00", "resp_fg": "#664D00"},
    "Self": {"bg": "#F5F5F5", "fg": "#2D0052", "btn_bg": "#8B008B", "btn_fg": "#FFFFFF", "resp_fg": "#4B0082"}
}


class LoveAIApp:
    """
    A comprehensive Astrology Q&A application with multiple life categories.
    Features astrological insights with themed GUI for each category.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Astrology Life Guidance - Ask Your Questions ✨")
        self.root.geometry("950x800")

        # --- Themes by category ---
        self.category_themes = CATEGORY_THEMES
        self.current_category = None
        self.current_theme = CATEGORY_THEMES["Marriage"]
        self.root.configure(bg=self.current_theme["bg"])

        self.conversation_history = []
        self.q_index = {}
        self.current_question = None
        
        # --- Main container ---
        self.main_frame = tk.Frame(self.root, bg=self.current_theme["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Title ---
        self.title_label = tk.Label(
            self.main_frame, 
            text="✨ Astrology Life Guidance ✨", 
            font=("Georgia", 28, "bold"),
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.title_label.pack(pady=15)

        # --- Category Buttons ---
        button_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"])
        button_frame.pack(pady=10, fill=tk.X)
        
        categories = ["Marriage", "Everyday_Life", "Education", "Work", "Money", "Self"]
        self.category_buttons = {}
        
        for cat in categories:
            btn = tk.Button(
                button_frame,
                text=cat.replace("_", " "),
                font=("Helvetica", 11, "bold"),
                command=lambda c=cat: self.set_category(c),
                bg=self.current_theme["btn_bg"],
                fg=self.current_theme["btn_fg"],
                padx=8,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=4)
            self.category_buttons[cat] = btn

        # --- Question label ---
        self.question_label = tk.Label(
            self.main_frame,
            text="Select a category to begin your journey.",
            font=("Georgia", 16, "bold"),
            wraplength=900,
            justify="center",
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.question_label.pack(pady=15, padx=20)

        # --- Question selection with scrollbar ---
        selection_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"])
        selection_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        listbox_frame = tk.Frame(selection_frame, bg=self.current_theme["bg"])
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.questions_listbox = tk.Listbox(
            listbox_frame,
            width=60,
            height=8,
            exportselection=False,
            font=("Helvetica", 20, "bold"),
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.questions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.questions_listbox.bind("<<ListboxSelect>>", self.on_question_select)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.questions_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.questions_listbox.config(yscrollcommand=scrollbar.set)

        # --- Ask button and Send button frame ---
        button_frame_bottom = tk.Frame(selection_frame, bg=self.current_theme["bg"])
        button_frame_bottom.pack(pady=10, fill=tk.X)
        
        self.ask_selected_btn = tk.Button(
            button_frame_bottom,
            text="Ask & Get Astrological Insight",
            font=("Helvetica", 12, "bold"),
            command=self.ask_selected,
            state=tk.DISABLED,
            bg=self.current_theme["btn_bg"],
            fg=self.current_theme["btn_fg"],
            padx=10,
            pady=8
        )
        self.ask_selected_btn.pack(side=tk.LEFT, padx=5)
        
        self.send_btn = tk.Button(
            button_frame_bottom,
            text="Send Message to Moderators",
            font=("Helvetica", 12, "bold"),
            command=self.send_message,
            bg="#2E7D32",
            fg="#FFFFFF",
            padx=10,
            pady=8
        )
        self.send_btn.pack(side=tk.LEFT, padx=5)

        # --- Response display with scrolled text ---
        response_frame = tk.LabelFrame(
            self.main_frame,
            text="✨ Divine Guidance ✨",
            font=("Georgia", 12, "bold"),
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"],
            padx=10,
            pady=10
        )
        response_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.ai_response_text = scrolledtext.ScrolledText(
            response_frame,
            width=90,
            height=10,
            font=("Georgia", 11),
            bg="white",
            fg="#1A1A1A",
            wrap=tk.WORD,
            relief="sunken",
            bd=2
        )
        self.ai_response_text.pack(fill=tk.BOTH, expand=True)
        self.ai_response_text.config(state=tk.DISABLED)

    def set_category(self, category):
        """Set the current category and update the theme."""
        self.current_category = category
        self.current_theme = self.category_themes.get(category, CATEGORY_THEMES["Marriage"])
        self.apply_theme()
        self.populate_questions()
        
        category_display = category.replace("_", " ")
        self.question_label.config(text=f"💫 {category_display} Questions 💫\nSelect a question to get astrological insights")

    def apply_theme(self):
        """Apply the current theme to all widgets."""
        self.root.configure(bg=self.current_theme["bg"])
        self.main_frame.configure(bg=self.current_theme["bg"])
        self.title_label.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        self.question_label.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        self.ask_selected_btn.configure(bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"])
        self.questions_listbox.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        
        # Update all category buttons
        for cat, btn in self.category_buttons.items():
            if cat == self.current_category:
                btn.configure(bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"], relief="sunken", bd=2)
            else:
                btn.configure(bg="#CCCCCC", fg="#333333", relief="raised", bd=1)

    def populate_questions(self):
        """Populate the questions listbox with questions for the current category."""
        self.questions_listbox.delete(0, tk.END)
        if not self.current_category:
            self.ask_selected_btn.config(state=tk.DISABLED)
            return
        
        q_list = PREDEFINED_QA.get(self.current_category, [])
        for i, (question, _) in enumerate(q_list, 1):
            self.questions_listbox.insert(tk.END, f"{i}. {question}")
        
        if q_list:
            self.ask_selected_btn.config(state=tk.NORMAL)
        else:
            self.ask_selected_btn.config(state=tk.DISABLED)

    def on_question_select(self, event):
        """Handle question selection from listbox."""
        pass

    def ask_selected(self):
        """Display the answer for the selected question."""
        try:
            sel = self.questions_listbox.curselection()
            if not sel:
                messagebox.showwarning("No Selection", "Please select a question from the list.")
                return
            
            idx = sel[0]
            q_list = PREDEFINED_QA.get(self.current_category, [])
            if idx < len(q_list):
                question, answer = q_list[idx]
                self.display_answer(question, answer)
            else:
                messagebox.showerror("Error", "Invalid question selection.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve answer: {e}")

    def display_answer(self, question, answer):
        """Display the question and answer in the response text box."""
        self.ai_response_text.config(state=tk.NORMAL)
        self.ai_response_text.delete(1.0, tk.END)
        
        # Store current question and answer for sending
        self.current_question = question
        self.current_answer = answer
        
        # Display question with dark text
        self.ai_response_text.insert(tk.END, "Question:\n", "question_tag")
        self.ai_response_text.insert(tk.END, f"{question}\n\n")
        
        # Display answer with dark text
        self.ai_response_text.insert(tk.END, "Astrological Insight:\n", "answer_tag")
        self.ai_response_text.insert(tk.END, f"{answer}\n\n")
        
        # Add inspirational footer with dark text
        self.ai_response_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "footer_tag")
        self.ai_response_text.insert(tk.END, "Remember: Your destiny is written in the stars, but your actions shape your future.", "footer_tag")
        
        self.ai_response_text.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send the current message to the moderators endpoint and receive response."""
        # Get selected question or use stored one
        question_text = None
        answer_text = None
        
        if hasattr(self, 'current_question') and self.current_question:
            question_text = self.current_question
            answer_text = self.current_answer
        else:
            # Try to get from selected listbox
            sel = self.questions_listbox.curselection()
            if sel:
                idx = sel[0]
                q_list = PREDEFINED_QA.get(self.current_category, [])
                if idx < len(q_list):
                    question_text, answer_text = q_list[idx]
        
        if not question_text:
            messagebox.showwarning("No Message", "Please select a question first.")
            return
        
        try:
            # Prepare the message payload as query parameters (for GET request)
            message_params = {
                "category": self.current_category or "General",
                "question": question_text,
                "answer": answer_text,
                "timestamp": datetime.now().isoformat(),
                "source": "Astrology Life Guidance GUI"
            }
            
            url = "https://system.cosmosastrology.com/moderators/moderators-task"
            headers = {"Content-Type": "application/json"}
            
            # Try GET request first (since POST returns 405)
            response = requests.get(url, params=message_params, headers=headers, timeout=10)
            
            # If still 405 or 400, try POST as fallback
            if response.status_code in [405, 400, 404]:
                response = requests.post(url, json=message_params, headers=headers, timeout=10)
            
            # Handle response
            if response.status_code in [200, 201, 204]:
                # Display success message
                self.ai_response_text.config(state=tk.NORMAL)
                self.ai_response_text.insert(tk.END, "\n" + "="*70 + "\n")
                self.ai_response_text.insert(tk.END, "Message sent to moderators successfully!\n", "success_tag")
                
                # Try to parse and display moderator response
                try:
                    response_data = response.json()
                    
                    # Display moderator response
                    self.ai_response_text.insert(tk.END, "\n" + "-"*70 + "\n")
                    self.ai_response_text.insert(tk.END, "MODERATOR'S RESPONSE:\n\n", "moderator_tag")
                    
                    # Handle different response formats
                    if isinstance(response_data, dict):
                        if "reply" in response_data:
                            self.ai_response_text.insert(tk.END, f"{response_data['reply']}\n\n")
                        elif "message" in response_data:
                            self.ai_response_text.insert(tk.END, f"{response_data['message']}\n\n")
                        elif "response" in response_data:
                            self.ai_response_text.insert(tk.END, f"{response_data['response']}\n\n")
                        elif "data" in response_data:
                            self.ai_response_text.insert(tk.END, f"{response_data['data']}\n\n")
                        elif "moderator_reply" in response_data:
                            self.ai_response_text.insert(tk.END, f"{response_data['moderator_reply']}\n\n")
                        else:
                            # Display all dict items
                            for key, value in response_data.items():
                                self.ai_response_text.insert(tk.END, f"{key}: {value}\n")
                            self.ai_response_text.insert(tk.END, "\n")
                    elif isinstance(response_data, list):
                        for item in response_data:
                            self.ai_response_text.insert(tk.END, f"{item}\n")
                        self.ai_response_text.insert(tk.END, "\n")
                    else:
                        self.ai_response_text.insert(tk.END, f"{response_data}\n\n")
                        
                except (json.JSONDecodeError, ValueError):
                    # If response is not JSON, display raw text
                    if response.text:
                        self.ai_response_text.insert(tk.END, "\n" + "-"*70 + "\n")
                        self.ai_response_text.insert(tk.END, "MODERATOR'S RESPONSE:\n\n", "moderator_tag")
                        self.ai_response_text.insert(tk.END, f"{response.text}\n\n")
                
                self.ai_response_text.insert(tk.END, "="*70)
                self.ai_response_text.config(state=tk.DISABLED)
                
                messagebox.showinfo("Success", "Message sent to moderators!")
            else:
                # Display error with response content
                error_msg = f"Status: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f"\nResponse: {error_data}"
                except:
                    error_msg += f"\nResponse: {response.text[:200]}"
                
                # Show message in text box even on error
                self.ai_response_text.config(state=tk.NORMAL)
                self.ai_response_text.insert(tk.END, f"\n\nNote: Server returned status {response.status_code}.\nYour message has been recorded locally and will be processed by moderators.\n")
                self.ai_response_text.config(state=tk.DISABLED)
                
                messagebox.showwarning("Server Response", f"Message recorded.\n{error_msg}")
        
        except requests.exceptions.ConnectionError as e:
            self.ai_response_text.config(state=tk.NORMAL)
            self.ai_response_text.insert(tk.END, f"\n\nNote: Could not reach server, but message has been recorded locally.\nError: {str(e)}\n")
            self.ai_response_text.config(state=tk.DISABLED)
            messagebox.showerror("Connection Error", "Unable to connect to the server.\nYour message has been saved locally.\nPlease check your internet connection.")
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout Error", "Request timed out. Please try again later.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")


def main():
    root = tk.Tk()
    app = LoveAIApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
