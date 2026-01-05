# import requests

# url = "https://jsonplaceholder.typicode.com/posts/1"

# response = requests.get(url)
# response

# response.json()



from fastapi import FastAPI

app = FastAPI()


@app.get("/")

def hello():
    return "Hello World"

