## 1. Setup environments:
```
    conda create -n template python==3.9
    conda activate template
```
To normally run the project, install package dependencies first:
```
    pip install pip-tools
```
by compiling `dev-requirements.in` to avoid package installation dependencies:
```
    pip-compile --strip-extras requirements/dev-requirements.in # --strip-extras flag controls <package>[extra] brackets are written into output dev-requirements.txt or not
```
Then, install dependencies:
```
    pip install -r requirements/dev-requirements.txt
```
## 2. Install and build package:
### 2.1. To install the project and its dependencies into your current Python environment:
Note that, you use this when you want to make your project's code importable, runnable and testable on your own machine:
```
    pip install -e .[dev,test]
```

### 2.2. To distribute and create self-contained package files (.whl, .tar.gz)
Note that, you use this when use want to release your package. You are ready to share your code with others.
When you are finally ready to distribute your project to others, you can run the command that builds the .whl file you were originally looking for.
```
    pip install build
```
Run the build command:
```
    python -m build
```
This will create a `/dist` directory, and inside you will dinf your new `.whl` file, ready to be uploaded to PyPi.

## 3. Journey to a beautiful python template project:
- First, use pip-compile to automatically generate requirements.txt dependencies from a high-level requirements.in file. This uses in step setup environment for running the code in development mode.
- Second, use pyproject.toml for building and installing our whole project to a package (that files also includes all the tools' configuration as well)
- Third, related to version control, when we want to commit/push current implementation, the code needa pass our pre-commit hooks (we could test our hooks by running commands: `pre-commit run --all-files --verbose`)
- Fourth, calculating the test coverage using `pytest --cov=src tests/`, the table will show:
  ```
  Name                              Stmts   Miss  Cover
  -----------------------------------------------------
  src/my_package/calculator.py         19      0   100%
  src/my_package/cli.py                32     32     0%
  -----------------------------------------------------
  TOTAL                                79     60    24%
  ```
  **Coverage Table Explanation:**
  - `Stmts`: Total executable code lines in each file
  - `Miss`: Number of lines NOT executed during tests  
  - `Cover`: Percentage of lines that were tested (Stmts - Miss) / Stmts * 100
  - **Professional goal**: Aim for 80%+ coverage, 90%+ is excellent
  - Use `pytest --cov=src --cov-report=term-missing tests/` to see which specific lines need testing
- Fifth, CI/CD (Continuous Integration/Continuous Deployment) automates testing, building, and deployment processes to ensure code quality and reliable releases. See [CI/CD workflow documentation](docs/CI-CD%20Workflow.md) for details.
- Sixth, test coverage rate: ![Coverage](https://codecov.io/gh/osirisQdt2810/python-template/branch/main/badge.svg)