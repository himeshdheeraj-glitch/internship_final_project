import urllib.request
import urllib.error

try:
    urllib.request.urlopen("http://127.0.0.1:8000/api/v1/locations/states/52e65242-aded-4574-92e1-304e7d64798b/cities")
except urllib.error.HTTPError as e:
    print(e.read().decode())
