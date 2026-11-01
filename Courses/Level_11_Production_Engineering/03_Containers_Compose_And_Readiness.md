# Lesson 3: Containers, Compose & Readiness

**Prerequisites:** Levels 1–10 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Containers_Compose_And_Readiness.py`.

Package a repeatable process and connect it to actual dependencies. A printed startup line is not a running container, and a started process is not necessarily ready to serve useful requests.

## 1. Build the process environment

A Dockerfile selects a base image, copies dependencies and source, installs requirements, and declares the launch command. Copy the requirements before frequently changing source so image-layer caching can reuse dependency installation when appropriate.

A container is not a substitute for a virtual environment's source/dependency contract; it packages that contract with an operating-system userland and process configuration. Keep credentials and unrelated local files out of the build context through a deliberate .dockerignore.

## 2. Connect real services

Compose describes services, environment values, networks, volumes, and readiness dependencies. Service names are hostnames inside the Compose network. localhost inside an API container refers to that container, not the database service or the host computer.

A named volume can preserve database data across container recreation. Removing a volume is different from stopping containers. Keep published ports deliberate; the supplied learning API binds its host port to 127.0.0.1, while database and cache ports stay inside the Compose network.

## 3. Distinguish started and healthy

A healthcheck executes an actual probe. depends_on with condition service_healthy waits for a dependency's defined healthcheck rather than merely its process start. The API readiness route should still check the operation it needs because a dependency can fail after startup.

The reference Assets directory contains a real FastAPI probe executing PostgreSQL SELECT 1 and Redis PING. It returns 503 on dependency failure. The small Python copying task only places those assets in a chosen folder; it does not claim the containers were run.

## 4. Observe failure and recovery

After implementing the task, use Docker's real commands: `docker compose config --quiet`, `docker compose up --build --wait`, `docker compose ps`, and an HTTP request to /ready. Stop the cache and observe 503, restart it, and observe recovery. If Docker is unavailable, that runtime evidence remains outstanding rather than being replaced with a success print.

Inspect logs and actual health results when startup fails. Pin compatible image/dependency choices and record what was run. The later capstone adds migrations and a worker so startup ordering includes a completed migration step as well as healthy services.

## Read the supplied build and service definitions

In Assets/Dockerfile, FROM selects Python's base image, WORKDIR sets the process directory, COPY places files in the image, RUN installs requirements during image creation, and CMD supplies an argument-list launch command. The JSON-style CMD list avoids an extra shell's quoting and signal behavior. In Compose YAML, indentation defines mappings, `-` or brackets define lists, and quoted `host:container` ports map the listener. `build: .` selects the current build context; command overrides the image CMD for a worker or migration service.

`environment` supplies process text settings; `${TOKEN_SECRET:?...}` in the capstone requires an external value at Compose interpolation time. `service_healthy` waits for a probe; `service_completed_successfully` waits for a one-shot migration process to exit with zero. A named volume maps persistent database files; docker compose down stops services while preserving that named volume by default. Do not add a volume-removal option to an ordinary restart.

The copy exercise uses `from shutil import copyfile`. `copyfile(source, destination)` copies file contents and overwrites an existing destination file; it does not create its parent directory. Create the controlled destination with Path.mkdir first. Resolve Assets relative to this lesson's source tree using __file__ and parents[1], not the caller's working directory. Copy only the five specified names.

## Probe actual database and cache clients

The supplied service.py uses `psycopg.connect(url, connect_timeout=2)` as a managed PostgreSQL connection, executes SELECT 1, and closes on block exit. `redis.Redis.from_url(url, socket_connect_timeout=2, socket_timeout=2)` creates a cache client with bounded connection/read waits; ping performs the actual check. Catch psycopg.Error and redis.exceptions.RedisError as their library failure families. The later SQLAlchemy service uses `pool_pre_ping=True` to check reused connections and `pool_timeout=2` to bound waiting for a pooled connection. Psycopg connect_args can include `connect_timeout=2` and `options="-c statement_timeout=2000"` to bound connections and statement execution in milliseconds. These bounds target different waits; none is proof that a complete request always finishes in two seconds.

References: [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict what localhost means inside an API container.
2. **Explain:** Explain why depends_on without a health condition is insufficient readiness evidence.
3. **Modify:** Stop a dependency and identify which actual probe should fail.
4. **Debug:** Replace a printed starting message with a real process healthcheck.

<details>
<summary>Hints</summary>

The asset-copy result and the actual container-readiness result are separate observations.

</details>

## Independent task: containers, compose & readiness

In `Practice/03_Containers_Compose_And_Readiness.py`, complete this task:

Implement `copy_assets(destination)` to copy Dockerfile, compose.yaml, requirements.txt, service.py, and .dockerignore from this level's Assets directory into an existing or newly created destination. Use pathlib and shutil.copyfile; return the sorted copied names. Demonstrate copying to a TemporaryDirectory and print the names. The copied Compose stack must later be run with Docker to establish runtime health; the Python demonstration reports files only.

Expected output:

```text
['.dockerignore', 'Dockerfile', 'compose.yaml', 'requirements.txt', 'service.py']
```
