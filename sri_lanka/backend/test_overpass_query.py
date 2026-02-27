import requests
import json

# Testing with London coordinates (known to have places)
lat = 51.5074
lon = -0.1278

query = f"""
[out:json][timeout:25];
(
  nwr["tourism"="attraction"](around:5000,{lat},{lon});
  nwr["historic"](around:5000,{lat},{lon});
);
out center;
"""

print(f"Querying Overpass with lat={lat}, lon={lon}...")
try:
    response = requests.get("https://overpass-api.de/api/interpreter", params={"data": query})
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        elements = data.get("elements", [])
        print(f"Found {len(elements)} elements.")
        
        has_tags = False
        names = []
        for el in elements:
            if "tags" in el:
                has_tags = True
                if "name" in el["tags"]:
                    names.append(el["tags"]["name"])
        
        print(f"Elements with tags: {has_tags}")
        print(f"Found names ({len(names)}): {names[:5]}")
    else:
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
