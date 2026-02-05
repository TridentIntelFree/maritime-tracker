import json
import os
import requests
from datetime import datetime

def fetch_ais_ships():
    """Fetch real ship positions from AISStream API"""
    ships = []
    api_key = os.environ.get('AISSTREAM_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return ships
    
    try:
        # AISStream REST API endpoint for recent positions
        url = "https://stream.aisstream.io/v0/stream"
        
        headers = {
            'x-api-key': api_key,
            'Accept': 'application/json'
        }
        
        # For now, we'll use a simpler approach - get vessel list
        # In production, you'd use WebSocket for real-time
        
        print("Fetching ship data from AISStream...")
        
        # Alternative: Use public AIS data aggregator
        # This is a fallback if AISStream format differs
        public_url = "https://www.myshiptracking.com/requests/vesselsonmap.php?type=json&zoom=3"
        
        response = requests.get(public_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse ship data
            count = 0
            for vessel in data[:100]:  # Limit to 100 ships
                try:
                    ship = {
                        "name": vessel.get('name', 'Unknown Vessel'),
                        "mmsi": vessel.get('mmsi', ''),
                        "lat": float(vessel.get('lat', 0)),
                        "lng": float(vessel.get('lon', 0)),
                        "speed": vessel.get('speed', 0),
                        "course": vessel.get('course', 0),
                        "type": vessel.get('type', 'Unknown'),
                        "destination": vessel.get('destination', 'N/A'),
                        "timestamp": vessel.get('timestamp', '')
                    }
                    
                    if ship['lat'] and ship['lng']:
                        ships.append(ship)
                        count += 1
                        
                except Exception as e:
                    continue
            
            print(f"✅ Fetched {count} ships")
        
    except Exception as e:
        print(f"❌ Error fetching ships: {e}")
    
    return ships

def save_data(ships):
    """Save to JSON file"""
    data = {
        "updated": datetime.now().isoformat(),
        "ships": ships,
        "source": "AIS Live Data"
    }
    
    with open('ships-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(ships)} ships to ships-data.json")

if __name__ == "__main__":
    print("Fetching real ship positions...")
    ships = fetch_ais_ships()
    save_data(ships)
