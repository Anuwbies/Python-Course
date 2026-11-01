# Level 11: Production Engineering

**Stage:** Professional. **Prerequisites:** Levels 1–10.

Deploy and diagnose a bounded service with explicit access control, durable local effects, cache policy, dependency readiness, meaningful test/CI boundaries, and a rehearsed recovery procedure.

## Reading order

| Lesson | Guide | Saved task |
| --- | --- | --- |
| 1 | [Configuration & Secrets](01_Configuration_And_Secrets.md) | [Practice](Practice/01_Configuration_And_Secrets.py) |
| 2 | [Authentication, Tokens & Authorization](02_Authentication_Tokens_And_Authorization.md) | [Practice](Practice/02_Authentication_Tokens_And_Authorization.py) |
| 3 | [Containers, Compose & Readiness](03_Containers_Compose_And_Readiness.md) | [Practice](Practice/03_Containers_Compose_And_Readiness.py) |
| 4 | [Durable Jobs, Retries & Idempotency](04_Durable_Jobs_Retries_And_Idempotency.md) | [Practice](Practice/04_Durable_Jobs_Retries_And_Idempotency.py) |
| 5 | [Caching, Expiration & Invariants](05_Caching_Expiration_And_Invariants.md) | [Practice](Practice/05_Caching_Expiration_And_Invariants.py) |
| 6 | [Continuous Integration & Exit Status](06_Continuous_Integration_And_Exit_Status.md) | [Practice](Practice/06_Continuous_Integration_And_Exit_Status.py) |
| 7 | [Observability, Readiness & Recovery](07_Observability_Readiness_And_Recovery.md) | [Practice](Practice/07_Observability_Readiness_And_Recovery.py) |

Continue with the [Operational shared-catalog service capstone](../../Capstones/Level_11_Production_Engineering/README.md).

## Working through this level

Read the detailed explanation, trace the examples, and complete the practice ladder before the independent task. Each file in `Practice/` contains the full task, accepted inputs, and expected behavior as comments. Write your own implementation below those comments. Reference implementations are in `Solutions/`; compare them after an attempt.

Ask the assistant to review your saved submission when ready. Progress is recorded manually after review, including revisions and topics to revisit. Independent-task sections contain only the assignment and its expected behavior.

## Environment and run commands

Install this level's requirements in a project environment. Container exercises additionally require Docker with Compose and Linux containers. Lesson reference scripts run locally; the capstone uses real PostgreSQL/Redis services. Its local pytest suite deliberately isolates the cache and does not pretend to test remote services.

## Advancement

Deploy and diagnose a bounded service with explicit access control, durable local effects, cache policy, dependency readiness, meaningful test/CI boundaries, and a rehearsed recovery procedure.

Demonstrate the capstone with its documented normal, boundary, and failure cases and explain one small requirement change. Record evidence in [the Level 11 progress record](../../Progress/Level_11_Production_Engineering.md). Running a reference does not complete your own submission.

## Scope and next steps

This is a learning deployment with classroom database credentials on an internal network and a short-lived local token issuer. No claim of complete production hardening is made. Select an actual identity provider, secret rotation, TLS, backup retention, and operational policies for a real deployment.
