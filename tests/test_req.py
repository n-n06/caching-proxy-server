import requests

response = requests.get("http://localhost:3000/v4/anime/33352/full")


print(response.headers)
