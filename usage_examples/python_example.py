import requests


with open("example.png", 'rb') as fp:
    print(requests.post("http://localhost:8000/upload/",
                        files={'file': fp}, ).content)
