import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/locations/countries/3b54ccf3-fcfe-400a-96e3-8e093f470577/states", timeout=5) as response:
        html = response.read()
        print("States Success:")
        states = json.loads(html.decode('utf-8'))
        print(states)
        
    # Get cities for Karnataka (ID: 52e65242-aded-4574-92e1-304e7d64798b)
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/locations/states/52e65242-aded-4574-92e1-304e7d64798b/cities", timeout=5) as response:
        html = response.read()
        print("Cities Success:")
        print(json.loads(html.decode('utf-8')))
except Exception as e:
    print("Error:", e)
