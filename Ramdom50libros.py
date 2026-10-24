import requests
import random
import string

BASE = "http://library.demo.local/api/v1"

login = requests.post(f"{BASE}/loginViaBasic", auth=("cisco", "Cisco123!"))
token = login.json()["token"]
headers = {"X-API-KEY": "cisco|sOWGvmVxek7-Os7NTzx9XCa-7B2uZtX8kcuy7HniOss"}

def texto(n):
    return "".join(random.choices(string.ascii_lowercase, k=n)).capitalize()

for i in range(8, 58):
    libro = {
        "id": i,
        "title": f"{texto(6)} {texto(8)}",
        "author": f"{texto(5)}_{texto(7)}",
        "isbn": "".join(random.choices(string.digits, k=9)),
    }
    r = requests.post(f"{BASE}/books", json=libro, headers=headers)
    print(i, r.status_code)

todos = requests.get(f"{BASE}/books", headers=headers)
for b in todos.json():
    print(b)