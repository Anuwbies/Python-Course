# Lesson 1: Configuration & Secrets

**Prerequisites:** Levels 1–10. **Practice file:** `Practice/01_Configuration_And_Secrets.py`.

Load deployment choices at a clear boundary, validate them before serving requests, and keep secret material out of source and diagnostics. Configuration is input to the application, not an excuse for hidden global state.

## 1. Separate code and deployment values

A database URL, log level, or signing key can vary between deployments while the application behavior stays the same. Read configuration once when constructing the service and pass the validated settings to the components that need them.

An environment variable is text. Convert numeric options and validate ranges just as you would for terminal input. A missing required value should cause a clear startup failure rather than silently selecting an insecure default.

## 2. Make validation observable without leaking values

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Settings:
    database_url: str = field(repr=False)
    token_ttl_seconds: int
```

A frozen settings object can hold validated choices. Do not include secrets in a default repr or log the entire environment. A diagnostic can name the missing setting without displaying the rejected value or a credential-bearing database URL.

Validate integer syntax and useful limits, not merely truthiness. A textual value of zero may be present but invalid. A long string is not proof of a randomly generated secret; length validation only rejects obviously inadequate configuration.

## 3. Generate and distribute keys deliberately

Use secrets.token_urlsafe or an appropriate secret-management system to generate high-entropy material. Keep it outside committed source and examples that pretend to be real deployment keys. Distinct services should receive only the secrets they need.

A .env file is a local configuration mechanism, not automatic encryption. A sample file can document required variable names without containing working credentials. Rotating a signing key affects active tokens and requires a coordinated acceptance policy rather than a blind edit in one process.

## 4. Keep configuration testable

A loader that accepts a mapping can be tested with an isolated dictionary. The launcher can supply os.environ in the actual deployment. This avoids changing the user's real environment merely to test one rejection case.

Record nonsecret environment details with operational evidence: interpreter, dependency versions, selected database, and configured bounds. Do not print a token or password merely to show that a setting was read. The next lesson uses validated key material at an authentication boundary.

## Keep secret fields out of generated representations

If a settings record includes a secret or a credential-bearing URL, declare that field with `field(repr=False)` from dataclasses. This suppresses it in the generated repr; it does not encrypt the value or stop a deliberate print of the field. `os.environ["TOKEN_SECRET"]` requires the key to exist, unlike get with a fallback. Name missing settings without echoing their contents. `secrets.token_urlsafe(32)` produces a newly generated URL-safe text secret from 32 random bytes; use a fresh deployment value rather than a committed sample.

References: [Secrets module](https://docs.python.org/3.13/library/secrets.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the outcome of a present but nonnumeric TTL setting.
2. **Explain:** Explain why key length does not prove randomness.
3. **Modify:** Load settings from an isolated mapping without modifying os.environ.
4. **Debug:** Remove an error message that includes the rejected secret value.

<details>
<summary>Hints</summary>

Validate a deployment value before creating components that rely on it.

</details>

## Independent task: configuration & secrets

In `Practice/01_Configuration_And_Secrets.py`, complete this task:

Define load_settings(mapping) returning a frozen Settings with database_url (excluded from its generated repr) and token_ttl_seconds. Require nonblank DATABASE_URL and an integer TOKEN_TTL_SECONDS from 1 through 3600, raising ValueError with a setting name on invalid input. Demonstrate a valid mapping with TTL 300 and an invalid zero TTL. Print the valid TTL and Rejected; do not print the database URL.

Expected output:

```text
300
Rejected
```
