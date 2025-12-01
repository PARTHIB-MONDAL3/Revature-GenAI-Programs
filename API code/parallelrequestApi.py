import concurrent.futures
import requests

def fetch(url):
    return requests.get(url, timeout=5)

urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch, urls))

for r in results:
    print(r.status_code, r.json()["id"])