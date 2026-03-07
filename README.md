# RandomJokesAPI

# Virtual env

## Linux / macOS

```bash
python -m venv venv
source venv/Scripts/activate
```

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

# Install requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

# Run locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
