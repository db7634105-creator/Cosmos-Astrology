# Kundali AI — GUI Interface

## Overview
This is a modern graphical user interface (GUI) for the Kundali AI application, built with PyQt5. It provides an easy-to-use interface for calculating Vedic astrology kundali charts.

## Features

✅ **Modern GUI Interface** - Clean, intuitive design  
✅ **Input Form** - Easy data entry for name, date, time, and location  
✅ **Location Lookup** - Automatic geocoding for city names  
✅ **Timezone Handling** - Automatic or manual timezone offset  
✅ **Real-time Calculations** - Background processing with progress updates  
✅ **SVG Chart Display** - View kundali charts directly in the app  
✅ **Planetary Data** - Detailed planetary positions with signs and nakshatras  
✅ **Export Options** - Save results as JSON  
✅ **Multi-tab Interface** - Organized input, results, and chart viewing  

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Install Dependencies**
   ```bash
   cd c:\Users\asus\OneDrive\Desktop\KundaliAI\Cosmos-Astrology\kundali
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "import PyQt5; print('PyQt5 installed successfully')"
   ```

## Usage

### Running the GUI Application

```bash
python kundali_gui.py
```

This will launch the Kundali AI GUI window.

### Using the Application

#### 1. **Input Details Tab**
   - **Name**: Enter your name (optional)
   - **Date of Birth**: Select your birth date using the calendar picker
   - **Time of Birth**: Select your birth time (or use 00:00:00 if unknown)
   - **Location Type**: Choose between city name or coordinates
   - **Location**: 
     - For city names: Enter city name (e.g., "New Delhi")
     - For coordinates: Enter as "latitude,longitude" (e.g., "27.7172,85.3240")
   - **Timezone Offset**: For city names, this is auto-detected; for coordinates, enter manually (e.g., 5.5 for IST)

#### 2. **Calculate Kundali**
   - Click the "Calculate Kundali" button
   - The app will show progress updates
   - Wait for processing to complete

#### 3. **Results Tab**
   - View planetary positions for all celestial bodies
   - Includes zodiac signs, degrees, houses, and nakshatras
   - Export results as JSON

#### 4. **Chart Tab**
   - View the SVG kundali chart
   - Click "Open in Browser" to view in full screen

## File Structure

```
kundali/
├── kundali_gui.py              # Main GUI application
├── kundali_ai.py               # Original CLI application
├── requirements.txt            # Python dependencies
├── kundali.svg                 # Generated chart (output)
├── kundali_planets.json        # Detailed planet data (output)
├── kundali_export.json         # Exported results (output)
└── input.txt                   # Sample input data
```

## System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: 512 MB minimum
- **Disk Space**: 100 MB for dependencies
- **Internet**: Required for API calls

## Troubleshooting

### "Module not found" Error
```bash
pip install PyQt5 PyQtWebEngine requests python-dateutil
```

### "API key invalid"
The application uses a default API key. If you have your own Free Astrology API key:
```bash
# On Windows CMD
set FREE_ASTRO_API_KEY=your_api_key_here

# Then run the app
python kundali_gui.py
```

### GUI Not Appearing
Make sure you have a display server running. On Linux/WSL:
```bash
export DISPLAY=:0
python kundali_gui.py
```

### Timezone Offset Issues
- For city lookup: The app automatically determines timezone
- For coordinates: Manually enter offset in hours (e.g., 5.5 for IST, -5 for EST)

## Keyboard Shortcuts

- `Ctrl+Q`: Close application
- `Tab`: Navigate between input fields

## API Information

The application uses the Free Astrology API:
- **Base URL**: https://json.freeastrologyapi.com
- **Endpoints Used**:
  - `geo-details`: Location lookup
  - `horoscope-chart-svg-code`: SVG chart generation
  - `planets/extended`: Detailed planetary data

## Output Files

After calculating a kundali, the app generates:

1. **kundali.svg** - Visual chart in SVG format
2. **kundali_planets.json** - Complete planetary data
3. **kundali_export.json** - Exported results (when using Export button)

## CLI Alternative

For command-line usage, use the original CLI application:
```bash
python kundali_ai.py
```

## Known Limitations

- Some locations may not be found in the geocoding database
- API responses depend on Free Astrology API availability
- Large SVG charts may take time to render

## Support

For issues or feature requests, check the main project documentation.

## License

This project is part of the Cosmos-Astrology suite.

---

**Enjoy calculating your kundali!** 🌟
