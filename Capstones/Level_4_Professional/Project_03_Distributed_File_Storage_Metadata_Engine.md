# Capstone Project 4.3: Distributed Media Storage & Processing API

## 📌 Project Overview
Build a secure, enterprise-grade **Cloud Media Storage & Asynchronous Processing Service** (similar to Cloudinary or AWS S3 + Lambda). The platform supports direct chunked multipart file uploads, cryptographic SHA-256 deduplication, automatic image resizing/transcoding via Celery workers, scoped presigned URL generation, and storage quota enforcement.

---

## 🎯 Learning Objectives
- **Object Storage Abstraction**: Building a pluggable storage provider interface supporting Local Filesystem, MinIO, and AWS S3.
- **Chunked Multipart Streaming**: Handling multi-gigabyte file uploads via asynchronous streams without exhausting server RAM.
- **Cryptographic Deduplication**: Hashing file content buffers to detect duplicate uploads across users and share identical disk blocks safely.
- **Distributed Image/Media Processing**: Offloading heavy image transformations (thumbnails, WebP conversion, watermarking) to Celery task workers.
- **Secure Access Delegation**: Implementing time-limited HMAC-signed presigned download URLs with permission validation.

---

## 🏗️ System Architecture

```text
                      [ Client File Upload ]
                                 |
                                 v  (Chunked stream)
                     [ FastAPI Storage Gateway ]
                                 |
           +---------------------+---------------------+
           |                                           |
           v (Metadata & Deduplication Check)          v (Async Write)
  [ PostgreSQL Database ]                      [ Object Storage ]
  - files & hashes                             - S3 / MinIO / Local
  - storage quotas & user permissions          - raw binary objects
           |
           v (Trigger processing event)
   [ Redis Task Broker ]
           |
           v
  [ Celery Media Workers ]
  - Generate 128x128 Thumbnails
  - Convert PNG/JPEG -> WebP
  - Extract EXIF metadata
```

---

## 📋 Functional Requirements

### 1. Storage Backend Abstraction
```python
class StorageProvider(ABC):
    @abstractmethod
    async def upload_stream(self, file_key: str, stream: AsyncIterator[bytes]) -> int:
        """Uploads a stream of bytes to storage. Returns total bytes written."""
        pass

    @abstractmethod
    async def get_download_url(self, file_key: str, expires_in_seconds: int = 3600) -> str:
        """Generates a temporary signed download URL."""
        pass
```

### 2. Chunked Stream Ingestion & SHA-256 Deduplication
- Process upload streams in 64 KB chunks.
- Compute SHA-256 hash incrementally as chunks arrive.
- If a file with the identical SHA-256 checksum already exists in the system:
  - Link the new user record to the existing physical file key.
  - Avoid writing duplicate bytes to disk/S3 (100% storage savings).

### 3. Asynchronous Media Transformation (Celery)
- Once an image (`.jpg`, `.png`) finishes uploading, dispatch a Celery worker to:
  1. Generate a responsive thumbnail (`150x150`).
  2. Generate a compressed high-efficiency `.webp` variant.
  3. Strip invasive EXIF GPS coordinate metadata for privacy.
  4. Update file metadata record in PostgreSQL to status `PROCESSED`.

### 4. Quota Enforcement & Rate Limits
- Users on Free plan capped at 500 MB total stored storage.
- File upload requests exceeding remaining user quota rejected with HTTP `413 Payload Too Large`.

---

## 📐 Phased Implementation Guide

### Phase 1: Streaming File Ingestion & Deduplication
```python
import hashlib
from fastapi import UploadFile, HTTPException

async def handle_streaming_upload(upload_file: UploadFile, storage: StorageProvider) -> tuple[str, int]:
    hasher = hashlib.sha256()
    total_bytes = 0
    temp_chunks = []

    while chunk := await upload_file.read(64 * 1024):  # 64 KB chunks
        hasher.update(chunk)
        total_bytes += len(chunk)
        temp_chunks.append(chunk)

    file_hash = hasher.hexdigest()
    # Check if duplicate exists in database
    # If not, write chunks to storage provider
    return file_hash, total_bytes
```

### Phase 2: Presigned HMAC URL Generator
Generate cryptographically signed download tokens valid for $N$ minutes.

### Phase 3: Celery Image Worker & Test Suite
Implement Pillow/Image transcoding tasks and write integration tests with test storage backends.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Duplicate File Upload** | Upload 10MB file previously uploaded by another user | Hash matches; returns instant success without extra storage consumed |
| **Quota Exceeded** | User with 490MB storage attempts to upload 20MB file | Rejects upload immediately with HTTP `413 Payload Too Large` |
| **Expired Download Link** | Access presigned URL 65 minutes after 1-hour expiry | Returns HTTP `403 Forbidden` with expired signature message |
| **Corrupted Media File** | Upload `.jpg` containing random non-image garbage bytes | Worker catches decompression error, marks file status `FAILED_TRANSCODE` |

---

## 🚀 Bonus Challenges
- **Video Transcoding**: Integrate `ffmpeg` to extract video duration, generate animated preview GIFs, and transcode MP4 to HLS streaming format.
- **S3 Multipart Upload Direct from Browser**: Issue presigned multi-part S3 upload URLs for direct browser-to-S3 uploads.
