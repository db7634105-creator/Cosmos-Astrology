# Quick Start Guide - Astrology Compatibility Matcher

## Installation & Setup

1. **Ensure Python is installed:**
   ```bash
   python --version
   ```
   You need Python 3.6 or higher.

2. **Navigate to the project folder:**
   ```bash
   cd c:\Users\dines\OneDrive\Documents\matching
   ```

## Running the Program

### Option 1: Interactive Mode (Recommended for First-Time Use)
```bash
python astrology_matcher.py
```

Follow the prompts to:
- Enter boy's name and birth details
- Select boy's astrological attributes (Gana, Yoni, Rajju)
- Enter girl's name and birth details
- Select girl's astrological attributes
- View comprehensive compatibility report
- Optionally save results to JSON

### Option 2: Run Sample Tests
```bash
python test_matcher.py
```

This runs pre-configured test cases with 3 sample couples:
1. Raj & Priya
2. Arjun & Deepika  
3. Vikram & Anjali

Shows individual compatibility function tests and zodiac compatibility info.

## Program Features

### All 6 Guna Milan Factors (Total 36 Points)

| Factor | Points | What It Measures |
|--------|--------|-----------------|
| Nadi | 8 | Nervous temperament & mental compatibility |
| Gana | 6 | Nature & character compatibility |
| Yoni | 4 | Sexual & physical compatibility |
| Rashi | 7 | Zodiac sign compatibility |
| Bhakut | 7 | Emotional strength & relationship stability |
| Rajju | 8 | Family lineage compatibility |

### Compatibility Ratings

- **32-36 points (89-100%)**: ⭐⭐⭐⭐⭐ **Excellent** - Highly Recommended
- **28-31 points (78-88%)**: ⭐⭐⭐⭐ **Very Good** - Strong Match
- **24-27 points (67-77%)**: ⭐⭐⭐ **Good** - Decent Match
- **18-23 points (50-66%)**: ⭐⭐ **Average** - Needs Understanding
- **12-17 points (33-49%)**: ⭐ **Below Average** - Challenging
- **Below 12 points (0-33%)**: ❌ **Poor** - Not Recommended

## Input Requirements

### Birth Date Format
- **Format**: DD/MM/YYYY (e.g., 15/08/1995)
- Must be a valid calendar date

### Birth Time Format
- **Format**: HH:MM (24-hour, e.g., 14:30 for 2:30 PM)
- Use 00:00 for midnight, 23:59 for 11:59 PM

### Astrological Selections

**Gana (Nature) - 3 Options:**
1. Deva - Divine, Virtuous
2. Manusha - Human, Balanced  
3. Rakshasa - Demon, Wild

**Yoni (Sexual Nature) - 14 Options:**
1. Ashwa (Horse) - Strong, Active
2. Gaj (Elephant) - Calm, Wise
3. Mesha (Sheep) - Gentle, Timid
4. Sarpa (Snake) - Secretive, Passionate
5. Sinha (Lion) - Brave, Strong
6. Marjara (Cat) - Quick, Restless
7. Vrishabha (Bull) - Stable, Patient
8. Vrika (Dog) - Loyal, Protective
9. Simhika (Serpent) - Sharp, Intelligent
10. Kaka (Crow) - Quick, Alert
11. Khaga (Bird) - Free, Mobile
12. Mriga (Deer) - Gentle, Sensitive
13. Vanara (Monkey) - Playful, Social
14. Makar (Crocodile) - Mysterious, Deep

**Rajju (Family Line) - 5 Options:**
1. Adi - Beginning (Head)
2. Madhya - Middle (Body)
3. Anta - End (Legs)
4. Parivartana - Exchanged
5. Parivartana - Exchanged (Same as 4)

**Nadi - Automatically Calculated:**
- Based on birth time, no selection needed
- Vata (6 AM - 2 PM)
- Pitta (2 PM - 10 PM)
- Kapha (10 PM - 6 AM)

## Example Session

