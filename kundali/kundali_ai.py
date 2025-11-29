import os
import sys
import json
import webbrowser
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones
from dateutil import parser as dateparser

import requests

# --------------------- Configuration ---------------------
API_KEY = os.getenv("FREE_ASTRO_API_KEY",
                    "ZEwB4wfX7PaUfsjhYOawHa8fYymQ760u6iz1iUht")  # <--- your key (you provided it)
BASE = "https://json.freeastrologyapi.com"
HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}

# Default chart config
DEFAULT_CONFIG = {
    "observation_point": "topocentric",
    "ayanamsha": "lahiri",
    "language": "en"
}

# --------------------- Helpers ---------------------
def call_api(path: str, payload: dict) -> dict:
    url = f"{BASE.rstrip('/')}/{path.lstrip('/')}"
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    except Exception as e:
        raise RuntimeError(f"HTTP request failed: {e}")
    if r.status_code != 200:
        # show response body for debugging
        raise RuntimeError(f"API {url} returned {r.status_code}: {r.text}")
    try:
        return r.json()
    except ValueError:
        return {"raw_text": r.text}


def geo_lookup(place: str) -> dict:
    """
    Calls geo-details and returns a dict like { 'latitude': .., 'longitude': .., 'timezone_id': .., 'place_name': .. }
    """
    payload = {"location": place}
    resp = call_api("geo-details", payload)
    # Some responses may be shaped with a 'geonames' array; handle common shapes:
    if isinstance(resp, dict) and resp.get("geonames"):
        g = resp["geonames"][0]
        return {
            "latitude": float(g.get("latitude")),
            "longitude": float(g.get("longitude")),
            "timezone_id": g.get("timezone_id"),
            "place_name": g.get("place_name")
        }
    # fallback: try direct fields
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
    """
    Given a tz name (eg 'Asia/Kolkata') and a naive datetime dt (representing local), return numeric offset in hours (e.g. 5.5)
    """
    if tz_name not in available_timezones():
        # If zoneinfo doesn't know it, try ZoneInfo anyway (it may still work)
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


def pretty_print_planets(planet_output: dict):
    """
    Given the response from planets/extended (it has output.*), print a formatted summary.
    We'll try to read output['planets'] or output keys; docs show 'output' contains entries.
    """
    out = planet_output.get("output") or planet_output
    # Try to find a planets list inside 'output' keys:
    # Many responses include planet names as keys (Sun, Moon, etc.) or an array.
    # We'll handle a few common shapes.
    rows = []
    if isinstance(out, dict):
        # if keys like 'Sun', 'Moon' exist, gather them
        planet_keys = [k for k in out.keys() if k.lower() not in ("statuscode", "status", "ascendant", "house", "output")]
        # prefer 'planets' array if present
        if "planets" in out and isinstance(out["planets"], list):
            for p in out["planets"]:
                rows.append(p)
        elif "Ascendant" in out:
            # The sample in docs shows output contains Ascendant and other objects
            # find keys that look like planets + ascendant
            keys = [k for k in out.keys() if isinstance(out[k], dict) and out[k].get("zodiac_sign_name")]
            for k in keys:
                entry = out[k].copy()
                entry["body"] = k
                rows.append(entry)
        else:
            # fallback: if each key contains dict with 'zodiac_sign_name' etc.
            for k, v in out.items():
                if isinstance(v, dict) and v.get("zodiac_sign_name"):
                    entry = v.copy()
                    entry["body"] = k
                    rows.append(entry)

    # Print header
    print("\nKundali — Planetary positions (abridged):")
    print("-" * 72)
    print(f"{'Body':<12} {'Sign (deg)':<18} {'House':<6} {'Nakshatra (pada)':<26}")
    print("-" * 72)
    for e in rows:
        body = e.get("body", e.get("name", ""))
        sign_name = e.get("zodiac_sign_name") or e.get("zodiacSignName") or ""
        deg = e.get("fullDegree")  # full deg as float
        if deg is None:
            deg = e.get("degrees")
            minutes = e.get("minutes")
            sec = e.get("seconds")
            if deg is not None and minutes is not None:
                deg = f"{deg}°{minutes}'"
        else:
            # convert to "SignName deg"
            norm = e.get("normDegree")
            if norm is not None:
                deg = f"{norm:.3f}°"
            else:
                deg = f"{float(deg):.3f}°"
        house = e.get("house_number") or e.get("house")
        nak = ""
        if e.get("nakshatra_name"):
            nak = f"{e.get('nakshatra_name')} ({e.get('nakshatra_number', '')})"
            if e.get("nakshatra_pada"):
                nak += f" p{e.get('nakshatra_pada')}"
        print(f"{body:<12} {sign_name+' '+str(deg):<18} {str(house):<6} {nak:<26}")
    print("-" * 72)
    print()


