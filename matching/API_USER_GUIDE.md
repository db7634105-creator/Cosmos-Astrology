# API-Integrated Astrology Matcher - User Guide

## 🚀 NEW: FreeAstrology API Integration

Your astrology matcher now supports **professional API-based matching** using the FreeAstrology Ashtakoot Score API!

---

## 📋 What's New

### Enhanced Features
✅ **Real Professional API Integration** - Uses FreeAstrology's trusted API
✅ **8-Factor Ashtakoot System** - More comprehensive than local calculations
✅ **Automatic Location Support** - Includes 50+ Indian cities with coordinates
✅ **Professional Results** - API-verified compatibility scores
✅ **Instant Processing** - Get results in seconds
✅ **Better Accuracy** - Uses topocentric observation and Lahiri ayanamsha

---

## 📊 The 8 Kootas (Ashtakoot System)

| Koota | Points | Measures |
|-------|--------|----------|
| **Varna Kootam** | 1 | Caste/Quality compatibility |
| **Vasya Kootam** | 2 | Control/Dominance dynamics |
| **Tara Kootam** | 3 | Star/Longevity patterns |
| **Yoni Kootam** | 4 | Sexual compatibility |
| **Graha Maitri Kootam** | 5 | Planetary friendship |
| **Gana Kootam** | 6 | Nature/Temperament match |
| **Rasi Kootam** | 7 | Moon sign compatibility |
| **Nadi Kootam** | 8 | Health/Heredity factors |
| **TOTAL** | **36** | **Overall Score** |

---

## 🎯 Compatibility Scale

```
Score Range     % Match    Rating              Recommendation
─────────────────────────────────────────────────────────────
32-36 pts       89-100%    EXCELLENT           ⭐⭐⭐⭐⭐
28-31 pts       78-88%     VERY GOOD           ⭐⭐⭐⭐
24-27 pts       67-77%     GOOD                ⭐⭐⭐
18-23 pts       50-66%     AVERAGE             ⭐⭐
12-17 pts       33-49%     BELOW AVERAGE       ⭐
0-11 pts        0-32%      POOR                ❌
```

---

## ⚙️ Installation

### Prerequisites
```bash
Python 3.6+
requests library (for API calls)
```

### Install requests library
```bash
pip install requests
```

Or if you have Python 3:
```bash
python -m pip install requests
```

### Check Installation
```bash
python -c "import requests; print('✓ requests library installed')"
```

---

## 🚀 Quick Start

### Running the Program
```bash
# Navigate to folder
cd "c:\Users\dines\OneDrive\Documents\matching"

# Run the API version
python astrology_matcher_api.py
```

---

## 📝 Input Requirements

### What You'll Need

1. **For Both Groom and Bride:**
   - Full name
   - Birth date (DD/MM/YYYY format)
   - Birth time (HH:MM:SS in 24-hour format)
   - Birth city

### Input Format Examples

**Birth Date:**
- Format: DD/MM/YYYY
- Examples: 15/08/1995, 03/12/1998, 25/01/1990

**Birth Time:**
- Format: HH:MM:SS (24-hour)
- Examples: 14:30:00 (2:30 PM), 06:15:30 (6:15:30 AM), 23:45:00 (11:45 PM)

**Birth City:**
- Examples: Delhi, Mumbai, Bangalore, Hyderabad, Pune, Jaipur
- Program auto-detects coordinates and timezone for major Indian cities

---

## 🌍 Supported Cities

### Major Indian Cities (Built-in Coordinates)
```
Delhi, Mumbai, Bangalore, Hyderabad, Kolkata, Pune, Ahmedabad,
Jaipur, Lucknow, Kanpur, Indore, Goa, and more
```

### How it Works
- You enter city name
- Program automatically:
  - Gets latitude & longitude
  - Gets correct timezone offset
  - Sends to API with proper coordinates

### Other Cities
- If city not in database, uses Delhi coordinates as default
- You can manually provide coordinates if needed

---

## 💻 Program Flow

