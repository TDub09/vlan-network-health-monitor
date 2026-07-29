import requests

url = "http://10.10.1.2/hello.html"  

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("good")
    else:
        print("bad")
except:
    print("bad")
