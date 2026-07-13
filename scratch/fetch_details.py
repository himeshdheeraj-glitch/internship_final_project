import urllib.request
import json
import sys

prop_id = "ee505318-f223-40b7-a482-58f89d74e06f"
url = f"http://127.0.0.1:8000/api/v1/properties/{prop_id}"
print("Fetching url:", url)
try:
    with urllib.request.urlopen(url, timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Success! Details:")
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error details:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
