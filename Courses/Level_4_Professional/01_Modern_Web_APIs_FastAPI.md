# Lesson 1: Modern Web APIs with FastAPI & Pydantic

In modern backend engineering, building robust, type-safe, and self-documenting RESTful APIs is paramount. **FastAPI** has emerged as the premier Python web framework, leveraging standard Python type hints, non-blocking `asyncio` concurrency, and automatic data validation powered by **Pydantic**. In this lesson, you will master API routing, request validation schemas, response modeling, and Dependency Injection (`Depends`).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Construct high-performance asynchronous RESTful APIs using **FastAPI**.
2. Define strict request and response schemas using **Pydantic v2** (`BaseModel`, `Field`).
3. Handle Path Parameters, Query Parameters, and JSON Request Bodies with automatic type casting and validation.
4. Utilize standard HTTP Status Codes (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`).
5. Implement modular, reusable middleware and services using FastAPI's **Dependency Injection (`Depends`)** system.

---

## 1. Request Modeling & Data Validation with Pydantic

Pydantic validates incoming JSON payloads against declared Python type annotations at runtime, rejecting malformed requests with detailed field-level error messages:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class UserRegistrationRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Alphanumeric handle")
    email: str = Field(..., description="Valid corporate email address")
    role: Literal["ADMIN", "ENGINEER", "ANALYST"] = "ENGINEER"
    age: int = Field(..., ge=18, le=120, description="Must be of legal age")

# Automatic serialization & deserialization:
valid_payload = {"username": "erostova", "email": "elena@enterprise.com", "role": "ADMIN", "age": 28}
user = UserRegistrationRequest(**valid_payload)
print(user.model_dump()) # Converts to clean Python dictionary
```

---

## 2. Asynchronous API Routing with FastAPI

FastAPI uses Python decorators matching standard REST verbs (`@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()`):

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Core Inventory API", version="1.0.0")

class ItemSchema(BaseModel):
    name: str
    price: float

DB_STORE = {}

@app.post("/items/{item_id}", status_code=status.HTTP_201_CREATED)
async def create_item(item_id: str, item: ItemSchema):
    if item_id in DB_STORE:
        raise HTTPException(status_code=400, detail="Item identifier already exists")
    DB_STORE[item_id] = item.model_dump()
    return {"status": "SUCCESS", "data": DB_STORE[item_id]}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in DB_STORE:
        raise HTTPException(status_code=404, detail="Item not found")
    return DB_STORE[item_id]
```

---

---

## 4. Pydantic v2 Core: `@field_validator` & `@model_validator`

Pydantic v2 rewritten in Rust (`pydantic-core`) is up to $20\times$ faster than v1:

```python
from pydantic import BaseModel, field_validator, model_validator

class UserSignupSchema(BaseModel):
    username: str
    password: str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must contain only letters and numbers.')
        return v.lower()

    @model_validator(mode='after')
    def passwords_match(self) -> 'UserSignupSchema':
        if self.password != self.confirm_password:
            raise ValueError('Password and confirmation do not match.')
        return self
```

---

## 5. Application Lifespan Events (`lifespan`)

In modern FastAPI, database connections, Redis pools, and ML models are initialized and cleanly terminated using an async context manager **`lifespan`**:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup: Connect to DB pool
    print("🚀 [STARTUP] Initializing connection pools...")
    yield # API serves requests here
    # Teardown: Close connection pool
    print("🛑 [SHUTDOWN] Terminating connection pools...")

app = FastAPI(lifespan=app_lifespan)
```

---

## 6. Custom HTTP Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time-Ms"] = str(round(process_time * 1000, 2))
    return response
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master FastAPI routing, Pydantic v2 schemas, dependencies, middleware, and exception handlers:

---

### 🟢 Tier 1: Pydantic Basics & Simple Routes (Exercises 1–3)

#### 🔹 Exercise 1: User Profile Pydantic Schema
* **Goal**: Build a Pydantic model validating `username`, `email`, and `age >= 18`.

#### 🔹 Exercise 2: Path & Query Parameter Route
* **Goal**: Write a `@app.get("/users/{user_id}")` endpoint accepting an optional `filter: str` query parameter.

#### 🔹 Exercise 3: HTTP Status Code Management
* **Goal**: Build a `@app.post("/items")` route returning `201 Created` on success and raising `HTTPException(400)` on duplicate key.

---

### 🟡 Tier 2: Validation & Custom Responses (Exercises 4–6)

#### 🔹 Exercise 4: Custom Field Validator (`@field_validator`)
* **Goal**: Validate that incoming phone numbers adhere to E.164 international format (`+1...`).

#### 🔹 Exercise 5: Root Model Validator (`@model_validator`)
* **Goal**: Validate that `start_date < end_date` in a reservation payload.

#### 🔹 Exercise 6: Reusable Auth Dependency (`Depends`)
* **Goal**: Create a dependency verifying `Authorization: Bearer <token>` and injecting current user dictionary.

---

### 🟠 Tier 3: Lifespans, Middleware & Error Handlers (Exercises 7–9)

#### 🔹 Exercise 7: Global Custom Exception Handler
* **Goal**: Register an `@app.exception_handler(CustomDomainError)` returning structured JSON error payloads.

#### 🔹 Exercise 8: Latency Audit Middleware
* **Goal**: Write an HTTP middleware calculating request elapsed time and logging slow requests (>500ms).

#### 🔹 Exercise 9: Async Database Connection Lifespan
* **Goal**: Implement `lifespan` managing the lifecycle of an async memory dictionary store.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Hospital Appointment Scheduling REST Gateway
* **Goal**: Build a production-grade asynchronous medical scheduling API with specialty fee calculators and Pydantic validation.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Fintech Merchant Invoicing & Payment Web API**, demonstrating Pydantic v2 validation models, async CRUD endpoints, custom dependencies, and structured error responses:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Enterprise Fintech Merchant Invoicing REST API
# =====================================================================

from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

app = FastAPI(title="Apex Fintech Invoicing Gateway", version="2.4.0")

# 1. Pydantic Request & Response Schemas (Lesson 1)
class LineItem(BaseModel):
    description: str = Field(..., min_length=2, max_length=100)
    unit_price: float = Field(..., gt=0.0, description="Must be strictly positive")
    quantity: int = Field(..., ge=1, description="Minimum 1 unit")

class InvoiceCreateRequest(BaseModel):
    customer_id: str = Field(..., min_length=3)
    currency: Literal["USD", "EUR", "GBP"] = "USD"
    items: list[LineItem] = Field(..., min_length=1, description="At least one line item required")

class InvoiceResponse(BaseModel):
    invoice_id: str
    customer_id: str
    currency: str
    subtotal: float
    tax_amount: float
    total_due: float
    status: Literal["ISSUED", "PAID", "CANCELLED"]
    created_at: str


# 2. In-Memory Storage & Dependencies
INVOICE_LEDGER: dict[str, dict] = {}
invoice_sequence = 1000

async def authenticate_merchant_key(x_merchant_key: str = Header(...)) -> str:
    """Security dependency validating merchant API token."""
    if not x_merchant_key.startswith("mk_live_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Merchant-Key credentials."
        )
    return "MERCHANT_APEX_CORP"


# 3. RESTful API Endpoints
@app.post(
    "/api/v1/invoices",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Merchant Invoice"
)
async def create_invoice(
    payload: InvoiceCreateRequest,
    merchant: str = Depends(authenticate_merchant_key)
):
    global invoice_sequence
    invoice_sequence += 1
    inv_id = f"INV-{invoice_sequence}"

    subtotal = sum(item.unit_price * item.quantity for item in payload.items)
    tax = round(subtotal * 0.08, 2) # 8% standard tax
    total = round(subtotal + tax, 2)

    record = {
        "invoice_id": inv_id,
        "customer_id": payload.customer_id,
        "currency": payload.currency,
        "subtotal": round(subtotal, 2),
        "tax_amount": tax,
        "total_due": total,
        "status": "ISSUED",
        "created_at": datetime.utcnow().isoformat(),
        "merchant": merchant
    }
    
    INVOICE_LEDGER[inv_id] = record
    return record


@app.get(
    "/api/v1/invoices/{invoice_id}",
    response_model=InvoiceResponse,
    summary="Fetch Invoice by ID"
)
async def get_invoice(
    invoice_id: str,
    merchant: str = Depends(authenticate_merchant_key)
):
    if invoice_id not in INVOICE_LEDGER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invoice '{invoice_id}' does not exist in master ledger."
        )
    return INVOICE_LEDGER[invoice_id]


