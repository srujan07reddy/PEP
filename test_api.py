import urllib.request
import urllib.error
import json

req = urllib.request.Request(
    'http://localhost:8000/domains', 
    data=json.dumps({'name': 'University ERP'}).encode('utf-8'), 
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(e.read().decode('utf-8'))
