# Lesson 1: HTTP, Routes & FastAPI

**Prerequisites:** Levels 1–9. **Practice file:** `Practice/01_HTTP_Routes_And_FastAPI.py`.

Expose an application operation through an explicit HTTP contract. A route connects a method and path to behavior; a response includes both a status and a representation of the result.

## 1. Describe the request and response

HTTP requests identify a method, a target path, headers, and sometimes a body. GET normally retrieves a representation; POST commonly creates or submits something. A status such as 200, 201, 404, or 422 describes the outcome under the API's contract, not whether Python printed a friendly message.

A server receives requests over a transport and invokes the application. FastAPI describes routing, validation, dependency wiring, and response serialization. Uvicorn is an ASGI server that can host that application; the two tools have distinct responsibilities.

## 2. Register a route

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

The decorator registers the function with the application. Returning a dictionary lets the framework serialize a JSON response; it is not the same as printing the dictionary. A path parameter written `{value}` is supplied to the corresponding function parameter, and its annotation can request integer parsing.

## 3. Exercise the real application in process

FastAPI's TestClient sends requests through routing and serialization without opening an external listening port. It still invokes the actual handler. A test returning a hardcoded status from a fake helper would not exercise these layers.

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
@app.get("/health")
def health():
    return {"status": "ok"}

with TestClient(app) as client:
    response = client.get("/health")
    print(response.status_code)
    print(response.json()["status"])
```

Using the client context also runs the application's lifespan handling when present. In-process tests do not demonstrate container networking, TLS, or an external database connection; those need separate operational evidence.

## 4. Keep blocking and async behavior honest

An ordinary def route can perform bounded blocking work in FastAPI's worker-thread handling. An async def route should await appropriate async operations rather than block the event-loop thread with synchronous database or file calls.

Do not choose async syntax merely because the application is a web API. Preserve the domain function contracts from earlier levels and adapt their results or errors at the HTTP boundary. The capstone combines these routes with actual persistent storage after the database lessons.

## Match a typed path placeholder

For a route declared with `@app.get("/triple/{number}")`, define its handler as `def triple(number: int):`. The matching name binds the path segment and the annotation requests integer validation; `/triple/4` can return `{"result": number * 3}` while a noninteger path receives a validation response. Creating app inside a factory keeps registrations and owned state independent between tests.

References: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the difference between printing a dictionary and returning it from a route.
2. **Explain:** Explain which layers a TestClient request actually exercises.
3. **Modify:** Add a typed integer path parameter with an explicit result shape.
4. **Debug:** Find a blocking operation placed directly in an async route.

<details>
<summary>Hints</summary>

The path placeholder and parameter name must match.

</details>

## Independent task: http, routes & fastapi

In `Practice/01_HTTP_Routes_And_FastAPI.py`, complete this task:

Define create_app() returning a FastAPI application with GET /health -> {"status":"ok"} and GET /double/{value} accepting an integer and returning {"result": value*2}. In a guarded TestClient demonstration, request /double/3 and print its HTTP status and result. Use the real response, not fixed status values.

Expected output:

```text
200
6
```
