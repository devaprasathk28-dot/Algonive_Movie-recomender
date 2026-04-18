import requests

url = "http://www.omdbapi.com/"
params = {
    "apikey": "c6ac3547",
    "i": "tt0114709"   # Toy Story
}

res = requests.get(url, params=params)
print(res.json())