```
1. Start Program
   ↓
2. Enter Groom Details
   - Name
   - Birth Date (DD/MM/YYYY)
   - Birth Time (HH:MM:SS)
   - Birth City
   ↓
3. Enter Bride Details
   - Name
   - Birth Date (DD/MM/YYYY)
   - Birth Time (HH:MM:SS)
   - Birth City
   ↓
4. Connect to FreeAstrology API
   - Sends data with your API key
   ↓
5. Receive Results
   - 8-factor analysis
   - Total score out of 36
   - Percentage match
   ↓
6. View Beautiful Report
   - Overall compatibility
   - Koota-by-koota breakdown
   - Visual progress bars
   ↓
7. Save to JSON (Optional)
   ↓
8. Check Another Match or Exit
```

---

## 📊 Sample Output Format

```
================================================================================
                        ASHTAKOOT MATCHING REPORT
                         (Using FreeAstrology API)
================================================================================

Groom: Raj                           Bride: Priya

────────────────────────────────────────────────────────────────────────────────

                           OVERALL COMPATIBILITY
────────────────────────────────────────────────────────────────────────────────
Total Score: 28/36 (77.78%)
Rating: Very Good - Strong compatibility - A very good match

────────────────────────────────────────────────────────────────────────────────
                          DETAILED KOOTA BREAKDOWN
────────────────────────────────────────────────────────────────────────────────

Varna Kootam (Caste/Quality Compatibility)
Score: 1/1 ████████████████████████████████

Vasya Kootam (Control/Dominance)
Score: 2/2 ████████████████████████████████

Tara Kootam (Star/Longevity)
Score: 2/3 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Yoni Kootam (Sexual Compatibility)
Score: 4/4 ████████████████████████████████

Graha Maitri Kootam (Planetary Friendship)
Score: 4/5 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Gana Kootam (Nature/Temperament)
Score: 5/6 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Rasi Kootam (Moon Sign Compatibility)
Score: 7/7 ████████████████████████████████

Nadi Kootam (Health/Heredity)
Score: 3/8 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

────────────────────────────────────────────────────────────────────────────────
```

---

## 💾 Output & Saving

### JSON Export Example
```json
{
  "boy_name": "Raj",
  "girl_name": "Priya",
  "total_score": 28,
  "out_of": 36,
  "percentage": 77.78,
  "kootas": {
    "varna_kootam": {
      "name": "Varna Kootam",
      "description": "Caste/Quality Compatibility",
      "score": 1,
      "out_of": 1,
      "bride_details": {
        "varnam": 4,
        "varnam_name": "Soodra",
        "moon_sign": "Aquarius"
      },
      "groom_details": {
        "varnam": 2,
        "varnam_name": "Kshatriya",
        "moon_sign": "Aries"
      }
    }
  }
}
```

### Saving Results
- Program asks if you want to save after each match
- Choose: Yes → Enter filename → Saved as JSON
- Default filename: `ashtakoot_[groom]_[bride].json`

---

## 🔒 API Information

### API Key
- **Your API Key:** DiA8MzlbeP9zQHZfCBFi69bMPWYDweB78H3pii6B
- **Provider:** FreeAstrology API
- **Endpoint:** https://json.freeastrologyapi.com/match-making/ashtakoot-score
- **Method:** POST
- **Language:** English
- **Ayanamsha:** Lahiri
- **Observation:** Topocentric

### What Gets Sent to API
```json
{
  "male": {
    "year": 1995,
    "month": 8,
    "date": 15,
    "hours": 14,
    "minutes": 30,
    "seconds": 0,
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": 5.5
  },
  "female": {
    "year": 1997,
    "month": 11,
    "date": 20,
    "hours": 9,
    "minutes": 15,
    "seconds": 0,
    "latitude": 19.0760,
    "longitude": 72.8777,
    "timezone": 5.5
  },
  "config": {
    "observation_point": "topocentric",
    "language": "en",
    "ayanamsha": "lahiri"
  }
}
```

---

## ✅ Understanding the Results

### What Each Koota Means

**Varna Kootam (1 pt)**
- Measures caste/quality compatibility
- Maximum score: 1
- Higher score = Better caste match

**Vasya Kootam (2 pts)**
- Measures who controls whom in relationship
- Maximum score: 2
- Indicates dominance dynamics

**Tara Kootam (3 pts)**
- Measures star/birth constellation
- Maximum score: 3
- Related to longevity and life events

**Yoni Kootam (4 pts)**
- Sexual and physical compatibility
- Maximum score: 4
- Most important for physical connection

**Graha Maitri Kootam (5 pts)**
- Planetary ruler friendship
- Maximum score: 5
- Indicates moon sign ruler compatibility

