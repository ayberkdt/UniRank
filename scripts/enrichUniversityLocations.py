import os
import json
import time
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

def geocode(query):
    # Nominatim requires a descriptive User-Agent
    headers = {
        'User-Agent': 'UniRankDataEnricher/1.0 (ayberkdt@example.com)'
    }
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(query)}&limit=1"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data:
                return data[0]
    except HTTPError as e:
        print(f"HTTP Error {e.code} for query: {query}")
    except URLError as e:
        print(f"URL Error {e.reason} for query: {query}")
    except Exception as e:
        print(f"Error {e} for query: {query}")
    return None

def main():
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_base')
    
    # Mapping filenames to country names just in case it's missing in the record
    country_map = {
        'almanya.json': 'Germany',
        'amerika.json': 'United States',
        'austria.json': 'Austria',
        'belcika.json': 'Belgium',
        'cin.json': 'China',
        'danimarka.json': 'Denmark',
        'fransa.json': 'France',
        'hollanda.json': 'Netherlands',
        'ingiltere.json': 'United Kingdom',
        'ispanya.json': 'Spain',
        'isvec.json': 'Sweden',
        'isvicre.json': 'Switzerland',
        'italy.json': 'Italy',
        'japonya.json': 'Japan',
        'kore.json': 'South Korea',
        'portekiz.json': 'Portugal',
        'rusya.json': 'Russia',
    }

    total_enriched = 0
    
    for filename in os.listdir(db_dir):
        if not filename.endswith('.json') or filename == 'taxonomy.json':
            continue
            
        filepath = os.path.join(db_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
                
        if not isinstance(data, list):
            continue
            
        modified = False
        default_country = country_map.get(filename, '')
        
        for record in data:
            if 'location' in record and record['location'].get('latitude'):
                continue # Already has location
                
            city = record.get('city', '')
            country = record.get('country', default_country)
            uni_name = record.get('name', '')
            
            # Extract english name if it's a dict
            if isinstance(uni_name, dict):
                uni_name = uni_name.get('en', uni_name.get('tr', ''))
                
            if isinstance(city, dict):
                city = city.get('en', city.get('tr', ''))
                
            if isinstance(country, dict):
                country = country.get('en', country.get('tr', ''))

            if not city and not country:
                continue

            print(f"Geocoding {uni_name} in {city}, {country}...")
            
            # Try 1: Exact University
            result = None
            if uni_name:
                query = f"{uni_name}, {city}, {country}" if city else f"{uni_name}, {country}"
                result = geocode(query)
                time.sleep(1.1) # Rate limit
                
            # Try 2: Just City and Country
            confidence = 'exact'
            if not result and city:
                print(f"Fallback to city level for {city}, {country}...")
                query = f"{city}, {country}"
                result = geocode(query)
                confidence = 'city'
                time.sleep(1.1)
                
            if result:
                lat = float(result['lat'])
                lon = float(result['lon'])
                # Extract country code from Nominatim if possible (requires addressdetails=1)
                # But it's easier to just use the country name since Nominatim doesn't return CC by default without &addressdetails=1
                # Let's do a quick addressdetails=1 request next time, but for now we have the lat/lon!
                
                record['location'] = {
                    'country': country,
                    'city': city,
                    'latitude': lat,
                    'longitude': lon,
                    'locationConfidence': confidence
                }
                modified = True
                total_enriched += 1
                print(f"Found: {lat}, {lon} ({confidence})")
            else:
                print(f"NOT FOUND: {uni_name}")
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved {filename}")
            
    print(f"Done. Enriched {total_enriched} records.")

if __name__ == '__main__':
    main()
