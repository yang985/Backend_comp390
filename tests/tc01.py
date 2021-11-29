import requests

payload = {
    'username': 'yang',
    'password': '234234423',
}

response = requests.post('http://localhost/users/signin/', data=payload)

result = response.json()

print(response.status_code)
print(result)