import requests

# Paste the access token you got from OAuth Playground
ACCESS_TOKEN = "ya29.a0ATi6K2sRawnvIfvQfFY0LLKZqflcEnwJpad9aI05gDFdNHHUSv7Yo8pijKyMW0AVW4pzLt3prayN64jxQgtSuYGijD9j5XEADnYg4mQhWCGkp9L_8951CifpWMARv8ujvyv0uAGw9nuJz0zmH5kmmbAnpoNP3auwGn8r3jwI5IqWO-ZBHCS44aJdzH6HAYMqdGferWYaCgYKARESARESFQHGX2Mi-OQBbtGSOcpkux8hmjFh0g0206"

url = "https://www.googleapis.com/drive/v3/files"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

params = {
    "pageSize": 20,          # Number of files to list
    "fields": "files(id, name, mimeType)"  # Info you want
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    print("Files in your Google Drive:")
    for f in response.json().get("files", []):
        print(f"{f['name']} ({f['id']}) - {f['mimeType']}")
else:
    print("Error:", response.text)