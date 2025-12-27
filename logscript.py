from simdata import gen_logs, users
import requests

API_URL = "http://127.0.0.1:8000/events"

test = gen_logs(users, 1)[0]

response = requests.post(API_URL, data = None, json = test, headers = None)

print(response.json())

