# Vedic Astrology Compatibility Matcher

A standalone Python program for matching boy and girl compatibility based on Vedic astrology principles using the Guna Milan system (36-point scale).

## Features

### Core Matchmaking Features (Guna Milan)

The program implements all 6 major compatibility factors in Vedic astrology:

1. **Nadi (Nervous Temperament)** - 8 points max
   - Measures mental and physical temperament compatibility
   - Three types: Vata (Air), Pitta (Fire), Kapha (Earth/Water)
   - Compatible when different Nadis complement each other

2. **Gana (Nature/Character)** - 6 points max
   - Evaluates character and nature compatibility
   - Three types: Deva (Divine), Manusha (Human), Rakshasa (Demon/Wild)
   - Same Gana is ideal

3. **Yoni (Sexual Compatibility)** - 4 points max
   - Assesses physical and intimate compatibility
   - 14 different Yoni types (Ashwa, Gaj, Mesha, Sarpa, etc.)
   - Based on animal representations and natural affinities
   - Same or friendly Yonis score higher

4. **Rashi (Zodiac Sign Compatibility)** - 7 points max
   - Checks zodiac sign compatibility
   - Considers aspects: Trine (120°), Sextile (60°), Opposition (180°)
   - 12 zodiac signs with specific compatibility patterns

5. **Bhakut (Nature/Strength Compatibility)** - 7 points max
   - Evaluates strength and emotional compatibility
   - Based on zodiac sign interactions
   - Determines sustained relationship potential

6. **Rajju (Family Line Compatibility)** - 8 points max
   - Ensures continuity of family line
   - 5 types: Adi, Madhya, Anta, Parivartana, Parivartana
   - Different Rajjus indicate good family compatibility

### Total Score: 36 Points

- **32-36 points**: Excellent - Outstanding compatibility
- **28-31 points**: Very Good - Strong compatibility
- **24-27 points**: Good - Decent compatibility
- **18-23 points**: Average - Moderate compatibility
- **12-17 points**: Below Average - Low compatibility
- **Below 12**: Poor - Very poor compatibility

## Installation

No external dependencies required! Uses only Python standard library.

```bash
# Simply have Python 3.6+ installed
python --version
```

## Usage

### Running the Program

```bash
python astrology_matcher.py
```

### Interactive Input Process

1. Enter boy's details:
   - Full name
   - Birth date (DD/MM/YYYY)
   - Birth time (HH:MM in 24-hour format)
   - Gana (Nature) - select from Deva, Manusha, Rakshasa
   - Yoni - select from 14 different types
   - Rajju (Family Line) - select from 5 types

2. Enter girl's details (same information as above)

3. The program automatically:
   - Calculates zodiac sign from birth date
   - Determines Nadi from birth time
   - Computes all 6 compatibility factors
   - Generates comprehensive compatibility report

4. View detailed results with:
   - Total compatibility score (out of 36)
   - Percentage match
   - Compatibility rating
   - Detailed breakdown of all 6 factors
   - Visual progress bars for each factor

5. Optionally save results to JSON file for future reference

## Program Structure

```
astrology_matcher.py
├── AstrologyMatcher Class
│   ├── Zodiac and astrology data
│   ├── Compatibility calculation methods
│   │   ├── Nadi compatibility
│   │   ├── Gana compatibility
│   │   ├── Yoni compatibility
│   │   ├── Rashi compatibility
│   │   ├── Bhakut compatibility
│   │   └── Rajju compatibility
│   ├── Input/Output methods
│   └── Reporting methods
└── main() entry point
```

## Example Output

```
======================================================================
                        COMPATIBILITY REPORT
======================================================================

Boy: Raj                           Girl: Priya

────────────────────────────────────────────────────────────────────
OVERALL COMPATIBILITY: 32/36 (88.89%)
Rating: Excellent - Outstanding compatibility - Highly recommended match

────────────────────────────────────────────────────────────────────
                         DETAILED BREAKDOWN
────────────────────────────────────────────────────────────────────

Nervous Temperament Compatibility........ ████████░░░░░░░░░░░░░░░░░░░ 8/8
  → Boy's Nadi: Pitta, Girl's Nadi: Vata

Nature/Character Compatibility............ ██████░░░░░░░░░░░░░░░░░░░░░░░░░ 6/6
  → Boy's Gana: Deva, Girl's Gana: Manusha

Sexual/Physical Compatibility............. ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 4/4
  → Boy's Yoni: Ashwa, Girl's Yoni: Gaj

Zodiac Sign Compatibility................. ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 7/7
  → Boy's Rashi: Leo, Girl's Rashi: Sagittarius

Nature/Strength Compatibility............ █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5/7
  → Nature/Strength Compatibility

Family Line Compatibility................ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2/8
  → Boy's Rajju: Adi, Girl's Rajju: Madhya

────────────────────────────────────────────────────────────────────
```

## Astrological Principles

### Zodiac Sign Compatibility

- **Aries**: Most compatible with Leo, Sagittarius, Libra
- **Taurus**: Most compatible with Virgo, Capricorn, Pisces
- **Gemini**: Most compatible with Libra, Aquarius, Aries
- **Cancer**: Most compatible with Scorpio, Pisces, Taurus
- **Leo**: Most compatible with Sagittarius, Aries, Gemini
- **Virgo**: Most compatible with Capricorn, Taurus, Cancer
- **Libra**: Most compatible with Aquarius, Gemini, Leo
- **Scorpio**: Most compatible with Pisces, Cancer, Virgo
- **Sagittarius**: Most compatible with Aries, Leo, Libra
- **Capricorn**: Most compatible with Taurus, Virgo, Scorpio
- **Aquarius**: Most compatible with Gemini, Libra, Sagittarius
- **Pisces**: Most compatible with Cancer, Scorpio, Taurus

### Yoni Types and Characteristics

- **Ashwa** (Horse): Strong, Active
- **Gaj** (Elephant): Calm, Wise
- **Mesha** (Sheep): Gentle, Timid
- **Sarpa** (Snake): Secretive, Passionate
- **Sinha** (Lion): Brave, Strong
- **Marjara** (Cat): Quick, Restless
- **Vrishabha** (Bull): Stable, Patient
- **Vrika** (Dog): Loyal, Protective
- **Simhika** (Serpent): Sharp, Intelligent
- **Kaka** (Crow): Quick, Alert
- **Khaga** (Bird): Free, Mobile
- **Mriga** (Deer): Gentle, Sensitive
- **Vanara** (Monkey): Playful, Social
- **Makar** (Crocodile): Mysterious, Deep

## File Output

When saving results, a JSON file is created with the structure:

```json
{
  "boy_name": "Raj",
  "girl_name": "Priya",
  "total_score": 32,
  "max_score": 36,
  "percentage": 88.89,
  "details": {
    "nadi": {
      "score": 8,
      "max": 8,
      "boy_nadi": "Pitta",
      "girl_nadi": "Vata",
      "description": "Nervous Temperament Compatibility"
    },
    ...
  }
}
```

## Notes

- Birth times should be as accurate as possible for better Nadi calculation
- The program uses simplified Vedic astrology calculations suitable for general compatibility assessment
- For professional astrological consultation, consider consulting with a certified Vedic astrologer
- All calculations are based on traditional Vedic astrology principles

## Requirements

- Python 3.6 or higher
- No external dependencies required

## License

This program is provided as-is for educational and personal use.

## Support

For issues or improvements, refer to the source code documentation within `astrology_matcher.py`.
