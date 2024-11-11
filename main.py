import requests
import os


directory = 'books'
os.makedirs(directory, exist_ok=True)

for i in range(10):
    url = f"https://tululu.org/txt.php?id={i}"
    response = requests.get(url)
    response.raise_for_status()
    filename = f"{directory}/id_{i}.txt"
    with open(filename, 'wb') as file:
        file.write(response.content)
