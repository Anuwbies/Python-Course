from fastapi import FastAPI
from fastapi.testclient import TestClient

def create_app():
    app = FastAPI()
    @app.get("/health")
    def health():
        return {"status": "ok"}
    @app.get("/double/{value}")
    def double(value: int):
        return {"result": value * 2}
    return app

if __name__ == "__main__":
    with TestClient(create_app()) as client:
        response = client.get("/double/3")
        print(response.status_code)
        print(response.json()["result"])
