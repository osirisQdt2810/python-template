## Setup environments:
```
    conda create -n template python==3.9
    conda activate template
```
To normally run the project, install package dependencies first:
```
    pip install pip-tool
```
by compiling `dev-requirements.in` to avoid package installation dependencies:
```
    pip-compile --strip-extras requirements/dev-requirements.in # --strip-extras flag controls <package>[extra] brackets are written into output dev-requirements.txt or not
```
Then, install dependencies:
```
    pip install -r requirements/dev-requirements.txt
```
## Install and build package:
### To install the project and its dependencies into your current Python environment:
Note that, you use this when you want to make your project's code importable, runnable and testable on your own machine:
```
    pip install -e .[dev,test]
```

### To distribute and create self-contained package files (.whl, .tar.gz)
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

### Journey to a beautiful python template project:
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
- Fifth, CI/CD (Continuous Integration/Continuous Deployment) automates testing, building, and deployment processes to ensure code quality and reliable releases:
#### CI/CD Implementation

##### Introduction
CI/CD represents the backbone of modern software development workflows, automating the journey from code changes to production deployment. While pre-commit hooks provide immediate feedback during development, CI/CD creates comprehensive quality gates that protect your main branch and automate release processes.

##### Purposes

**Why CI/CD is Essential:**
- **Quality Assurance**: Automatically run comprehensive tests across multiple environments
- **Early Bug Detection**: Catch integration issues before they reach production
- **Consistent Builds**: Ensure reproducible builds across different environments  
- **Automated Deployment**: Reduce human error in release processes
- **Team Collaboration**: Provide shared visibility into build status and quality metrics

**What CI/CD Provides:**
- **Continuous Integration (CI)**: Automated testing, linting, and building on every code change
- **Continuous Deployment (CD)**: Automated deployment to staging/production environments
- **Quality Gates**: Coverage thresholds, security scans, and performance checks
- **Artifact Management**: Build and store distributable packages
- **Notification Systems**: Alert teams about build failures or successful deployments

**When to Use CI/CD:**
- **Every repository**: Essential for professional development workflows
- **Team projects**: Critical for coordination and quality assurance
- **Production systems**: Mandatory for reliable deployment processes
- **Open source projects**: Provides transparency and builds trust with contributors

##### Pipeline Stages

Our CI/CD pipeline includes the following stages:

1. **Code Quality Checks**: Linting, formatting, type checking
2. **Testing**: Unit tests, integration tests, coverage analysis
3. **Build**: Package creation and validation
4. **Release**: Automated deployment to staging/production
- Sixth, test coverage rate: ![Coverage](https://codecov.io/gh/osirisQdt2810/python-template/branch/main/graph/badge.svg)