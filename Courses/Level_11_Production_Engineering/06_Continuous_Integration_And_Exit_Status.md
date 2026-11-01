# Lesson 6: Continuous Integration & Exit Status

**Prerequisites:** Levels 1–10 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Continuous_Integration_And_Exit_Status.py`.

Run repeatable project checks in a clean environment and make failure visible to the calling system. A workflow file describes execution; it is not evidence that a remote run has succeeded.

## 1. Reproduce the local command first

A CI job should install the declared dependencies and run the same meaningful tests available locally. Establish the working directory and interpreter version explicitly. A pipeline that depends on undeclared packages from a developer machine is not reproducible.

Use subprocess with an argument list for a local runner rather than constructing a shell command from untrusted text. The process return code is part of the outcome: a failed test command must fail the pipeline, even if a later echo or print succeeds.

## 2. Keep test assertions meaningful

A CI server executing weak tests does not strengthen their claims. Run the actual implementation and check normal, boundary, failure, and state-preservation behavior. Integration tests requiring PostgreSQL or Redis need those services explicitly prepared, not an undocumented dependency on a developer's existing containers.

Collect coverage only when the tool actually measures it. Store reports as artifacts when they help investigation, but do not hardcode a percentage or treat a high number as proof that assertions cover important requirements.

## 3. Describe the workflow without publishing it

GitHub Actions uses workflow YAML under the repository's .github/workflows directory. This course keeps a template inside its level or capstone folder to respect the workspace organization; copying it to the activation path and publishing is a separate deliberate step.

Use narrowly scoped workflow permissions, a supported Python setup action, and a fresh install. For a hardened deployment, review dependency and action references and pin immutable versions according to the project's update policy. A moving tag and an immutable commit have different reproducibility properties.

## 4. Separate test, build, and deployment evidence

A passing local test run is not a built container, and a built image is not a successful deployment. Record the result at the boundary actually executed. Gate deployment on the required checks and environment controls rather than silently publishing from a tutorial exercise.

The independent task runs a real local pytest subprocess against a temporary tiny project. It demonstrates exit-status propagation without installing a recurring automation, contacting a remote CI provider, or pretending a workflow was run.

## Observe the subprocess exit code

`subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=folder, check=False)` waits for that real test process. The list supplies arguments directly, cwd selects its project directory, and check=False lets the caller inspect a nonzero status rather than raising automatically. The returned object's returncode is the observed status. `raise SystemExit(code)` propagates it from the launcher. A missing executable still raises its own launch error; check=False does not pretend every command started successfully.

In the supplied ci.yml template, name labels the workflow, on selects triggers, permissions limits its token, and jobs contains runnable jobs. Each job selects runs-on and steps. A uses step invokes an action; a run step executes a command; working-directory/defaults select where relative paths are resolved. needs can require an earlier job to pass. This capstone supplies configuration as scaffolding: inspect it and keep tests meaningful before activating anything remotely.

References: [GitHub setup-python](https://github.com/actions/setup-python), [GitHub checkout](https://github.com/actions/checkout).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict what a pipeline should return when pytest exits unsuccessfully.
2. **Explain:** Explain why the workflow working directory is part of its contract.
3. **Modify:** Create a fresh dependency environment for the same local command.
4. **Debug:** Find a shell sequence whose final success masks an earlier test failure.

<details>
<summary>Hints</summary>

Return the subprocess result instead of assuming the intended command succeeded.

</details>

## Independent task: continuous integration & exit status

In `Practice/06_Continuous_Integration_And_Exit_Status.py`, complete this task:

Define run_tests(folder) to execute the current interpreter's `-m pytest -q` in the supplied project folder and return its actual exit code. Use subprocess without shell=True. In a TemporaryDirectory, create calc.py with double(value) and test_calc.py asserting normal and zero behavior, run the real tests, and print `Pipeline exit: <code>`. Exit the launcher with that same code so a failing test run cannot be masked. Pytest's own report and timing vary; the correct implementation ends with Pipeline exit: 0.