# Direct execution mock to test API logic without external uvicorn server
if __name__ == "__main__":
    import asyncio
    print("=" * 70)
    print(f"{'FASTAPI FINTECH INVOICING GATEWAY SIMULATION':^70}")
    print("=" * 70)

    async def run_api_tests():
        # Test 1: Successful Invoice Creation
        req = InvoiceCreateRequest(
            customer_id="CUST-4491",
            currency="USD",
            items=[
                LineItem(description="Cloud Server Hosting", unit_price=250.00, quantity=2),
                LineItem(description="Managed SSL Certificate", unit_price=49.99, quantity=1)
            ]
        )
        inv = await create_invoice(req, merchant="MERCHANT_APEX_CORP")
        print(f"✅ Created Invoice: {inv['invoice_id']}")
        print(f"   Subtotal:  ${inv['subtotal']:,.2f}")
        print(f"   Tax (8%):  ${inv['tax_amount']:,.2f}")
        print(f"   Total Due: ${inv['total_due']:,.2f}")

        # Test 2: Fetch by ID
        fetched = await get_invoice(inv['invoice_id'], merchant="MERCHANT_APEX_CORP")
        print(f"✅ Fetched Invoice: {fetched['invoice_id']} -> Status: {fetched['status']}")

    asyncio.run(run_api_tests())
    print("=" * 70)
