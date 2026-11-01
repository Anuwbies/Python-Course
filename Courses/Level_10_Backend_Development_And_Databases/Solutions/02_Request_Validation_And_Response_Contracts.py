from threading import Lock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field

class OrderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    item: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=100, strict=True)

class OrderOutput(OrderInput):
    id: int

def create_app():
    app = FastAPI()
    orders = {}
    lock = Lock()
    @app.post("/orders", response_model=OrderOutput, status_code=201)
    def create_order(payload: OrderInput):
        with lock:
            identifier = len(orders) + 1
            result = {"id": identifier, **payload.model_dump()}
            orders[identifier] = result
            return result.copy()
    @app.get("/orders/{order_id}", response_model=OrderOutput)
    def get_order(order_id: int):
        with lock:
            if order_id not in orders:
                raise HTTPException(404, "Order not found")
            return orders[order_id].copy()
    return app

if __name__ == "__main__":
    with TestClient(create_app()) as client:
        print(client.post("/orders", json={"item": "Pen", "quantity": 2}).status_code)
        print(client.post("/orders", json={"item": "Pen", "quantity": True}).status_code)
        print(client.get("/orders/999").status_code)
