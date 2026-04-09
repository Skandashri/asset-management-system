import requests

# Simple script to call the login endpoint on the backend
url = 'http://localhost:8001/api/auth/login'
cred = {'username': 'admin@optiasset.com', 'password': 'admin123'}

try:
    r = requests.post(url, data=cred, timeout=5)
    print('status', r.status_code)
    print('body', r.text)
except Exception as e:
    print('request failed', e)
