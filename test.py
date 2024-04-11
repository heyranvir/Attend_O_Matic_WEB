import requests
headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'course':'english','name':'Ranvir','date':'2024-04-07'}

r = requests.post('http://localhost:5000/mark_attendance',headers=headers,data=payload)

print(r.response)
