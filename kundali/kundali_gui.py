import os
import sys
import json
import webbrowser
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones
from dateutil import parser as dateparser
import requests
import traceback

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QDateEdit, QTimeEdit,
    QTextEdit, QTabWidget, QMessageBox, QProgressBar, QGroupBox, QScrollArea,
    QFormLayout
)
from PyQt5.QtCore import Qt, QDate, QTime, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# --------------------- Configuration ---------------------
API_KEY = os.getenv("FREE_ASTRO_API_KEY",
                    "ZEwB4wfX7PaUfsjhYOawHa8fYymQ760u6iz1iUht")
BASE = "https://json.freeastrologyapi.com"
HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}

DEFAULT_CONFIG = {
    "observation_point": "topocentric",
    "ayanamsha": "lahiri",
    "language": "en"
}


# --------------------- API Functions ---------------------
def call_api(path: str, payload: dict) -> dict:
    url = f"{BASE.rstrip('/')}/{path.lstrip('/')}"
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    except Exception as e:
        raise RuntimeError(f"HTTP request failed: {e}")
    if r.status_code != 200:
        raise RuntimeError(f"API {url} returned {r.status_code}: {r.text}")
    try:
        return r.json()
    except ValueError:
        return {"raw_text": r.text}


def geo_lookup(place: str) -> dict:
    payload = {"location": place}
    resp = call_api("geo-details", payload)
    
    if isinstance(resp, dict) and resp.get("geonames"):
        g = resp["geonames"][0]
        return {
            "latitude": float(g.get("latitude")),
            "longitude": float(g.get("longitude")),
            "timezone_id": g.get("timezone_id"),
            "place_name": g.get("place_name")
        }
    
    if isinstance(resp, dict) and resp.get("output"):
        out = resp["output"]
        return {
            "latitude": float(out.get("latitude")),
            "longitude": float(out.get("longitude")),
            "timezone_id": out.get("timezone_id"),
            "place_name": out.get("place_name", place)
        }
    
    raise RuntimeError("Could not parse geo-details response: " + json.dumps(resp)[:500])


def timezone_offset_hours(tz_name: str, dt: datetime) -> float:
    if tz_name not in available_timezones():
        tz = ZoneInfo(tz_name)
    else:
        tz = ZoneInfo(tz_name)
    localized = dt.replace(tzinfo=tz)
    offset = localized.utcoffset()
    if offset is None:
        raise RuntimeError(f"Could not compute offset for timezone {tz_name}")
    return offset.total_seconds() / 3600.0


def save_svg(svg_text: str, filename: str = "kundali.svg") -> str:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_text)
    return os.path.abspath(filename)


def format_planet_data(planet_output: dict) -> list:
    """Parse and format planet data from API response."""
    out = planet_output.get("output") or planet_output
    rows = []
    
    if isinstance(out, dict):
        if "planets" in out and isinstance(out["planets"], list):
            for p in out["planets"]:
                rows.append(p)
        elif "Ascendant" in out:
            keys = [k for k in out.keys() if isinstance(out[k], dict) and out[k].get("zodiac_sign_name")]
            for k in keys:
                entry = out[k].copy()
                entry["body"] = k
                rows.append(entry)
        else:
            for k, v in out.items():
                if isinstance(v, dict) and v.get("zodiac_sign_name"):
                    entry = v.copy()
                    entry["body"] = k
                    rows.append(entry)
    
    return rows