```
==================================================
VEDIC ASTROLOGY COMPATIBILITY MATCHER
Guna Milan (36 Point System)
==================================================

Enter Boy's Details
==================================================

Enter Boy's name: Raj

Enter Boy's birth date (DD/MM/YYYY): 15/08/1995

Enter Boy's birth time (HH:MM in 24-hour format): 14:30

Select Gana (Nature):
1. Deva - Divine, Virtuous
2. Manusha - Human, Balanced
3. Rakshasa - Demon, Wild
Enter choice (1-3): 1

Select Yoni (Sexual Nature):
1. Ashwa - Horse (Strong, Active)
...
14. Makar - Crocodile (Mysterious, Deep)
Enter choice (1-14): 1

Select Rajju (Family Line):
1. Adi - Beginning
2. Madhya - Middle
3. Anta - End
4. Parivartana - Exchanged
5. Parivartana - Exchanged
Enter choice (1-5): 1

[Same for Girl's details...]

==================================================================
                  COMPATIBILITY REPORT
==================================================================

Boy: Raj                          Girl: Priya

OVERALL COMPATIBILITY: 32/36 (88.89%)
Rating: Excellent - Outstanding compatibility

──────────────────────────────────────────────────
              DETAILED BREAKDOWN
──────────────────────────────────────────────────

Nervous Temperament Compatibility........ 8/8
Gana Nature/Character Compatibility...... 6/6
Sexual/Physical Compatibility........... 4/4
Zodiac Sign Compatibility............... 7/7
Nature/Strength Compatibility........... 5/7
Family Line Compatibility............... 2/8

Would you like to save the results to a file? (yes/no): yes

Enter filename (default: match_results.json): raj_priya_match.json

Results saved to raj_priya_match.json
```

## Output Files

When you save results, a JSON file is created with all matching details:

```json
{
  "boy_name": "Raj",
  "girl_name": "Priya",
  "total_score": 32,
  "max_score": 36,
  "percentage": 88.89,
  "details": {
    "nadi": {...},
    "gana": {...},
    ...
  }
}
```

These files are saved in the same directory as the program.

## Zodiac Sign Quick Reference

### Fire Signs (Passionate, Energetic)
- Aries, Leo, Sagittarius

### Earth Signs (Practical, Stable)
- Taurus, Virgo, Capricorn

### Air Signs (Intellectual, Social)
- Gemini, Libra, Aquarius

### Water Signs (Emotional, Intuitive)
- Cancer, Scorpio, Pisces

### Best Matches by Sign
| Sign | Best Match |
|------|-----------|
| Aries | Leo, Sagittarius |
| Taurus | Virgo, Capricorn |
| Gemini | Libra, Aquarius |
| Cancer | Scorpio, Pisces |
| Leo | Sagittarius, Aries |
| Virgo | Capricorn, Taurus |
| Libra | Aquarius, Gemini |
| Scorpio | Pisces, Cancer |
| Sagittarius | Aries, Leo |
| Capricorn | Taurus, Virgo |
| Aquarius | Gemini, Libra |
| Pisces | Cancer, Scorpio |

## Tips for Accurate Results

1. **Accurate Birth Time**: The program calculates Nadi from birth time. Try to get the exact birth time from birth certificates for best results.

2. **Correct Birth Date**: Use the actual birth date in Gregorian calendar format.

3. **Astrological Attributes**: Choose Gana, Yoni, and Rajju based on the person's natal chart. If you're unsure, consult with a Vedic astrologer.

4. **Keep Records**: Save JSON files for future reference and comparison.

5. **Multiple Matches**: The program allows checking multiple matches in one session.

## Troubleshooting

### Program won't start
- Ensure Python is properly installed
- Check that you're in the correct directory
- Try: `python --version` to verify Python works

### Invalid date error
- Check date format is DD/MM/YYYY
- Ensure the date is valid (e.g., not 31/02)

### Need help with selections
- Refer to the quick reference tables above
- Run `python test_matcher.py` to see example outputs

## Advanced Usage

### Programmatic Use
```python
from astrology_matcher import AstrologyMatcher

matcher = AstrologyMatcher()

boy = {
    "name": "Raj",
    "day": 15, "month": 8, "year": 1995,
    "birth_time": "14:30",
    "zodiac_sign": "Leo",
    "nadi": "Pitta",
    "gana": "Deva",
    "yoni": "Ashwa",
    "rajju": "Adi"
}

girl = {
    "name": "Priya",
    "day": 20, "month": 11, "year": 1997,
    "birth_time": "09:15",
    "zodiac_sign": "Scorpio",
    "nadi": "Vata",
    "gana": "Manusha",
    "yoni": "Gaj",
    "rajju": "Madhya"
}

results = matcher.calculate_compatibility(boy, girl)
matcher.display_results(results)
matcher.save_results(results, "custom_match.json")
```

## File Structure

```
matching/
├── astrology_matcher.py      # Main program (run this!)
├── test_matcher.py           # Sample tests and demos
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
└── [saved JSON files]        # Your match results
```

## Need More Help?

1. Check README.md for detailed documentation
2. Run test_matcher.py to see examples
3. Review comments in astrology_matcher.py for technical details
4. Check sample JSON files for output format

Enjoy matching! 🌟
