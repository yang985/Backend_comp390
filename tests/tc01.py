import requests

payload = {
    'username': 'yang',
    'password': '79898896sgyzh173',
}

response = requests.post('http://localhost:8000/users/signin/', data=payload)

result = response.json()

print(response.status_code)
print(result)