**Gana Kootam (6 pts)**
- Nature and temperament matching
- Maximum score: 6
- Shows if natures complement each other

**Rasi Kootam (7 pts)**
- Moon sign (Rashi) compatibility
- Maximum score: 7
- Most used indicator in astrology

**Nadi Kootam (8 pts)**
- Health and heredity compatibility
- Maximum score: 8
- Important for health inheritance

---

## ❓ FAQ

### Q: What if API fails to connect?
A: Check internet connection and try again. If issue persists, contact API support.

### Q: Can I use non-Indian cities?
A: Yes! Built-in support for London, NY, LA, Toronto, Sydney, Dubai, Singapore, Bangkok, Hong Kong, Tokyo.

### Q: How accurate are the results?
A: Very accurate! Uses professional Vedic astrology calculations from trusted API provider.

### Q: Can I save multiple matches?
A: Yes! Program allows checking multiple matches with unique filenames.

### Q: What's the difference from the local version?
A: 
- Local version: Uses basic Guna Milan (6 factors)
- API version: Uses professional Ashtakoot (8 factors) + API calculations

### Q: Is my birth data secure?
A: Data is sent to API over HTTPS (secure connection). No data is stored on your computer after processing.

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
**Solution:**
```bash
pip install requests
```

### "Connection Error"
**Solution:**
- Check internet connection
- Check if API is working at: https://freeastrologyapi.com
- Wait a moment and try again

### "Invalid date" error
**Solution:**
- Use format: DD/MM/YYYY (not MM/DD/YYYY)
- Example: 15/08/1995 (15th August 1995)

### "Invalid time" error
**Solution:**
- Use format: HH:MM:SS in 24-hour
- Example: 14:30:00 (2:30 PM), not 2:30:00 PM

### "City not found"
**Solution:**
- Enter exact city name (case-insensitive)
- Program will use Delhi coordinates as default
- Or enter any major Indian city

---

## 📚 Using Both Versions

### Local Version (astrology_matcher.py)
- **Best for:** Offline use, no internet needed
- **Factors:** 6 Guna Milan factors
- **Accuracy:** Good for general matching
- **Use when:** No internet or want local computation

### API Version (astrology_matcher_api.py)
- **Best for:** Professional matching, detailed analysis
- **Factors:** 8 Ashtakoot kootas
- **Accuracy:** Professional-grade results
- **Use when:** Want trusted API results with details

---

## 🌐 Switching Between Versions

```bash
# Use local version
python astrology_matcher.py

# Use API version (RECOMMENDED)
python astrology_matcher_api.py
```

---

## 📞 API Support

- **Website:** https://freeastrologyapi.com
- **Documentation:** https://freeastrologyapi.com/api-reference
- **Postman Collection:** Available at FreeAstrology docs
- **Status:** 24/7 API availability

---

## 🎉 Getting Started

### First Time Users
1. Install requests library: `pip install requests`
2. Run the program: `python astrology_matcher_api.py`
3. Follow the prompts
4. Enter birth details
5. View results
6. Save if desired

### Example Session
```
Enter Groom Details:
- Name: Raj
- Birth Date: 15/08/1995
- Birth Time: 14:30:00
- Birth City: Delhi

Enter Bride Details:
- Name: Priya
- Birth Date: 20/11/1997
- Birth Time: 09:15:00
- Birth City: Mumbai

→ Program connects to API
→ Shows detailed Ashtakoot report
→ Saves to: ashtakoot_Raj_Priya.json
```

---

## ✨ Key Advantages

✅ **Professional Results** - Uses trusted FreeAstrology API
✅ **8-Factor Analysis** - More comprehensive than Guna Milan
✅ **Auto-Location** - Built-in database for major cities
✅ **Instant Results** - Get analysis in seconds
✅ **Beautiful Reports** - Well-formatted output with progress bars
✅ **Data Export** - Save to JSON for records
✅ **User-Friendly** - Clear prompts and helpful messages

---

## 🚀 Next Steps

1. **Install dependencies:** `pip install requests`
2. **Run program:** `python astrology_matcher_api.py`
3. **Enter details:** Groom and bride information
4. **View results:** Beautiful Ashtakoot report
5. **Save & compare:** Export results for future reference

Enjoy your professional astrology matching! 🌙✨

---

**Version:** 2.0 (API-Enhanced)
**API Provider:** FreeAstrology
**Status:** Production Ready ✓