```

### 🔍 Code Explanation:
- **`Pydantic v2 Schemas`**: `LineItem` and `InvoiceCreateRequest` guarantee that incoming data contains positive prices, non-zero quantities, and valid currencies before the route handler executes.
- **`Depends(authenticate_merchant_key)`**: Decouples API credential authentication into a reusable dependency injected into multiple route handlers.
- **`response_model=InvoiceResponse`**: Automatically filters out internal fields (such as private internal DB keys) before returning JSON payloads to client callers.

---

## 📝 Quick Exercise: Healthcare Patient Medical Appointment Scheduling API

### 🏢 Real-Life Scenario
You are developing the RESTful API for a regional hospital's outpatient appointment scheduling portal. Patients can book medical consultations with physicians. You must define Pydantic validation models and FastAPI route handlers to create and query appointments, verifying that appointment dates are future timestamps and doctor specialties are valid.

### 📋 Requirements
1. **Define Pydantic Schema `AppointmentBookingRequest`**:
   - `patient_name: str` (min length 2, max length 50)
   - `patient_email: str`
   - `doctor_specialty: Literal["CARDIOLOGY", "DERMATOLOGY", "NEUROLOGY", "PEDIATRICS"]`
   - `duration_minutes: int` (must be 15, 30, 45, or 60)
2. **Define Pydantic Schema `AppointmentResponse`**:
   - `appointment_id: str`
   - `patient_name: str`
   - `doctor_specialty: str`
   - `consultation_fee: float` (Calculated: Cardiology/Neurology = $250.00, Dermatology/Pediatrics = $150.00)
   - `status: Literal["CONFIRMED", "CANCELLED"]`
3. **Define Async Route Handler `book_appointment(payload: AppointmentBookingRequest)`**:
   - Computes consultation fee based on specialty.
   - Stores appointment in memory dictionary `APPOINTMENT_STORE`.
   - Returns formatted `AppointmentResponse`.
4. Test booking an appointment and verify validation behavior.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 FastAPI/Pydantic schemas with Level 3 async execution and Level 1 dictionaries, functions, and string formatting.

### 🎯 Expected Output
```text
==================================================
        HOSPITAL APPOINTMENT SCHEDULING API       
