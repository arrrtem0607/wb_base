import os
import subprocess

GITIGNORE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
venv/
.env

# Node
node_modules/
dist/

# OS
.DS_Store
Thumbs.db

# Editor
.idea/
.vscode/
*.swp
"""

README = """# New Project

Описание проекта. Замените содержимое README по своему усмотрению.
"""

LICENSE = """MIT License

Copyright (c) [year] [your name]

Permission is hereby granted, free of charge, to any person obtaining a copy..."""

EDITORCONFIG = """root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true
"""

PRETTIERRC = """{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all"
}
"""

GITATTRIBUTES = """* text=auto
"""

ENV_EXAMPLE = """# Example .env
API_KEY=your_api_key_here
"""

REQUIREMENTS = """# Add your Python packages here
requests
pytest
"""

GITHUB_ACTIONS_YML = """name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest
"""

files = {
    ".gitignore": GITIGNORE,
    "README.md": README,
    "LICENSE": LICENSE,
    ".editorconfig": EDITORCONFIG,
    ".prettierrc": PRETTIERRC,
    ".gitattributes": GITATTRIBUTES,
    ".env.example": ENV_EXAMPLE,
    "requirements.txt": REQUIREMENTS,
}

print("Создаю стандартные файлы...")
for filename, content in files.items():
    with open(filename, "w") as f:
        f.write(content)
        print(f"Создан {filename}")

# GitHub Actions setup
os.makedirs(".github/workflows", exist_ok=True)
with open(".github/workflows/ci.yml", "w") as f:
    f.write(GITHUB_ACTIONS_YML)
    print("Создан .github/workflows/ci.yml для GitHub Actions")

print("\nИнициализирую git-репозиторий...")
subprocess.run(["git", "init"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Initial commit"])

repo_url = input("\nВведите ссылку на удалённый репозиторий: ")
if repo_url:
    subprocess.run(["git", "remote", "add", "origin", repo_url])
    print(f"Удалённый репозиторий добавлен: {repo_url}")
else:
    print("Ссылка не указана. Добавьте вручную с помощью 'git remote add origin <url>'")

print("\nПодготовка завершена ✅")
