# Python Package Dependency Management Guide

This document outlines best practices for managing Python package dependencies to ensure **reproducibility**, **maintainability**, and a clear separation between runtime and development requirements. It is tailored for a project using `pyproject.toml` (following [PEPs 518](https://peps.python.org/pep-0518/) and [621](https://peps.python.org/pep-0621/)) and `pip-tools` for pinning versions in `requirements/` files.

## 1. Understanding `pyproject.toml` and `requirements/` Files

### `pyproject.toml`: Source of Truth for Dependency Declaration
Use `pyproject.toml` to declare all dependencies in a standardized, tool-agnostic format:

- **Runtime Dependencies** (`[project.dependencies]`): Packages required for the project to run (e.g., `typer`). These are automatically installed via `pip install your-package`.
- **Optional Dependencies** (`[project.optional-dependencies]`): Extras for specific tasks, installed via `pip install '.[extra-name]'`. Common groups include:
  - `dev`: Development tools like linters (`ruff`), type checkers (`mypy`), formatters (`docformatter`), and utilities (`pip-tools`, `pre-commit`).
  - `test`: Testing tools like `pytest` and `pytest-cov`.

This approach avoids duplication, replaces older files like `setup.py` or `setup.cfg`, and ensures compatibility with tools like `pip`, `poetry`, or `hatch`.

**When to Use**: Always for declaring **unpinned** dependencies (e.g., without specific versions like `==1.2.3`) to maintain flexibility across environments.

### `requirements/` Files: Pinned Versions for Reproducibility
Use `requirements/` files (e.g., `dev-requirements.in` and `dev-requirements.txt`) to manage **pinned** (version-locked) dependencies for specific environments (e.g., CI/CD, local development):

- **`.in` Files**: List package names, either unpinned or with loose constraints (e.g., `ruff>=0.1`).
- **`.txt` Files**: Generated from `.in` files using `pip-compile`, containing exact versions (e.g., `ruff==0.1.5`) resolved for your Python version and constraints.

**When to Use**: For environments requiring exact reproducibility, such as CI pipelines or production deployments. Always start dependency declarations in `pyproject.toml` and generate `requirements/` files from it to avoid duplication.

**Key Principle**: `pyproject.toml` defines *what* is needed; `requirements/` specifies *how* (exact versions). This prevents version drift and ensures deliberate upgrades.

## 2. Building the Package

Running `python -m build` is sufficient to create source distribution (`sdist`) and wheel (`whl`) files if:

- The `[build-system]` section in `pyproject.toml` is configured correctly (e.g., `requires = ["setuptools>=61.0"]`, `build-backend = "setuptools.build_meta"`).
- The `build` package is installed (`pip install build`).

**Do You Need `requirements/*.txt` for Building?** No, unless custom build hooks (e.g., `setup.py` extensions) require specific dependencies. Runtime dependencies are embedded as metadata in the package, not installed during the build.

**Best Practices**:
- In CI (e.g., `actions.yml` with `build-package: true`):
  - Install `build`:
    ```bash
    pip install build
    python -m build
    ```
    * Avoid installing extras or `requirements/` files, as they are irrelevant to building.
* For complex builds (e.g., C extensions), add dependencies to `[build-system.requires]`.

### 3. Development Tasks (Linting, Formatting, Testing)

The current CI setup (in `actions.yml` for `build-package: false`) involves:

* `pip install -e '.[dev,test]'`: Installs the project in editable mode with dev/test extras (unpinned).
* `pip-compile requirements/dev-requirements.in`: Generates pinned `.txt` files.
* `pip install -r requirements/dev-requirements.txt`: Installs pinned versions.

**Redundancy Issue:** Installing unpinned extras before pinned versions can cause unnecessary downloads or conflicts and risks drift if `dev-requirements.in` diverges from `pyproject.toml`.

**Best Practices:**
Use `pyproject.toml` as the single source. Generate pinned dependencies with:
```bash
pip-compile --extra=dev --extra=test --output-file=requirements/dev-requirements.txt pyproject.toml
```
This includes runtime dependencies and specified extras.

* In CI/local setup:
    * Run `pip-compile` (if not pre-committed).
    * Install with:
        ```bash
        pip install -r requirements/dev-requirements.txt
        ```
* For editable installs (useful for testing changes), add `--editable .` to the `pip install` command. Non-editable installs suffice for most CI tasks (e.g., linting, testing).
* Commit `dev-requirements.txt` to version control for reproducibility. Regenerate periodically for updates.
* For local development, use virtual environments (`venv` or `pipenv`) and install from pinned files to align with CI.

### 4. Placement of Tools: [dev,test] vs. requirements/

**Correct Placement**: Tools like `mypy`, `ruff`, `pytest`, `pytest-cov`, `pip-tools`, `pre-commit`, and `docformatter` belong in `[project.optional-dependencies.dev]` or `.test`, not in `[project.dependencies]` (runtime) or `requirements/*.in`.

* Runtime dependencies (e.g., `typer`) are for end-users.
* Development/test tools are for developers, keeping user installations lightweight.

**Avoid Direct `requirements/` Declarations:** Generate `requirements/` files from `pyproject.toml` to prevent maintaining duplicate lists.

**Tool Verification:**

* `dev`: `mypy`, `ruff`, `pip-tools`, `pre-commit`, `docformatter` (for type checking, linting/formatting, dependency management, hooks, docstring checks).
* `test`: `pytest`, `pytest-cov` (for testing and coverage).
* For tools used across multiple extras, declare once in `pyproject.toml` and include in generation with multiple `--extra` flags.

### 5. Recommended Workflow and File Updates

**Update `actions.yml`**

For non-build jobs, replace the install steps with:
```bash
python -m pip install --upgrade pip
pip install pip-tools
pip-compile --extra=dev --extra=test --output-file=requirements/dev-requirements.txt pyproject.toml requirements/dev-requirements.in
pip install -r requirements/dev-requirements.txt
```
* Add `-e .` to the last `pip install` if editable mode is needed.
* Update `cache-dependency-path` to `pyproject.toml` if `dev-requirements.in` is eliminated.
* No changes are needed for build jobs.

### Minimize or Eliminate dev-requirements.in

If possible, remove `dev-requirements.in` to rely solely on `pyproject.toml`. Use `.in` files only for custom constraints not in `pyproject.toml`.

### Local Development Workflow

1. Update dependencies in `pyproject.toml`.
2. Run:

```bash
pip-compile --extra-dev --extra-test pyproject.toml -o requirements/dev-requirements.txt
```
3. Create/activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements/dev-requirements.txt
```
5. Run tools (e.g., `ruff check`, `pytest`).

### Tools and Extensions

* Consider `pipenv` or `poetry` for managed environments as project complexity grows.
* Leverage `pre-commit` hooks (already in dev extras) to enforce `pip-compile` on commits.
* Update pinned versions with:
```bash
pip-compile --upgrade
```
This structure aligns with Python Packaging Authority (PyPA) recommendations, promoting efficiency and reproducibility. For evolving projects (e.g., adding `docs` extras), extend `[project.optional-dependencies]` as needed. If specific errors arise or `dev-requirements.in` contents are available, further refinements can be provided.

### Instructions to Download
1. Copy the above content.
2. Paste it into a text editor (e.g., VS Code, Notepad).
3. Save the file with the name `README.md`.
4. Alternatively, if using a terminal, you can create the file directly:

```bash
cat << EOF > README.md
[Paste the markdown content here]
EOF
```
This README uses markdown features like headers (`###`), bold/italic text (`**`, `*`), code blocks (``` ` ```), and links for clarity. Let me know if you need further formatting adjustments or additional sections!