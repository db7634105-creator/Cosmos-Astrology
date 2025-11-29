# Astrologers Directory Application

A Python-based GUI application that displays a directory of astrologers with their profiles, photos, and call functionality.

## Features

✨ **Profile Cards**: Display astrologers in an attractive grid layout with:
- Profile photo
- Name and specialization
- Experience and rating
- Call Now button
- View Profile button

📞 **Call Functionality**: 
- Click "Call Now" to initiate a phone call
- Confirmation dialog before calling
- Call history logging

🎨 **User-Friendly Interface**:
- Responsive grid layout (3 columns)
- Smooth scrolling
- Professional styling
- Placeholder images for missing photos

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Navigate to the project directory:
   ```
   cd "c:\Users\dines\OneDrive\Documents\Astrologers"
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python main.py
```

## Project Structure

```
Astrologers/
├── main.py                 # Main GUI application
├── astrologers_data.py     # Sample astrologer data
├── call_handler.py         # Phone call functionality
├── image_utils.py          # Image loading and processing
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── assets/                # Folder for astrologer photos
    ├── astrologer1.jpg
    ├── astrologer2.jpg
    └── ... (more photos)
```

## How to Use

1. **Browse Astrologers**: Scroll through the list of available astrologers
2. **View Details**: Click "View Profile" to see full details of an astrologer
3. **Make a Call**: 
   - Click "Call Now" button on any astrologer card
   - Confirm the call in the dialog box
   - The system will initiate the call

## Adding Astrologer Photos

1. Create an `assets` folder in the project directory if it doesn't exist
2. Add astrologer photos with names: `astrologer1.jpg`, `astrologer2.jpg`, etc.
3. Alternatively, modify `astrologers_data.py` to point to your image locations

## Customization

### Adding More Astrologers

Edit `astrologers_data.py` and add new entries to the `ASTROLOGERS` list:

```python
{
    "id": 7,
    "name": "Your Astrologer Name",
    "specialization": "Your Specialty",
    "experience": "X years",
    "phone": "+91-XXXXXXXXXX",
    "rating": 4.5,
    "image_url": "assets/astrologer7.jpg"
}
```

### Modifying Styling

Edit the color values in `main.py`:
- Primary color: `#4a3f8f` (Purple)
- Accent color: `#ff9800` (Orange)
- Text color: `#333333` (Dark Gray)

## Features in Detail

### Call Functionality
- Uses the `tel:` protocol to open system phone dialer
- Logs all calls to `call_history.log`
- Shows confirmation dialog before placing call

### Image Handling
- Supports JPG, PNG, and other image formats
- Auto-generates placeholder images if photo is missing
- Automatically resizes images to fit card layout

### Data Management
- Sample data included for demonstration
- Easy to integrate with databases
- Call history tracking

## Troubleshooting

**Issue**: PIL Import Error
- Solution: Run `pip install Pillow`

**Issue**: Images not loading
- Solution: Ensure images are in the `assets/` folder and named correctly

**Issue**: Call not working
- Solution: 
  - Ensure phone dialer is available on your system
  - Check phone number format is correct
  - On some systems, tel: protocol may require additional setup

## Future Enhancements

- Integration with actual VoIP services
- Database storage for astrologer profiles
- User authentication and booking system
- Payment integration
- Chat functionality
- Appointment scheduling
- Reviews and ratings system
- Advanced search and filtering

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, please refer to the inline code comments and documentation.

---

**Created**: 2025
**Version**: 1.0
