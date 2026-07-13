import urllib.request
import json

queries = ["Residential", "Houses", "Villas", "Land"]

for q in queries:
    url = f"http://127.0.0.1:8000/api/v1/properties?search_query={q}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('data', {}).get('items', [])
            print(f"Query '{q}': found {len(items)} items.")
            for item in items:
                print(f"  - Title: {item['title']}, Type: {item['property_type']['name']}")
    except Exception as e:
        print(f"Query '{q}' failed: {e}")
