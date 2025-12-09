"""
Astrologers Data Module
Contains sample astrologer data with contact information
"""

ASTROLOGERS = [
    {
        "id": 1,
        "name": "Dinesh Bohara",
        "specialization": "Vedic Astrology",
        "experience": "15 years",
        "phone": "+977-9769899316",
        "rating": 4.8,
        "image_url": "assets/d.jpg",
        "price_per_minute": 0,
        "available": True,
        "is_free": True,
        "packages": []
    },
    {
        "id": 2,
        "name": "Anil Adhikari",
        "specialization": "Astrology",
        "experience": "12 years",
        "phone": "+977-9866148226",
        "rating": 4.7,
        "image_url": "assets/a.jpg",
        "price_per_minute": 0,
        "available": True,
        "is_free": True,
        "packages": []
    },
    {
        "id": 3,
        "name": "Sahil Chhetri",
        "specialization": "Western Astrology",
        "experience": "18 years",
        "phone": "+977-0967900593",
        "rating": 4.9,
        "image_url": "assets/astrologer3.jpg",
        "price_per_minute": 50,
        "available": True,
        "is_free": False,
        "packages": [
            {"name": "5 min", "duration": 5, "price": 250},
            {"name": "15 min", "duration": 15, "price": 700},
            {"name": "30 min", "duration": 30, "price": 1300}
        ]
    },
    {
        "id": 4,
        "name": "Deepa Verma",
        "specialization": "Horoscope Reading",
        "experience": "10 years",
        "phone": "+977-9876543213",
        "rating": 4.6,
        "image_url": "assets/astrologer4.jpg",
        "price_per_minute": 40,
        "available": True,
        "is_free": False,
        "packages": [
            {"name": "5 min", "duration": 5, "price": 200},
            {"name": "15 min", "duration": 15, "price": 550},
            {"name": "30 min", "duration": 30, "price": 1000}
        ]
    },
    {
        "id": 5,
        "name": "Vikram Singh",
        "specialization": "Planetary Analysis",
        "experience": "20 years",
        "phone": "+977-9876543214",
        "rating": 5.0,
        "image_url": "assets/astrologer5.jpg",
        "price_per_minute": 60,
        "available": True,
        "is_free": False,
        "packages": [
            {"name": "5 min", "duration": 5, "price": 300},
            {"name": "15 min", "duration": 15, "price": 850},
            {"name": "30 min", "duration": 30, "price": 1500}
        ]
    },
    {
        "id": 6,
        "name": "Neha Gupta",
        "specialization": "Astrology & Counseling",
        "experience": "14 years",
        "phone": "+977-9876543215",
        "rating": 4.7,
        "image_url": "assets/astrologer6.jpg",
        "price_per_minute": 45,
        "available": True,
        "is_free": False,
        "packages": [
            {"name": "5 min", "duration": 5, "price": 225},
            {"name": "15 min", "duration": 15, "price": 630},
            {"name": "30 min", "duration": 30, "price": 1150}
        ]
    }
]
