Poetry is a dependency management and packaging tool in Python. It allows you to declare the libraries your project depends on and manage distribution packages.

## Installation of Poetry

Reference Documentation: [Poetry Official Documentation](https://python-poetry.org/docs/)

Install Poetry with the following PowerShell command:

```powershell

(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

```

### Setting Environment Variables

Ensure that the `poetry.exe` file is located in `C:\Users\18317\AppData\Local\Programs\Python\Python311\Scripts` and add this path to the environment variable:

```powershell

$Env:Path += ";C:\Users\18317\AppData\Roaming\Python\Scripts"; setx PATH "$Env:Path"

```

## Poetry Commands

### Project Initialization

Use the current directory's `pyproject.toml` environment:

```bash

poetry env use python

```

Create a new project (with `src` directory):

```bash

poetry new --src your_project

```

Initialize `pyproject.toml` file:

```bash

poetry init

```

Set Poetry configuration (e.g., to create virtual environments):

```bash

poetry config virtualenvs.create true --local

```

List Poetry configuration:

```bash

poetry config --list

```

Display environment information:

```bash

poetry env info

```

Create a project named `poetry-demo` with a `src` folder:

```bash

poetry new --src poetry-demo

```

Check Poetry version:

```bash

poetry --version

```

Add a Python package (e.g., add `request`):

```bash

poetry add request

```

Get the path to the virtual environment (for use in IDEs like PyCharm):

```bash

poetry env info --path

```

Export `requirements.txt` file:

```bash

poetry export -f requirements.txt --output requirements.txt

```

List virtual environments:

```bash

poetry env list

```

Remove a specific virtual environment:

```bash

poetry env remove <venv_name>

```

## Dependency Management

### Export `requirements.txt`

```bash

poetry export -f requirements.txt --output requirements.txt

```

### Install Dependencies from `requirements.txt`

```bash

poetry add $(cat requirements.txt)

```

## Publishing Packages

### Initialize PyPI

```powershell

poetry config pypi-token.pypi <token>

```

### Build and Publish

```bash

Remove-Item -Path 'dist/*' -Recurse -Force

poetry publish --build

```