# --------------------- Worker Thread ---------------------
class KundaliWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, name, dob, time_of_birth, place, tz_offset, is_lat_lon=False):
        super().__init__()
        self.name = name
        self.dob = dob
        self.time_of_birth = time_of_birth
        self.place = place
        self.tz_offset = tz_offset
        self.is_lat_lon = is_lat_lon
    
    def run(self):
        try:
            # Parse date/time
            self.progress.emit("Parsing date and time...")
            dt_str = f"{self.dob} {self.time_of_birth}"
            dt = dateparser.parse(dt_str)
            year = dt.year
            month = dt.month
            date = dt.day
            hours = dt.hour
            minutes = dt.minute
            seconds = dt.second
            
            # Get coordinates
            if self.is_lat_lon:
                self.progress.emit("Using provided coordinates...")
                lat_s, lon_s = self.place.split(",", 1)
                latitude = float(lat_s.strip())
                longitude = float(lon_s.strip())
                timezone_id = None
            else:
                self.progress.emit(f"Looking up location: {self.place}...")
                geo = geo_lookup(self.place)
                latitude = float(geo["latitude"])
                longitude = float(geo["longitude"])
                timezone_id = geo.get("timezone_id")
                self.progress.emit(f"Found: {geo.get('place_name')} | Tz: {timezone_id}")
                
                if timezone_id:
                    self.tz_offset = timezone_offset_hours(timezone_id, dt)
                    self.progress.emit(f"Using timezone offset: {self.tz_offset} hours")
            
            # Build payload
            payload_core = {
                "year": year,
                "month": month,
                "date": date,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": self.tz_offset,
                "settings": DEFAULT_CONFIG,
                "config": DEFAULT_CONFIG
            }
            
            # Get SVG chart
            self.progress.emit("Requesting SVG chart...")
            svg_resp = call_api("horoscope-chart-svg-code", payload_core)
            
            if isinstance(svg_resp, dict) and ("svg" in svg_resp):
                svg_code = svg_resp["svg"]
            elif isinstance(svg_resp, dict) and ("output" in svg_resp) and isinstance(svg_resp["output"], str):
                svg_code = svg_resp["output"]
            elif isinstance(svg_resp, dict) and ("output" in svg_resp) and isinstance(svg_resp["output"], dict) and svg_resp["output"].get("svg"):
                svg_code = svg_resp["output"]["svg"]
            elif isinstance(svg_resp, dict) and svg_resp.get("svg_code"):
                svg_code = svg_resp["svg_code"]
            else:
                svg_code = svg_resp if isinstance(svg_resp, str) else json.dumps(svg_resp)
            
            svg_file = save_svg(svg_code, filename="kundali.svg")
            
            # Get planets data
            self.progress.emit("Requesting planets data...")
            planet_resp = call_api("planets/extended", payload_core)
            
            # Save planet data
            with open("kundali_planets.json", "w", encoding="utf-8") as f:
                json.dump(planet_resp, f, indent=2, ensure_ascii=False)
            
            planet_rows = format_planet_data(planet_resp)
            
            self.progress.emit("Complete!")
            
            self.finished.emit({
                "success": True,
                "svg_file": svg_file,
                "planet_data": planet_rows,
                "latitude": latitude,
                "longitude": longitude,
                "timezone_offset": self.tz_offset,
                "name": self.name
            })
            
        except Exception as e:
            self.error.emit(f"Error: {str(e)}\n\n{traceback.format_exc()}")


