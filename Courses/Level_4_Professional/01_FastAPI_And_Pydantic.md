# Lesson 1: Modern Web Frameworks: FastAPI & Pydantic Validation

FastAPI is the modern, high-performance web framework for building REST APIs with Python 3.8+ based on standard Python type hints and ASGI.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Initialize a FastAPI app and define route endpoints (`GET`, `POST`, `PUT`, `DELETE`).
2. Validate and serialize request bodies using **Pydantic v2 Models**.
3. Use FastAPI's **Dependency Injection (`Depends`)** system.
4. Auto-generate interactive OpenAPI / Swagger documentation (`/docs`).

---

## 1. Building a REST API with FastAPI & Pydantic

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="User Management Microservice", version="1.0.0")

# 1. Define Request / Response Schemas with Pydantic
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

# In-memory mock database
db: dict[int, dict] = {}
user_id_counter = 1

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate):
    global user_id_counter
    new_user = {
        "id": user_id_counter,
        "username": payload.username,
        "email": payload.email,
        "age": payload.age
    }
    db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]
```

---

## 📝 Quick Exercise

**Prompt**:
Create a FastAPI endpoint `POST /products` with fields `name`, `price` (must be $> 0$), and `stock` (integer $\ge 0$).

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0.0, description="Price must be strictly greater than 0")
    stock: int = Field(..., ge=0, description="Stock must be 0 or positive integer")

class ProductResponse(ProductCreate):
    id: int

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    # Simulated db insert
    return {
        "id": 101,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
```
</details>
