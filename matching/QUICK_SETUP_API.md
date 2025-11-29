# API VERSION - QUICK SETUP GUIDE

## ⚡ 5-Minute Setup

### Step 1: Install Python Library (1 minute)
```bash
pip install requests
```

Or with Python 3:
```bash
python -m pip install requests
```

Verify installation:
```bash
python -c "import requests; print('OK')"
```

### Step 2: Navigate to Folder (30 seconds)
```bash
cd "c:\Users\dines\OneDrive\Documents\matching"
```

### Step 3: Run the Program (30 seconds)
```bash
python astrology_matcher_api.py
```

### Step 4: Enter Details (2 minutes)
When prompted:
- Enter groom's name
- Enter birth date as: DD/MM/YYYY (e.g., 15/08/1995)
- Enter birth time as: HH:MM:SS (e.g., 14:30:00)
- Enter birth city (e.g., Delhi, Mumbai)
- Repeat for bride

### Step 5: View Results (1 minute)
Program shows:
- Overall compatibility score
- 8-factor detailed breakdown
- Percentage match
- Rating (Excellent, Good, Average, etc.)

---

## 🎯 What Happens

```
YOU ENTER:           API DOES:              YOU GET:
─────────────────────────────────────────────────────
Birth data ──────→ Connects to API ──────→ Ashtakoot
Names               Sends coordinates        Results
Times               Calculates 8 factors     JSON file
Dates               Scores out of 36        Beautiful
Locations           Returns JSON            Report
```

---

## 📝 Input Examples

### Birth Date Format
✓ Correct: 15/08/1995 (15th Aug 1995)
✗ Wrong: 08/15/1995, 15-08-1995

### Birth Time Format
✓ Correct: 14:30:00 (2:30 PM), 06:15:30 (6:15 AM)
✗ Wrong: 2:30 PM, 06:30, 2:30PM

### Birth City
✓ Correct: Delhi, Mumbai, Bangalore, Pune, Jaipur
✗ Wrong: precise coordinates (not needed, just city name)

---

## 🌍 Supported Cities

### India
Delhi, Mumbai, Bangalore, Hyderabad, Kolkata, Pune, Ahmedabad, Jaipur, Lucknow, Kanpur, Indore, Goa

### International
London, New York, Los Angeles, Toronto, Sydney, Dubai, Singapore, Bangkok, Hong Kong, Tokyo

### Not in List?
- Enter city name anyway
- Program uses Delhi as default
- Results still valid

---

## 📊 Understanding Results

### Score Interpretation
```
32-36 (89-100%)    EXCELLENT      ⭐⭐⭐⭐⭐
28-31 (78-88%)     VERY GOOD      ⭐⭐⭐⭐
24-27 (67-77%)     GOOD           ⭐⭐⭐
18-23 (50-66%)     AVERAGE        ⭐⭐
12-17 (33-49%)     BELOW AVERAGE  ⭐
0-11  (0-32%)      POOR           ❌
```

### 8 Kootas Explained
1. **Varna** (1 pt) - Caste/Quality
2. **Vasya** (2 pts) - Control/Dominance
3. **Tara** (3 pts) - Star/Longevity
4. **Yoni** (4 pts) - Sexual Compatibility
5. **Graha Maitri** (5 pts) - Planetary Friendship
6. **Gana** (6 pts) - Nature/Temperament
7. **Rasi** (7 pts) - Moon Sign
8. **Nadi** (8 pts) - Health/Heredity

---

## ❓ Common Questions

**Q: Why do I need to install 'requests'?**
A: It's a library for sending data to the API. Without it, Python can't connect.

**Q: Will it work offline?**
A: No, needs internet for API connection. Local version works offline.

**Q: How long does it take?**
A: 5-10 seconds typically. Depends on internet speed.

**Q: Is my data safe?**
A: Yes. Uses HTTPS encryption. No data stored permanently.

**Q: Can I check multiple couples?**
A: Yes! Program asks if you want another match after each result.

---

## 🔧 If Something Goes Wrong

### "requests not found"
```bash
pip install requests
```

### "No internet connection"
```
Check WiFi or network
Try again in a few seconds
```

### "API Error"
```
Retry after a moment
Check internet connection
Contact API support if persists
```

### "Invalid date/time"
```
Use format: DD/MM/YYYY for dates
Use format: HH:MM:SS for times
Examples: 15/08/1995, 14:30:00
```

---

## 📁 Files

| File | Purpose |
|------|---------|
| **astrology_matcher_api.py** | Main API program |
| **API_USER_GUIDE.md** | Detailed guide |
| **QUICK_SETUP_API.md** | This file |

---

## 🚀 Let's Get Started!

### One-Line Summary
```
1. pip install requests
2. python astrology_matcher_api.py
3. Enter birth details
4. Get Ashtakoot matching results!
```

### Ready?
```bash
cd "c:\Users\dines\OneDrive\Documents\matching"
python astrology_matcher_api.py
```

---

## 📊 Sample Output

```
================================================================================
                        ASHTAKOOT MATCHING REPORT
================================================================================

Groom: Raj                          Bride: Priya

OVERALL COMPATIBILITY: 28/36 (77.78%)
Rating: Very Good - Strong compatibility

DETAILED KOOTA BREAKDOWN:
──────────────────────────────────────────────────────
Varna Kootam        1/1 ████████████████████ 
Vasya Kootam        2/2 ████████████████████
Tara Kootam         2/3 ██████████░░░░░░░░░░
Yoni Kootam         4/4 ████████████████████
Graha Maitri        4/5 ████████████████░░░░
Gana Kootam         5/6 █████████████████░░░
Rasi Kootam         7/7 ████████████████████
Nadi Kootam         3/8 ████████░░░░░░░░░░░░

Save results? yes → ashtakoot_Raj_Priya.json
Another match? yes/no
```

---

## ✅ Checklist

- [ ] Python installed (python --version)
- [ ] In matching folder (cd ...)
- [ ] Requests installed (pip install requests)
- [ ] API key configured (built-in: DiA8MzlbeP9zQHZfCBFi69bMPWYDweB78H3pii6B)
- [ ] Internet connection ready
- [ ] Birth details prepared
- [ ] Ready to run!

---

## 🎉 You're Ready!

Everything is set up. Just run:
```bash
python astrology_matcher_api.py
```

Then follow the prompts!

**Questions?** See API_USER_GUIDE.md
**Need help?** Check troubleshooting section

Happy matching! 🌙✨
