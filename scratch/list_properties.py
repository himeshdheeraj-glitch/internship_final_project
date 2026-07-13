import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/properties", timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Success! Number of properties:", len(data.get('data', {}).get('items', [])))
        for prop in data.get('data', {}).get('items', []):
            print(f"ID: {prop['id']}, Title: {prop['title']}, Price: {prop['price']}")
except Exception as e:
    print("Error:", e)
