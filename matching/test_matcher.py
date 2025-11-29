"""
Demo/Test script for Astrology Matcher
Shows how to use the matcher programmatically with sample data
"""

from astrology_matcher import AstrologyMatcher
import json


def test_sample_matches():
    """Test with predefined sample data"""
    matcher = AstrologyMatcher()
    
    # Sample data 1: Raj and Priya
    print("\n" + "="*70)
    print("SAMPLE TEST 1: Raj and Priya")
    print("="*70)
    
    raj_data = {
        "name": "Raj",
        "day": 15,
        "month": 8,
        "year": 1995,
        "birth_time": "14:30",
        "zodiac_sign": matcher.get_zodiac_sign(8, 15),
        "nadi": matcher.calculate_nadi_guna("14:30"),
        "gana": "Deva",
        "yoni": "Ashwa",
        "rajju": "Adi"
    }
    
    priya_data = {
        "name": "Priya",
        "day": 20,
        "month": 11,
        "year": 1997,
        "birth_time": "09:15",
        "zodiac_sign": matcher.get_zodiac_sign(11, 20),
        "nadi": matcher.calculate_nadi_guna("09:15"),
        "gana": "Manusha",
        "yoni": "Gaj",
        "rajju": "Madhya"
    }
    
    results1 = matcher.calculate_compatibility(raj_data, priya_data)
    matcher.display_results(results1)
    
    # Sample data 2: Arjun and Deepika
    print("\n" + "="*70)
    print("SAMPLE TEST 2: Arjun and Deepika")
    print("="*70)
    
    arjun_data = {
        "name": "Arjun",
        "day": 3,
        "month": 4,
        "year": 1994,
        "birth_time": "06:45",
        "zodiac_sign": matcher.get_zodiac_sign(4, 3),
        "nadi": matcher.calculate_nadi_guna("06:45"),
        "gana": "Rakshasa",
        "yoni": "Sarpa",
        "rajju": "Madhya"
    }
    
    deepika_data = {
        "name": "Deepika",
        "day": 28,
        "month": 1,
        "year": 1998,
        "birth_time": "11:30",
        "zodiac_sign": matcher.get_zodiac_sign(1, 28),
        "nadi": matcher.calculate_nadi_guna("11:30"),
        "gana": "Deva",
        "yoni": "Marjara",
        "rajju": "Anta"
    }
    
    results2 = matcher.calculate_compatibility(arjun_data, deepika_data)
    matcher.display_results(results2)
    
    # Sample data 3: Vikram and Anjali
    print("\n" + "="*70)
    print("SAMPLE TEST 3: Vikram and Anjali")
    print("="*70)
    
    vikram_data = {
        "name": "Vikram",
        "day": 12,
        "month": 12,
        "year": 1993,
        "birth_time": "19:00",
        "zodiac_sign": matcher.get_zodiac_sign(12, 12),
        "nadi": matcher.calculate_nadi_guna("19:00"),
        "gana": "Manusha",
        "yoni": "Sinha",
        "rajju": "Adi"
    }
    
    anjali_data = {
        "name": "Anjali",
        "day": 5,
        "month": 5,
        "year": 1996,
        "birth_time": "15:20",
        "zodiac_sign": matcher.get_zodiac_sign(5, 5),
        "nadi": matcher.calculate_nadi_guna("15:20"),
        "gana": "Deva",
        "yoni": "Mesha",
        "rajju": "Parivartana"
    }
    
    results3 = matcher.calculate_compatibility(vikram_data, anjali_data)
    matcher.display_results(results3)
    
    # Save all results
    print("\n" + "="*70)
    print("SAVING SAMPLE RESULTS")
    print("="*70)
    
    matcher.save_results(results1, "sample_results_raj_priya.json")
    matcher.save_results(results2, "sample_results_arjun_deepika.json")
    matcher.save_results(results3, "sample_results_vikram_anjali.json")
    
    # Generate comparison report
    print("\n" + "="*70)
    print("COMPATIBILITY SUMMARY COMPARISON")
    print("="*70 + "\n")
    
    comparisons = [
        (results1["boy_name"], results1["girl_name"], results1["total_score"]),
        (results2["boy_name"], results2["girl_name"], results2["total_score"]),
        (results3["boy_name"], results3["girl_name"], results3["total_score"])
    ]
    
    print(f"{'Boy Name':<15} {'Girl Name':<15} {'Score':<10} {'Percentage':<12} {'Rating':<15}")
    print("─" * 67)
    
    for boy, girl, score in comparisons:
        percentage = (score / 36) * 100
        rating, _ = matcher.get_compatibility_interpretation(score)
        print(f"{boy:<15} {girl:<15} {score}/36   {percentage:>6.2f}%      {rating:<15}")


