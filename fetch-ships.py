import json
import requests
from datetime import datetime

def fetch_ais_ships():
    """Fetch real ship positions from public AIS aggregator"""
    ships = []
    
    try:
        # Using AISHub public data feed
        url = "https://data.aishub.net/ws.php?username=AH_DEMO&format=1&output=json&compress=0"
        
        headers = {'User-Agent': 'Maritime-Tracker/1.0'}
        response = requests.get(url, headers=headers, timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse first 100 ships
            for vessel in data[0][:100]:
                try:
                    ship = {
                        "name": vessel.get(8, 'Unknown'),
                        "mmsi": vessel.get(0, ''),
                        "lat": float(vessel.get(1, 0)),
                        "lng": float(vessel.get(2, 0)),
                        "speed": vessel.get(4, 0),
                        "course": vessel.get(3, 0),
                        "type": vessel.get(9, 'Unknown'),
                        "timestamp": vessel.get(10, '')
                    }
                    
                    if ship['lat'] and ship['lng']:
                        ships.append(ship)
                        
                except Exception as e:
                    continue
            
            print(f"✅ Fetched {len(ships)} ships from AISHub")
        else:
            print(f"❌ API returned status {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return ships

def save_data(ships):
    data = {
        "updated": datetime.now().isoformat(),
        "ships": ships,
        "source": "AISHub Public Feed"
    }
    
    with open('ships-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(ships)} ships")

if __name__ == "__main__":
    print("Fetching ship data...")
    ships = fetch_ais_ships()
    save_data(ships)
