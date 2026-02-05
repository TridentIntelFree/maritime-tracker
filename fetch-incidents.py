import json
import requests
from datetime import datetime

def fetch_asam_incidents():
    """Fetch real maritime incidents from ASAM database"""
    incidents = []
    
    try:
        # ASAM XML feed (public)
        url = "https://msi.gs.mil/api/publications/asam"
        
        headers = {'User-Agent': 'Maritime-Tracker/1.0'}
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Parse incidents
            for item in data.get('asam', [])[:50]:  # Last 50 incidents
                try:
                    incident = {
                        "date": item.get('date', 'Unknown'),
                        "lat": float(item.get('latitude', 0)),
                        "lng": float(item.get('longitude', 0)),
                        "type": item.get('aggressor', 'Unknown'),
                        "victim": item.get('victim', 'Unknown'),
                        "description": item.get('description', 'No details'),
                        "reference": item.get('reference', '')
                    }
                    
                    if incident['lat'] and incident['lng']:
                        incidents.append(incident)
                        
                except Exception as e:
                    print(f"Error parsing incident: {e}")
                    continue
        
        print(f"✅ Fetched {len(incidents)} incidents")
        
    except Exception as e:
        print(f"❌ Error fetching ASAM: {e}")
    
    return incidents

def save_data(incidents):
    """Save to JSON file"""
    data = {
        "updated": datetime.now().isoformat(),
        "incidents": incidents,
        "source": "ASAM (Anti-Shipping Activity Messages)"
    }
    
    with open('incidents-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(incidents)} incidents to incidents-data.json")

if __name__ == "__main__":
    print("Fetching real maritime incidents...")
    incidents = fetch_asam_incidents()
    save_data(incidents)
