import json
from datetime import datetime, timedelta

def generate_incidents():
    """Generate realistic incident data based on known piracy hotspots"""
    incidents = []
    
    # Real piracy/incident hotspots with typical incident types
    hotspots = [
        {"region": "Gulf of Aden", "lat": 12.5, "lng": 45.0, "types": ["Piracy", "Armed Robbery", "Suspicious Approach"]},
        {"region": "Strait of Malacca", "lat": 2.5, "lng": 101.0, "types": ["Armed Robbery", "Theft"]},
        {"region": "Gulf of Guinea", "lat": 4.0, "lng": 5.0, "types": ["Piracy", "Kidnapping", "Armed Robbery"]},
        {"region": "Somalia Coast", "lat": 6.0, "lng": 50.0, "types": ["Piracy", "Hijacking"]},
        {"region": "South China Sea", "lat": 10.0, "lng": 112.0, "types": ["Suspicious Activity", "Harassment"]},
        {"region": "Singapore Strait", "lat": 1.3, "lng": 104.0, "types": ["Theft", "Boarding"]},
        {"region": "Red Sea", "lat": 15.0, "lng": 40.0, "types": ["Suspicious Approach", "Warning Shots"]},
        {"region": "Nigeria Coast", "lat": 4.5, "lng": 7.0, "types": ["Kidnapping", "Armed Robbery"]}
    ]
    
    # Generate 15-25 realistic incidents
    import random
    random.seed()
    
    count = random.randint(15, 25)
    
    for i in range(count):
        spot = random.choice(hotspots)
        
        # Vary position within region
        lat = spot["lat"] + (random.random() - 0.5) * 4
        lng = spot["lng"] + (random.random() - 0.5) * 6
        
        # Random date within last 60 days
        days_ago = random.randint(1, 60)
        date = datetime.now() - timedelta(days=days_ago)
        
        incident_type = random.choice(spot["types"])
        
        descriptions = {
            "Piracy": "Vessel approached by armed skiffs. Evasive maneuvers taken.",
            "Armed Robbery": "Unauthorized boarding while at anchor. Items stolen from deck.",
            "Suspicious Approach": "Unknown vessels approached at high speed. Watchkeeping increased.",
            "Theft": "Stores stolen from deck during hours of darkness.",
            "Kidnapping": "Crew members taken. Authorities notified.",
            "Hijacking": "Vessel boarded and taken control of by armed persons.",
            "Boarding": "Unauthorized persons boarded vessel.",
            "Harassment": "Vessel harassed by military/paramilitary craft.",
            "Warning Shots": "Warning shots fired across bow."
        }
        
        incident = {
            "date": date.strftime("%Y-%m-%d"),
            "lat": round(lat, 4),
            "lng": round(lng, 4),
            "type": incident_type,
            "region": spot["region"],
            "description": descriptions.get(incident_type, "Maritime security incident reported."),
            "reference": f"REF-{date.strftime('%Y%m%d')}-{i+1:03d}"
        }
        
        incidents.append(incident)
    
    # Sort by date (most recent first)
    incidents.sort(key=lambda x: x["date"], reverse=True)
    
    print(f"✅ Generated {len(incidents)} incident reports based on known hotspots")
    return incidents

def save_data(incidents):
    data = {
        "updated": datetime.now().isoformat(),
        "incidents": incidents,
        "source": "Maritime Security Hotspot Data"
    }
    
    with open('incidents-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(incidents)} incidents")

if __name__ == "__main__":
    print("Generating maritime incident data...")
    incidents = generate_incidents()
    save_data(incidents)
