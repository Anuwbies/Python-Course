# Capstone Project 4.2: Real-Time Chat & Notification Microservice

## 📌 Project Overview
Build a scalable **Real-Time Group Chat & Push Notification Microservice** (similar to Slack or Discord) using FastAPI WebSockets, Redis Pub/Sub for horizontal cross-server broadcasting, PostgreSQL for message archiving, and Celery background workers for email/push notifications when users are offline.

---

## 🎯 Learning Objectives
- **FastAPI WebSockets**: Managing stateful two-way WebSocket connections, heartbeat pings, and disconnect lifecycles.
- **Horizontal Scaling via Redis Pub/Sub**: Broadcasting messages across multiple stateless FastAPI instances so connected clients on different server pods receive messages instantly.
- **Async Database Persistence**: Storing message history, chat channels, and user memberships in PostgreSQL asynchronously without blocking the WebSocket event loop.
- **Background Worker Integration**: Dispatching unread notification emails via Celery and Redis task brokers when recipients are not actively connected.
- **Connection Security**: Authenticating WebSocket handshakes via JWT tokens passed via query parameters or handshake headers.

---

## 🏗️ System Architecture

```text
[ Browser / App Client A ]        [ Browser / App Client B ]
          | (WebSocket)                     | (WebSocket)
          v                                 v
+--------------------+             +--------------------+
|  FastAPI Pod 1     |             |  FastAPI Pod 2     |
| (ConnectionManager)|             | (ConnectionManager)|
+--------------------+             +--------------------+
          \                                 /
           \                               /
            v                             v
          +---------------------------------+
          |      Redis Pub/Sub Broker       |
          |  (Channel: "room:{channel_id}") |
          +---------------------------------+
                          |
           +--------------+--------------+
           |                             |
           v                             v
+---------------------+       +---------------------+
| PostgreSQL Database |       | Celery Worker Pool  |
| - channels          |       | - offline email     |
| - message archive   |       |   notifications     |
| - read receipts     |       | - push webhooks     |
+---------------------+       +---------------------+
```

---

## 📋 Functional Requirements

### 1. WebSocket Connection Manager
- Accept incoming connections at `ws://localhost:8000/ws/channels/{channel_id}?token=<jwt>`.
- Validate JWT on handshake. Reject unauthorized connections with close code `4001`.
- Maintain active local connection pools per channel ID.

### 2. Redis Pub/Sub Cross-Pod Broadcast
- When a user sends a message `{"action": "send_message", "content": "Hello team!"}`:
  1. Validate content length and permissions.
  2. Persist message asynchronously to PostgreSQL.
  3. Publish JSON payload to Redis channel `channel:{channel_id}`.
  4. All FastAPI instances subscribed to that Redis channel receive the payload and broadcast it to their local connected WebSockets.

### 3. Presence & Typing Indicators
- Real-time `"user_typing"` events with a 3-second auto-expiry.
- `"user_joined"` and `"user_left"` presence notifications broadcasted to room participants.

### 4. Offline Notifications via Celery
- If a channel member is offline (not connected to any WebSocket) and mentioned with `@username`, trigger a Celery background task to send an email notification.

### 5. Historical Message Pagination REST API
- `GET /api/v1/channels/{channel_id}/messages?cursor=<message_id>&limit=50`: Fetch historical chat transcripts with cursor-based pagination.

---

## 📐 Phased Implementation Guide

### Phase 1: Connection Manager & Redis Pub/Sub
```python
from fastapi import WebSocket
from typing import Dict, Set
import asyncio
import redis.asyncio as aioredis
import json

class ChannelConnectionManager:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.redis_client = aioredis.from_url(redis_url)

    async def connect(self, channel_id: str, websocket: WebSocket):
        await websocket.accept()
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = set()
            # Start background subscriber for this channel
            asyncio.create_task(self._redis_channel_subscriber(channel_id))
        self.active_connections[channel_id].add(websocket)

    async def disconnect(self, channel_id: str, websocket: WebSocket):
        if channel_id in self.active_connections:
            self.active_connections[channel_id].discard(websocket)

    async def broadcast_local(self, channel_id: str, message: dict):
        if channel_id in self.active_connections:
            raw_msg = json.dumps(message)
            for ws in list(self.active_connections[channel_id]):
                try:
                    await ws.send_text(raw_msg)
                except Exception:
                    self.active_connections[channel_id].discard(ws)

    async def publish_message(self, channel_id: str, message: dict):
        await self.redis_client.publish(f"chat:{channel_id}", json.dumps(message))

    async def _redis_channel_subscriber(self, channel_id: str):
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(f"chat:{channel_id}")
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                data = json.loads(msg["data"].decode("utf-8"))
                await self.broadcast_local(channel_id, data)
```

### Phase 2: WebSocket Endpoint & Handshake Validation
Implement FastAPI route `websocket_endpoint` with token authentication and error dispatch.

### Phase 3: Background Message Archiving & Celery Tasks
Persist messages to PostgreSQL and schedule notification jobs.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Invalid JWT on WS Connect**| Connect with expired or forged JWT | Closes WebSocket immediately with status code `4001` |
| **Cross-Instance Message** | Client 1 on Pod A sends message to Channel 5 | Client 2 on Pod B in Channel 5 receives message in $< 20\text{ms}$ |
| **Abrupt Client Disconnect** | Force close browser / kill network connection | Server removes socket from active set without crashing event loop |
| **Offline Mention Notification**| Send message `@john check this out` when John is offline | Celery task enqueued; logs simulated email delivery to John |

---

## 🚀 Bonus Challenges
- **End-to-End Encryption (E2EE)**: Implement client-side key exchange so server only stores encrypted ciphertext.
- **File & Media Attachments**: Support uploading images/audio clips with direct pre-signed S3 links in chat payloads.