def test_individual_compatibility_functions():
    """Test individual compatibility functions"""
    matcher = AstrologyMatcher()
    
    print("\n" + "="*70)
    print("TESTING INDIVIDUAL COMPATIBILITY FUNCTIONS")
    print("="*70 + "\n")
    
    # Test Nadi compatibility
    print("1. NADI COMPATIBILITY TEST")
    print("─" * 50)
    nadi_combinations = [
        ("Vata", "Vata"),
        ("Vata", "Pitta"),
        ("Pitta", "Kapha"),
        ("Kapha", "Kapha")
    ]
    for nadi1, nadi2 in nadi_combinations:
        score = matcher.calculate_nadi_compatibility(nadi1, nadi2)
        print(f"{nadi1} + {nadi2} = {score}/8")
    
    # Test Gana compatibility
    print("\n2. GANA COMPATIBILITY TEST")
    print("─" * 50)
    gana_combinations = [
        ("Deva", "Deva"),
        ("Deva", "Manusha"),
        ("Manusha", "Rakshasa"),
        ("Rakshasa", "Rakshasa")
    ]
    for gana1, gana2 in gana_combinations:
        score = matcher.calculate_gana_compatibility(gana1, gana2)
        print(f"{gana1} + {gana2} = {score}/6")
    
    # Test Yoni compatibility
    print("\n3. YONI COMPATIBILITY TEST")
    print("─" * 50)
    yoni_combinations = [
        ("Ashwa", "Ashwa"),
        ("Ashwa", "Gaj"),
        ("Sarpa", "Marjara"),
        ("Ashwa", "Sarpa")
    ]
    for yoni1, yoni2 in yoni_combinations:
        score = matcher.calculate_yoni_compatibility(yoni1, yoni2)
        print(f"{yoni1} + {yoni2} = {score}/4")
    
    # Test Rashi compatibility
    print("\n4. RASHI COMPATIBILITY TEST")
    print("─" * 50)
    rashi_combinations = [
        ("Aries", "Leo"),
        ("Taurus", "Virgo"),
        ("Gemini", "Libra"),
        ("Aries", "Capricorn"),
        ("Leo", "Scorpio")
    ]
    for rashi1, rashi2 in rashi_combinations:
        score = matcher.calculate_rashi_compatibility(rashi1, rashi2)
        print(f"{rashi1} + {rashi2} = {score}/7")
    
    # Test Rajju compatibility
    print("\n5. RAJJU COMPATIBILITY TEST")
    print("─" * 50)
    rajju_combinations = [
        ("Adi", "Adi"),
        ("Adi", "Madhya"),
        ("Madhya", "Anta"),
        ("Parivartana", "Adi")
    ]
    for rajju1, rajju2 in rajju_combinations:
        score = matcher.calculate_rajju_compatibility(rajju1, rajju2)
        print(f"{rajju1} + {rajju2} = {score}/8")


def display_zodiac_info():
    """Display zodiac sign information"""
    matcher = AstrologyMatcher()
    
    print("\n" + "="*70)
    print("ZODIAC SIGNS AND COMPATIBILITY")
    print("="*70 + "\n")
    
    for sign, compatible_signs in matcher.RASHI_COMPATIBILITY.items():
        print(f"{sign:<15} → Most compatible with: {', '.join(compatible_signs)}")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("ASTROLOGY MATCHER - SAMPLE TEST SUITE")
    print("="*70)
    
    # Run individual function tests
    test_individual_compatibility_functions()
    
    # Display zodiac info
    display_zodiac_info()
    
    # Run sample matches
    test_sample_matches()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED")
    print("="*70)
    print("\nTo run interactive mode, use: python astrology_matcher.py")


if __name__ == "__main__":
    main()
