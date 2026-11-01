# Lesson 2: Request Validation & Response Contracts

**Prerequisites:** Levels 1–9 and Lesson 1 of this level. **Practice file:** `Practice/02_Request_Validation_And_Response_Contracts.py`.

Validate external payloads before they reach domain or storage operations. A useful API distinguishes invalid input, a missing resource, and a successfully created resource.

## 1. Define a request model

Pydantic BaseModel uses annotated fields to describe a data shape. Field can add numeric or length constraints. This course uses Pydantic v2 syntax, including model_dump and ConfigDict rather than the older v1 APIs.

```python
from pydantic import BaseModel, ConfigDict, Field

class OrderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    item: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=100, strict=True)
```

String whitespace cleanup happens before length validation under this configuration, so a whitespace-only item is rejected. Strict integer quantity rejects Boolean and numeric-string substitutions instead of silently accepting them. Extra fields are forbidden deliberately; accepting and ignoring them would be a different interface policy.

## 2. Keep input and output models distinct

The client provides item and quantity; the server assigns an identifier. A response model can include that identifier and control which fields are serialized. Do not return an entire internal object simply because a serializer can inspect it: internal or sensitive fields may not belong in the public representation.

Validation at the HTTP boundary does not replace database constraints or authorization. Another caller could reach the domain layer without that exact request model. Keep important invariants enforced at the appropriate underlying boundaries too.

## 3. Use statuses for actual outcomes

POST creation can return 201. A missing ID can raise HTTPException with 404. Request-model failures normally produce 422 in this FastAPI contract. Use 400, 401, 403, and conflict statuses according to a documented policy rather than labeling every failure 500.

A success-shaped error dictionary with status 200 is ambiguous to clients and monitoring. Translate known domain errors into the intended status while allowing unexpected failures to be logged and investigated without exposing internal secrets in the response.

## 4. Make temporary storage limits explicit

An in-memory dictionary can demonstrate routes but disappears when the process restarts and is not a multiworker shared store. The next lessons introduce real relational persistence. Do not print a persistence claim merely because a GET succeeds immediately after POST in the same instance.

Because synchronous routes can run on worker threads, protect the in-memory identifier allocation and dictionary update with a shared lock, using Level 9's read-modify-write discipline. This is a local demonstration only; it does not make several server processes share the same dictionary.

For this task, keep state inside the application factory so separate test applications are independent. Derive each response from actual validated and stored data, and inspect both status and JSON fields.

## Connect models to handlers and HTTP calls

An output model can inherit input fields and add the assigned identifier. The route decorator accepts both response_model and the successful status code:

```python
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

class ItemInput(BaseModel):
    name: str = Field(min_length=1)

class ItemOutput(ItemInput):
    id: int

app = FastAPI()
@app.post("/example-items", response_model=ItemOutput, status_code=201)
def create_item(payload: ItemInput):
    return {"id": 1, **payload.model_dump()}

@app.get("/example-missing")
def missing():
    raise HTTPException(status_code=404, detail="Item not found")

with TestClient(app) as client:
    response = client.post("/example-items", json={"name": "Pen"})
    print(response.status_code)  # 201
```

This example only demonstrates a request/response shape and assigns a fixed example ID; the independent task must allocate real increasing IDs under its shared lock. model_dump returns a dictionary of validated fields. The json= argument sends a JSON request body; response.json() parses the actual response body. Field(default="", max_length=120) can add an optional empty note for a later project without requiring callers to send it.

References: [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/), [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the outcome of quantity true, quantity "2", and quantity 2.
2. **Explain:** Explain why a generated ID belongs to the response rather than required client input.
3. **Modify:** Reject whitespace-only item text using the stated model configuration.
4. **Debug:** Find an API that reports a known missing resource as successful status 200.

<details>
<summary>Hints</summary>

Use a request model for validation and a separate response shape for server-assigned fields.

</details>

## Independent task: request validation & response contracts

In `Practice/02_Request_Validation_And_Response_Contracts.py`, complete this task:

Implement an isolated in-memory create_app() with POST /orders and GET /orders/{order_id}. Define OrderInput with whitespace-stripped item text of length 1..80, a strict plain-integer quantity from 1 through 100, and forbidden extra fields. Define OrderOutput with those fields plus an integer id. Then assign increasing IDs from 1 under a shared Lock, return 201 on creation, 404 for missing IDs, and use an output model including id/item/quantity. Demonstrate a valid creation, a Boolean quantity rejection, and a missing read; print the three response statuses.

Expected output:

```text
201
422
404
```