# --------------------- Main Flow ---------------------
def main():
    print("Kundali AI — quick Vedic kundali (uses Free Astrology API)")
    print("Enter details. You can give place name (e.g. 'New Delhi') or latitude,longitude.")
    name = input("Name (optional): ").strip()
    dob_raw = input("Date of birth (YYYY-MM-DD): ").strip()
    time_raw = input("Time of birth (HH:MM or HH:MM:SS) — if unknown give 00:00:00: ").strip() or "00:00:00"
    place_raw = input("Place (city name) OR 'lat,lon' (e.g. 27.7172,85.3240): ").strip()

    # parse date/time
    try:
        # combine and parse into a datetime
        dt_str = dob_raw + " " + time_raw
        dt = dateparser.parse(dt_str)
        year = dt.year
        month = dt.month
        date = dt.day
        hours = dt.hour
        minutes = dt.minute
        seconds = dt.second
    except Exception as e:
        print("Couldn't parse date/time:", e)
        sys.exit(1)

    # get lat/lon and timezone
    if "," in place_raw:
        try:
            lat_s, lon_s = place_raw.split(",", 1)
            latitude = float(lat_s.strip())
            longitude = float(lon_s.strip())
            timezone_id = None
            # We can try to infer timezone using zoneinfo from lat/lon but that requires extra services.
            # Ask user for timezone offset
            tz_offset_input = input("Enter timezone offset for that location (e.g. 5.5 for IST) or blank to assume 0: ").strip()
            if tz_offset_input:
                tz_offset = float(tz_offset_input)
            else:
                tz_offset = 0.0
        except Exception as e:
            print("Couldn't parse lat,lon:", e)
            sys.exit(1)
    else:
        # call geo-details
        try:
            geo = geo_lookup(place_raw)
            latitude = float(geo["latitude"])
            longitude = float(geo["longitude"])
            timezone_id = geo.get("timezone_id")
            print(f"Resolved place to {geo.get('place_name', place_raw)} -> lat {latitude}, lon {longitude}, tz {timezone_id}")
            # compute numeric offset for the birth datetime
            tz_offset = timezone_offset_hours(timezone_id, dt)
            print(f"Using timezone offset: {tz_offset} hours (from zone {timezone_id})")
        except Exception as e:
            print("Geo lookup failed:", e)
            tz_offset_input = input("Enter timezone offset manually (e.g. 5.5 for IST): ").strip()
            tz_offset = float(tz_offset_input or 0.0)
            lat_input = input("Enter latitude: ").strip()
            lon_input = input("Enter longitude: ").strip()
            latitude = float(lat_input or 0.0)
            longitude = float(lon_input or 0.0)

    # build core payload
    payload_core = {
        "year": year,
        "month": month,
        "date": date,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": tz_offset,
    }

    # add default settings/config
    # planets/extended shows 'settings' while charts examples use 'config' — send both to be robust
    payload_core["settings"] = DEFAULT_CONFIG
    payload_core["config"] = DEFAULT_CONFIG

    # 1) get SVG chart
    try:
        print("Requesting SVG chart from API...")
        svg_resp = call_api("horoscope-chart-svg-code", payload_core)
        # The endpoint often returns a JSON with a key that contains the SVG string.
        if isinstance(svg_resp, dict) and ("svg" in svg_resp):
            svg_code = svg_resp["svg"]
        elif isinstance(svg_resp, dict) and ("output" in svg_resp) and isinstance(svg_resp["output"], str):
            svg_code = svg_resp["output"]
        elif isinstance(svg_resp, dict) and ("output" in svg_resp) and isinstance(svg_resp["output"], dict) and svg_resp["output"].get("svg"):
            svg_code = svg_resp["output"]["svg"]
        elif isinstance(svg_resp, dict) and svg_resp.get("svg_code"):
            svg_code = svg_resp["svg_code"]
        else:
            # fallback: if the whole response is a string
            svg_code = svg_resp if isinstance(svg_resp, str) else json.dumps(svg_resp)
        # save
        svg_file = save_svg(svg_code, filename="kundali.svg")
        print(f"Saved SVG chart to: {svg_file}")
        try:
            # try to open in default browser/viewer
            webbrowser.open("file://" + svg_file)
        except Exception:
            pass
    except Exception as e:
        print("SVG chart fetch failed:", e)
        # continue to fetch planets data anyway

    # 2) get planets/extended (detailed kundali data)
    try:
        print("Requesting planets (extended) data from API...")
        planet_resp = call_api("planets/extended", payload_core)
        # print a pretty summary
        pretty_print_planets(planet_resp)
        # also pretty-print the whole JSON to file for reference
        with open("kundali_planets.json", "w", encoding="utf-8") as f:
            json.dump(planet_resp, f, indent=2, ensure_ascii=False)
        print("Saved detailed planet JSON to kundali_planets.json")
    except Exception as e:
        print("Failed to fetch planets/extended:", e)

    print("Done. You can open kundali.svg and kundali_planets.json for full details.")
    if name:
        print(f"Thanks, {name} — hope the kundali helps")


if __name__ == "__main__":

    main()
