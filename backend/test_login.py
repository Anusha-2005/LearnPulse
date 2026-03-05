import urllib.request
import urllib.parse

url = 'http://127.0.0.1:8000/api/auth/login'
data = urllib.parse.urlencode({'username':'faculty1@gmail.com','password':'password'}).encode()
req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print('STATUS', resp.status)
        print(resp.read().decode())
except Exception as e:
    import traceback
    traceback.print_exc()
    print('ERROR:', e)