==================================================
✅ APPOINTMENT CONFIRMED:
  - Appointment ID:   APT-5001
  - Patient:          Elena Rostova
  - Specialty:        CARDIOLOGY
  - Duration:         45 mins
  - Consultation Fee: $250.00
  - Status:           CONFIRMED
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Hospital API & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Hospital Appointment Scheduling API
# =====================================================================
import asyncio
from pydantic import BaseModel, Field
from typing import Literal

class AppointmentBookingRequest(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=50)
    patient_email: str
    doctor_specialty: Literal["CARDIOLOGY", "DERMATOLOGY", "NEUROLOGY", "PEDIATRICS"]
    duration_minutes: Literal[15, 30, 45, 60]

class AppointmentResponse(BaseModel):
    appointment_id: str
    patient_name: str
    doctor_specialty: str
    duration_minutes: int
    consultation_fee: float
    status: Literal["CONFIRMED", "CANCELLED"]


APPOINTMENT_STORE: dict[str, dict] = {}
appointment_counter = 5000

async def book_appointment(payload: AppointmentBookingRequest) -> AppointmentResponse:
    global appointment_counter
    appointment_counter += 1
    apt_id = f"APT-{appointment_counter}"

    fee = 250.00 if payload.doctor_specialty in {"CARDIOLOGY", "NEUROLOGY"} else 150.00

    record = {
        "appointment_id": apt_id,
        "patient_name": payload.patient_name,
        "doctor_specialty": payload.doctor_specialty,
        "duration_minutes": payload.duration_minutes,
        "consultation_fee": fee,
        "status": "CONFIRMED"
    }

    APPOINTMENT_STORE[apt_id] = record
    return AppointmentResponse(**record)


async def main():
    req = AppointmentBookingRequest(
        patient_name="Elena Rostova",
        patient_email="elena@medical.org",
        doctor_specialty="CARDIOLOGY",
        duration_minutes=45
    )

    res = await book_appointment(req)

    print("==================================================")
    print("        HOSPITAL APPOINTMENT SCHEDULING API       ")
    print("==================================================")
    print("✅ APPOINTMENT CONFIRMED:")
    print(f"  - Appointment ID:   {res.appointment_id}")
    print(f"  - Patient:          {res.patient_name}")
    print(f"  - Specialty:        {res.doctor_specialty}")
    print(f"  - Duration:         {res.duration_minutes} mins")
    print(f"  - Consultation Fee: ${res.consultation_fee:,.2f}")
    print(f"  - Status:           {res.status}")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: User Profile Model
class UserProfile(BaseModel):
    username: str = Field(..., min_length=3)
    email: str
    age: int = Field(..., ge=18)

# Ex 2: Route Params
# @app.get("/users/{user_id}")
# async def get_user(user_id: int, filter_str: str | None = None): ...

# Ex 3: Status 201
# @app.post("/items", status_code=201)

# Ex 4: Field Validator
from pydantic import field_validator
class PhoneSchema(BaseModel):
    phone: str
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v.startswith("+"): raise ValueError("Must start with +")
        return v

# Ex 5: Model Validator
from pydantic import model_validator
class DateRange(BaseModel):
    start: int
    end: int
    @model_validator(mode="after")
    def check_range(self):
        if self.start >= self.end: raise ValueError("start must be < end")
        return self

# Ex 6: Auth Dependency
# async def get_current_user(auth: str = Header(...)): ...

# Ex 7: Global Exception Handler
# @app.exception_handler(ValueError)

# Ex 8: Middleware
# @app.middleware("http")

# Ex 9: Lifespan
# @asynccontextmanager async def lifespan(app: FastAPI): yield
```
</details>
