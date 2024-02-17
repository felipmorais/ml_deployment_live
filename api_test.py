import requests

# teste 1 - hello world
response = requests.get("http://localhost:8000/hello_world")
print(response)

if response.status_code == 200:
    response_data = response.json()
    print(f"Response: {response_data['message']}")
else:
    print(f"Erro na requisição: {response.status_code}")