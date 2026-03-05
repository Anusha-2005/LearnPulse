import urllib.request
import urllib.parse
import traceback

url = 'http://127.0.0.1:8000/api/auth/login'
form = {
    'username': 'test@example.com',
    'password': 'password'
}

data = urllib.parse.urlencode(form).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        status = resp.getcode()
        body = resp.read()
        try:
            body_text = body.decode('utf-8')
        except Exception:
            body_text = repr(body)
        print(f"HTTP {status}")
        print(body_text)
except Exception:
    print(traceback.format_exc(), end='')
