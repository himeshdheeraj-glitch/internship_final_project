import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/users", timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Success!")
        print(json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