# --------------------- Main GUI Window ---------------------
class KundaliGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kundali AI — Vedic Astrology")
        self.setGeometry(100, 100, 1200, 800)
        self.worker = None
        self.svg_file = None
        self.planet_data = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the GUI components."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create main layout with tabs
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.input_tab = self.create_input_tab()
        self.results_tab = self.create_results_tab()
        self.chart_tab = self.create_chart_tab()
        
        self.tabs.addTab(self.input_tab, "Input Details")
        self.tabs.addTab(self.results_tab, "Results")
        self.tabs.addTab(self.chart_tab, "Chart")
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_input_tab(self) -> QWidget:
        """Create the input details tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Scroll area for better UX
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QFormLayout()
        
        # Title
        title = QLabel("Kundali AI — Enter Your Details")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        scroll_layout.addRow(title)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name (optional)")
        scroll_layout.addRow("Name:", self.name_input)
        
        # Date of Birth
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate(2000, 1, 1))
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dddd, MMMM d, yyyy")  # Full format: Monday, January 1, 2000
        scroll_layout.addRow("Date of Birth:", self.date_input)
        
        # Time of Birth
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(0, 0, 0))
        self.time_input.setDisplayFormat("hh:mm:ss AP")  # Full format with AM/PM
        scroll_layout.addRow("Time of Birth:", self.time_input)
        
        # Location input method
        location_group = QGroupBox("Location")
        location_layout = QVBoxLayout()
        
        self.location_type = QComboBox()
        self.location_type.addItems(["City Name", "Latitude & Longitude"])
        self.location_type.currentTextChanged.connect(self.on_location_type_changed)
        location_layout.addWidget(QLabel("Location Type:"))
        location_layout.addWidget(self.location_type)
        
        # City name input
        self.place_input = QLineEdit()
        self.place_input.setPlaceholderText("Enter city name (e.g., New Delhi)")
        location_layout.addWidget(QLabel("City/Place:"))
        location_layout.addWidget(self.place_input)
        
        # Latitude input
        self.latitude_input = QLineEdit()
        self.latitude_input.setPlaceholderText("e.g., 27.7172")
        self.latitude_input.setVisible(False)
        location_layout.addWidget(QLabel("Latitude:"))
        location_layout.addWidget(self.latitude_input)
        
        # Longitude input
        self.longitude_input = QLineEdit()
        self.longitude_input.setPlaceholderText("e.g., 85.3240")
        self.longitude_input.setVisible(False)
        location_layout.addWidget(QLabel("Longitude:"))
        location_layout.addWidget(self.longitude_input)
        
        self.tz_offset_input = QLineEdit()
        self.tz_offset_input.setPlaceholderText("e.g., 5.5 for IST")
        self.tz_offset_input.setText("5.5")
        location_layout.addWidget(QLabel("Timezone Offset (hours):"))
        location_layout.addWidget(self.tz_offset_input)
        
        location_group.setLayout(location_layout)
        scroll_layout.addRow(location_group)
        
        # Submit button
        self.submit_btn = QPushButton("Calculate Kundali")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_btn.clicked.connect(self.calculate_kundali)
        scroll_layout.addRow(self.submit_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        scroll_layout.addRow(self.progress_bar)
        
        # Progress label
        self.progress_label = QLabel("")
        scroll_layout.addRow(self.progress_label)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        widget.setLayout(layout)
        return widget
    
    def create_results_tab(self) -> QWidget:
        """Create the results tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Planetary Positions")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Results table (using text edit for now)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("font-family: Courier; font-size: 10px;")
        layout.addWidget(self.results_text)
        
        # Export button
        export_btn = QPushButton("Export as JSON")
        export_btn.clicked.connect(self.export_json)
        layout.addWidget(export_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_chart_tab(self) -> QWidget:
        """Create the chart tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Title with center alignment
        title = QLabel("Kundali Chart")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Web view for SVG with center alignment
        self.chart_view = QWebEngineView()
        self.chart_view.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ddd;")
        layout.addWidget(self.chart_view, alignment=Qt.AlignCenter)
        
        # Button layout - centered
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        open_btn = QPushButton("Open in Browser")
        open_btn.setMaximumWidth(200)
        open_btn.clicked.connect(self.open_chart_browser)
        button_layout.addWidget(open_btn)

        hindu_btn = QPushButton("Hindu Themed Chart")
        hindu_btn.setMaximumWidth(200)
        hindu_btn.clicked.connect(self.show_hindu_chart)
        button_layout.addWidget(hindu_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def on_location_type_changed(self, text):
        """Update visibility based on location type."""
        if text == "City Name":
            self.place_input.setVisible(True)
            self.latitude_input.setVisible(False)
            self.longitude_input.setVisible(False)
        else:
            self.place_input.setVisible(False)
            self.latitude_input.setVisible(True)
            self.longitude_input.setVisible(True)
    
    def calculate_kundali(self):
        """Calculate kundali by submitting form."""
        # Validate inputs
        name = self.name_input.text().strip()
        dob = self.date_input.date().toString("yyyy-MM-dd")
        time_of_birth = self.time_input.time().toString("hh:mm:ss")
        
        # Determine if using city name or coordinates
        location_type = self.location_type.currentText()
        
        if location_type == "City Name":
            place = self.place_input.text().strip()
            if not place:
                QMessageBox.warning(self, "Validation Error", "Please enter a city/place name.")
                return
            is_lat_lon = False
        else:
            lat = self.latitude_input.text().strip()
            lon = self.longitude_input.text().strip()
            if not lat or not lon:
                QMessageBox.warning(self, "Validation Error", "Please enter both latitude and longitude.")
                return
            try:
                float(lat)
                float(lon)
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Latitude and longitude must be valid numbers.")
                return
            place = f"{lat},{lon}"
            is_lat_lon = True
        
        try:
            tz_offset = float(self.tz_offset_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid timezone offset.")
            return
        
        # Disable button and show progress
        self.submit_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Processing...")
        self.statusBar().showMessage("Calculating kundali...")
        
        # Start worker thread
        self.worker = KundaliWorker(name, dob, time_of_birth, place, tz_offset, is_lat_lon)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_kundali_finished)
        self.worker.error.connect(self.on_kundali_error)
        self.worker.start()
    
    def on_progress(self, message: str):
        """Update progress."""
        self.progress_label.setText(message)
        self.progress_bar.setValue(min(self.progress_bar.value() + 20, 90))
    
    def on_kundali_finished(self, data: dict):
        """Handle successful kundali calculation."""
        if data["success"]:
            self.svg_file = data["svg_file"]
            self.planet_data = data["planet_data"]
            
            # Display results
            self.display_results(data)
            self.display_chart(data["svg_file"])
            
            # Switch to results tab
            self.tabs.setCurrentIndex(1)
            
            QMessageBox.information(self, "Success", "Kundali calculated successfully!")
            self.statusBar().showMessage("Ready")
        
        # Re-enable button
        self.submit_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText("")
    
    def on_kundali_error(self, error: str):
        """Handle kundali calculation error."""
        QMessageBox.critical(self, "Error", error)
        self.submit_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setText("")
        self.statusBar().showMessage("Error occurred")
    
    def display_results(self, data: dict):
        """Display planetary data in results tab."""
        result_text = f"Kundali Results\n"
        result_text += "=" * 80 + "\n\n"
        
        if data["name"]:
            result_text += f"Name: {data['name']}\n"
        
        result_text += f"Latitude: {data['latitude']:.4f}\n"
        result_text += f"Longitude: {data['longitude']:.4f}\n"
        result_text += f"Timezone Offset: {data['timezone_offset']} hours\n"
        result_text += "\n" + "=" * 80 + "\n\n"
        
        result_text += "Planetary Positions (abridged):\n"
        result_text += "-" * 80 + "\n"
        result_text += f"{'Body':<12} {'Sign (deg)':<20} {'House':<8} {'Nakshatra (pada)':<30}\n"
        result_text += "-" * 80 + "\n"
        
        for e in data["planet_data"]:
            body = e.get("body", e.get("name", ""))
            sign_name = e.get("zodiac_sign_name") or e.get("zodiacSignName") or ""
            deg = e.get("fullDegree")
            
            if deg is None:
                deg = e.get("degrees")
                minutes = e.get("minutes")
                if deg is not None and minutes is not None:
                    deg = f"{deg}°{minutes}'"
            else:
                norm = e.get("normDegree")
                if norm is not None:
                    deg = f"{norm:.3f}°"
                else:
                    deg = f"{float(deg):.3f}°"
            
            house = e.get("house_number") or e.get("house") or ""
            nak = ""
            if e.get("nakshatra_name"):
                nak = f"{e.get('nakshatra_name')} ({e.get('nakshatra_number', '')})"
                if e.get("nakshatra_pada"):
                    nak += f" p{e.get('nakshatra_pada')}"
            
            result_text += f"{body:<12} {sign_name+' '+str(deg):<20} {str(house):<8} {nak:<30}\n"
        
        result_text += "-" * 80 + "\n"
        
        self.results_text.setText(result_text)
    
    def display_chart(self, svg_file: str):
        """Display SVG chart in chart tab."""
        try:
            # Prefer loading the SVG file directly — QWebEngineView handles SVG files when loaded via file URL.
            abs_path = os.path.abspath(svg_file)
            self.chart_view.setUrl(QUrl.fromLocalFile(abs_path))
            return
        except Exception:
            pass

        # Fallback: try embedding the SVG content inside an HTML wrapper
        try:
            with open(svg_file, 'r', encoding='utf-8') as f:
                svg_content = f.read()

            # Remove any XML prolog which may interfere when embedding
            if svg_content.lstrip().startswith('<?xml'):
                idx = svg_content.find('?>')
                if idx != -1:
                    svg_content = svg_content[idx+2:]

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset='utf-8'/>
                <style>
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        margin: 0;
                        padding: 10px;
                        background-color: #f0f0f0;
                    }}
                    svg {{
                        max-width: 90%;
                        max-height: 90%;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }}
                </style>
            </head>
            <body>
                {svg_content}
            </body>
            </html>
            """
            self.chart_view.setHtml(html_content, QUrl.fromLocalFile(os.path.dirname(abs_path)))
        except Exception as e:
            self.chart_view.setHtml(f"<p style='text-align: center; margin-top: 50px;'>Could not display chart: {str(e)}</p>")

    def create_hindu_html(self, svg_file: str) -> str:
        """Create a Hindu-themed HTML wrapper around the SVG and return the HTML file path."""
        try:
            with open(svg_file, 'r', encoding='utf-8') as f:
                svg_content = f.read()

            # Strip XML prolog if present
            if svg_content.lstrip().startswith('<?xml'):
                idx = svg_content.find('?>')
                if idx != -1:
                    svg_content = svg_content[idx+2:]

            html = f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kundali — Hindu Themed Chart</title>
  <style>
    html,body {{height:100%; margin:0; padding:0; background: linear-gradient(180deg, #FFF3E0 0%, #FFF8E1 100%); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif}}
    .frame {{
      max-width: 1000px; margin: 28px auto; padding: 24px; background: rgba(255,255,255,0.95); border-radius: 18px; box-shadow: 0 8px 30px rgba(0,0,0,0.12);
      border: 6px solid #F9E0B2; position: relative;
    }}
    .om {{ position: absolute; left:50%; top:8%; transform: translateX(-50%); font-size:120px; color: rgba(165,36,61,0.08); font-family: serif; pointer-events:none }}
    .header {{text-align:center; color:#A5243D; font-weight:700; margin-bottom:12px; font-size:22px}}
    .sub {{text-align:center; color:#2A3D45; margin-bottom:18px}}
    .svg-wrap {{display:flex; justify-content:center; align-items:center;}}
    .decor-top, .decor-bottom {{height:20px; background: repeating-linear-gradient(90deg, #FDD692 0 10px, #F6A623 10px 20px); border-radius:8px}}
    .mantra {{text-align:center; color:#7A4B2B; margin-top:14px; font-style:italic}}
    @media (max-width:800px) {{ .om {{font-size:80px; top:6%}} .frame{{margin:12px}} }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="om">ॐ</div>
    <div class="header">Rasi Chart — Divine Presentation</div>
    <div class="sub">A sacred view of planetary positions — may it bring clarity and peace</div>
    <div class="svg-wrap">{svg_content}</div>
    <div class="mantra">ॐ श्री गणेशाय नमः — Om Shri Ganeshaaya Namah</div>
  </div>
</body>
</html>'''

            out_path = os.path.abspath('kundali_hindu.html')
            with open(out_path, 'w', encoding='utf-8') as out:
                out.write(html)
            return out_path
        except Exception:
            return ''

    def show_hindu_chart(self):
        """Generate and display the Hindu-themed chart in the web view (or show error)."""
        if not self.svg_file or not os.path.exists(self.svg_file):
            QMessageBox.warning(self, "Warning", "No chart available. Please calculate kundali first.")
            return

        html_path = self.create_hindu_html(self.svg_file)
        if not html_path:
            QMessageBox.critical(self, "Error", "Could not generate Hindu-themed chart.")
            return

        try:
            self.chart_view.setUrl(QUrl.fromLocalFile(html_path))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not display Hindu-themed chart: {str(e)}")
    
    def open_chart_browser(self):
        """Open chart in default browser."""
        if self.svg_file:
            try:
                webbrowser.open("file://" + os.path.abspath(self.svg_file))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open browser: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No chart available. Please calculate kundali first.")
    
    def export_json(self):
        """Export planet data as JSON."""
        if not self.planet_data:
            QMessageBox.warning(self, "Warning", "No data to export. Please calculate kundali first.")
            return
        
        try:
            with open("kundali_export.json", "w", encoding="utf-8") as f:
                json.dump(self.planet_data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Success", "Data exported to kundali_export.json")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not export: {str(e)}")


# --------------------- Main ---------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set app style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = KundaliGUI()
    window.show()
    
    sys.exit(app.exec_())
