import requests

session = requests.Session()
session.trust_env = True  # 🔥 VERY IMPORTANT

url = "https://api.themoviedb.org/3/movie/8916"
params = {"api_key": "YOUR_API_KEY"}

res = session.get(url, params=params, timeout=10)

print(res.status_code)
print(res.json())