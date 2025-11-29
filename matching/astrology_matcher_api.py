"""
Enhanced Astrology Compatibility Matcher with FreeAstrology API Integration
Uses Ashtakoot Score API for professional matching + local Guna Milan system

Ashtakoot Matching Factors (8 Kootas - 36 points):
1. Varna Kootam (1 pt) - Caste/Quality
2. Vasya Kootam (2 pts) - Control/Dominance
3. Tara Kootam (3 pts) - Star/Longevity
4. Yoni Kootam (4 pts) - Sexual Compatibility
5. Graha Maitri Kootam (5 pts) - Planetary Friendship
6. Gana Kootam (6 pts) - Nature/Temperament
7. Rasi Kootam (7 pts) - Moon Sign Compatibility
8. Nadi Kootam (8 pts) - Health/Heredity
"""

import requests
import json
from datetime import datetime
from typing import Dict, Tuple, Optional
import time


class EnhancedAstrologyMatcher:
    """Enhanced matcher using FreeAstrology API and local calculations"""
    
    # API Configuration
    API_BASE_URL = "https://json.freeastrologyapi.com/match-making/ashtakoot-score"
    API_KEY = "DiA8MzlbeP9zQHZfCBFi69bMPWYDweB78H3pii6B"
    
    # Timezone database (city -> timezone offset)
    TIMEZONES = {
        "delhi": 5.5, "mumbai": 5.5, "bangalore": 5.5, "kolkata": 5.5,
        "hyderabad": 5.5, "pune": 5.5, "ahmedabad": 5.5, "jaipur": 5.5,
        "lucknow": 5.5, "kanpur": 5.5, "indore": 5.5, "goa": 5.5,
        "uttar_pradesh": 5.5, "maharashtra": 5.5, "karnataka": 5.5,
        "london": 0, "new_york": -5, "los_angeles": -8, "toronto": -5,
        "sydney": 10, "dubai": 4, "singapore": 8, "bangkok": 7,
        "hong_kong": 8, "tokyo": 9, "mumbai": 5.5, "default": 5.5
    }
    
    # Lat/Long database (major cities)
    LOCATIONS = {
        "delhi": (28.6139, 77.2090),
        "mumbai": (19.0760, 72.8777),
        "bangalore": (12.9716, 77.5946),
        "hyderabad": (17.3850, 78.4867),
        "kolkata": (22.5726, 88.3639),
        "pune": (18.5204, 73.8567),
        "ahmedabad": (23.0225, 72.5714),
        "jaipur": (26.9124, 75.7873),
        "lucknow": (26.8467, 80.9462),
        "indore": (22.7196, 75.8577),
        "default": (28.6139, 77.2090)  # Default to Delhi
    }
    
    def __init__(self):
        """Initialize the enhanced matcher"""
        self.boy_data = {}
        self.girl_data = {}
        self.api_response = {}
        self.local_results = {}
        
    def validate_date(self, day: int, month: int, year: int) -> bool:
        """Validate date"""
        try:
            datetime(year, month, day)
            return True
        except ValueError:
            return False
    
    def get_coordinates_and_timezone(self, city: str) -> Tuple[float, float, float]:
        """Get latitude, longitude, and timezone for a city"""
        city_lower = city.lower().strip()
        
        if city_lower in self.LOCATIONS:
            lat, lon = self.LOCATIONS[city_lower]
            tz = self.TIMEZONES.get(city_lower, 5.5)
        else:
            lat, lon = self.LOCATIONS["default"]
            tz = self.TIMEZONES.get("default", 5.5)
        
        return lat, lon, tz
    
    def input_person_details(self, person_type: str = "Groom") -> Dict:
        """Input details for a person with location support"""
        print(f"\n{'='*60}")
        print(f"Enter {person_type}'s Details")
        print(f"{'='*60}\n")
        
        data = {}
        data["name"] = input(f"Enter {person_type}'s name: ").strip()
        data["gender"] = "male" if person_type.lower() == "groom" else "female"
        
        # Birth Date
        while True:
            try:
                birth_date = input(f"Enter birth date (DD/MM/YYYY): ").strip()
                day, month, year = map(int, birth_date.split("/"))
                if self.validate_date(day, month, year):
                    data["date"] = day
                    data["month"] = month
                    data["year"] = year
                    break
                else:
                    print("Invalid date. Please try again.")
            except ValueError:
                print("Invalid format. Please use DD/MM/YYYY")
        
        # Birth Time
        while True:
            try:
                birth_time = input(f"Enter birth time (HH:MM:SS in 24-hour format): ").strip()
                parts = birth_time.split(":")
                if len(parts) == 3:
                    hour, minute, second = map(int, parts)
                    if 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59:
                        data["hours"] = hour
                        data["minutes"] = minute
                        data["seconds"] = second
                        break
                    else:
                        print("Invalid time. Please use valid ranges.")
                else:
                    print("Invalid format. Please use HH:MM:SS")
            except ValueError:
                print("Invalid format. Please use HH:MM:SS")
        
        # Birth Location
        city = input(f"Enter birth city (e.g., Delhi, Mumbai, Bangalore): ").strip()
        lat, lon, tz = self.get_coordinates_and_timezone(city)
        
        data["city"] = city
        data["latitude"] = lat
        data["longitude"] = lon
        data["timezone"] = tz
        
        return data
    
    def call_ashtakoot_api(self, boy_data: Dict, girl_data: Dict) -> Optional[Dict]:
        """Call the FreeAstrology API for Ashtakoot matching"""
        print("\n" + "="*60)
        print("Connecting to FreeAstrology API...")
        print("="*60)
        
        # Prepare request payload
        payload = {
            "male": {
                "year": boy_data["year"],
                "month": boy_data["month"],
                "date": boy_data["date"],
                "hours": boy_data["hours"],
                "minutes": boy_data["minutes"],
                "seconds": boy_data["seconds"],
                "latitude": boy_data["latitude"],
                "longitude": boy_data["longitude"],
                "timezone": boy_data["timezone"]
            },
            "female": {
                "year": girl_data["year"],
                "month": girl_data["month"],
                "date": girl_data["date"],
                "hours": girl_data["hours"],
                "minutes": girl_data["minutes"],
                "seconds": girl_data["seconds"],
                "latitude": girl_data["latitude"],
                "longitude": girl_data["longitude"],
                "timezone": girl_data["timezone"]
            },
            "config": {
                "observation_point": "topocentric",
                "language": "en",
                "ayanamsha": "lahiri"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.API_KEY
        }
        
        try:
            response = requests.post(self.API_BASE_URL, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✓ API Connected Successfully!")
                return response.json()
            else:
                print(f"✗ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection Error: {str(e)}")
            return None
    
    def format_ashtakoot_results(self, api_response: Dict, boy_name: str, girl_name: str) -> Dict:
        """Format and extract Ashtakoot API response"""
        try:
            if api_response.get("statusCode") != 200:
                return None
            
            output = api_response.get("output", {})
            total_score = output.get("total_score", 0)
            out_of = output.get("out_of", 36)
            
            results = {
                "boy_name": boy_name,
                "girl_name": girl_name,
                "total_score": total_score,
                "out_of": out_of,
                "percentage": round((total_score / out_of) * 100, 2),
                "kootas": {}
            }
            
            # Extract all 8 Kootas
            kootas_mapping = {
                "varna_kootam": {"name": "Varna Kootam", "desc": "Caste/Quality Compatibility"},
                "vasya_kootam": {"name": "Vasya Kootam", "desc": "Control/Dominance"},
                "tara_kootam": {"name": "Tara Kootam", "desc": "Star/Longevity"},
                "yoni_kootam": {"name": "Yoni Kootam", "desc": "Sexual Compatibility"},
                "graha_maitri_kootam": {"name": "Graha Maitri Kootam", "desc": "Planetary Friendship"},
                "gana_kootam": {"name": "Gana Kootam", "desc": "Nature/Temperament"},
                "rasi_kootam": {"name": "Rasi Kootam", "desc": "Moon Sign Compatibility"},
                "nadi_kootam": {"name": "Nadi Kootam", "desc": "Health/Heredity"}
            }
            
            for key, info in kootas_mapping.items():
                if key in output:
                    koota_data = output[key]
                    results["kootas"][key] = {
                        "name": info["name"],
                        "description": info["desc"],
                        "score": koota_data.get("score", 0),
                        "out_of": koota_data.get("out_of", 0),
                        "bride_details": koota_data.get("bride", {}),
                        "groom_details": koota_data.get("groom", {})
                    }
            
            return results
        except Exception as e:
            print(f"Error formatting results: {str(e)}")
            return None
    
    def get_compatibility_interpretation(self, score: float, max_score: float = 36) -> Tuple[str, str]:
        """Get interpretation based on score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 89:
            return "Excellent", "Outstanding compatibility - Highly recommended match"
        elif percentage >= 78:
            return "Very Good", "Strong compatibility - A very good match"
        elif percentage >= 67:
            return "Good", "Decent compatibility - Good match with some considerations"
        elif percentage >= 50:
            return "Average", "Moderate compatibility - Requires mutual understanding"
        elif percentage >= 33:
            return "Below Average", "Low compatibility - Significant challenges ahead"
        else:
            return "Poor", "Very poor compatibility - Not recommended match"
    
    def display_ashtakoot_results(self, results: Dict):
        """Display formatted Ashtakoot API results"""
        print(f"\n{'='*80}")
        print(f"{'ASHTAKOOT MATCHING REPORT':^80}")
        print(f"{'(Using FreeAstrology API)':^80}")
        print(f"{'='*80}\n")
        
        print(f"Groom: {results['boy_name']:<35} Bride: {results['girl_name']}")
        print(f"\n{'─'*80}")
        
        compatibility_type, interpretation = self.get_compatibility_interpretation(
            results['total_score'], 
            results['out_of']
        )
        
        print(f"\n{'OVERALL COMPATIBILITY':^80}")
        print(f"{'─'*80}")
        print(f"Total Score: {results['total_score']}/{results['out_of']} ({results['percentage']}%)")
        print(f"Rating: {compatibility_type} - {interpretation}")
        
        print(f"\n{'─'*80}")
        print(f"{'DETAILED KOOTA BREAKDOWN (8 Factors)':^80}")
        print(f"{'─'*80}\n")
        
        for koota_key, koota in results['kootas'].items():
            score = koota['score']
            max_score = koota['out_of']
            name = koota['name']
            desc = koota['description']
            
            # Progress bar
            bar_length = 30
            filled = int((score / max_score) * bar_length) if max_score > 0 else 0
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"{name} ({desc})")
            print(f"Score: {score}/{max_score} {bar}")
            
            # Display koota-specific details
            if koota['bride_details']:
                bride_info = koota['bride_details']
                print(f"  Bride: ", end="")
                
                if 'moon_sign' in bride_info:
                    print(f"Moon Sign: {bride_info.get('moon_sign', 'N/A')}", end="")
                if 'varnam_name' in bride_info:
                    print(f" Varna: {bride_info.get('varnam_name', 'N/A')}", end="")
                if 'yoni' in bride_info:
                    print(f" Yoni: {bride_info.get('yoni', 'N/A')}", end="")
                if 'star_name' in bride_info:
                    print(f" Star: {bride_info.get('star_name', 'N/A')}", end="")
                if 'bride_nadi_name' in bride_info:
                    print(f" Nadi: {bride_info.get('bride_nadi_name', 'N/A')}", end="")
                if 'nadi_name' in bride_info:
                    print(f" Nadi: {bride_info.get('nadi_name', 'N/A')}", end="")
                print()
            
            if koota['groom_details']:
                groom_info = koota['groom_details']
                print(f"  Groom: ", end="")
                
                if 'moon_sign' in groom_info:
                    print(f"Moon Sign: {groom_info.get('moon_sign', 'N/A')}", end="")
                if 'varnam_name' in groom_info:
                    print(f" Varna: {groom_info.get('varnam_name', 'N/A')}", end="")
                if 'yoni' in groom_info:
                    print(f" Yoni: {groom_info.get('yoni', 'N/A')}", end="")
                if 'star_name' in groom_info:
                    print(f" Star: {groom_info.get('star_name', 'N/A')}", end="")
                if 'groom_nadi_name' in groom_info:
                    print(f" Nadi: {groom_info.get('groom_nadi_name', 'N/A')}", end="")
                if 'nadi_name' in groom_info:
                    print(f" Nadi: {groom_info.get('nadi_name', 'N/A')}", end="")
                print()
            
            print()
        
        print(f"{'─'*80}\n")
    
    def save_results(self, results: Dict, filename: str = "ashtakoot_results.json"):
        """Save results to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✓ Results saved to {filename}")
            return True
        except Exception as e:
            print(f"✗ Error saving file: {str(e)}")
            return False
    
    def run(self):
        """Run the enhanced matching program"""
        print("\n" + "="*80)
        print(f"{'ENHANCED ASTROLOGY COMPATIBILITY MATCHER':^80}")
        print(f"{'Powered by FreeAstrology API (Ashtakoot Score)':^80}")
        print(f"{'8-Factor Matching System - 36 Points':^80}")
        print("="*80)
        
        # Input groom details
        self.boy_data = self.input_person_details("Groom")
        print("\n✓ Groom details recorded")
        
        # Input bride details
        self.girl_data = self.input_person_details("Bride")
        print("\n✓ Bride details recorded")
        
        # Call API
        api_response = self.call_ashtakoot_api(self.boy_data, self.girl_data)
        
        if api_response:
            # Format results
            results = self.format_ashtakoot_results(
                api_response,
                self.boy_data["name"],
                self.girl_data["name"]
            )
            
            if results:
                # Display results
                self.display_ashtakoot_results(results)
                
                # Save option
                save = input("Would you like to save the results? (yes/no): ").strip().lower()
                if save in ['yes', 'y']:
                    default_name = f"ashtakoot_{self.boy_data['name']}_{self.girl_data['name']}.json"
                    filename = input(f"Enter filename (default: {default_name}): ").strip()
                    if not filename:
                        filename = default_name
                    self.save_results(results, filename)
            else:
                print("\n✗ Error formatting results from API")
        else:
            print("\n✗ Could not connect to API. Please check your internet connection.")
        
        # Another match option
        another = input("\nWould you like to check another match? (yes/no): ").strip().lower()
        if another in ['yes', 'y']:
            self.run()
        else:
            print("\n" + "="*80)
            print("Thank you for using Enhanced Astrology Compatibility Matcher!")
            print("="*80 + "\n")


def main():
    """Main entry point"""
    try:
        matcher = EnhancedAstrologyMatcher()
        matcher.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
