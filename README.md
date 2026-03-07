# 🤡 RandomJokesAPI ⚡

A high-performance, serverless-ready **FastAPI** application that serves up jokes from **AWS DynamoDB**, synced automatically from **S3**.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## 🚀 Features

* **FastAPI Core**: Blazing fast asynchronous endpoints.
* **DynamoDB Backend**: NoSQL storage designed for ultra-low latency.
* **Smart Rate Limiting**: Built-in protection using `slowapi` to prevent API abuse.
* **Hardened Security Middleware**: Custom-built `SecurityHeadersMiddleware` implementing high-level browser protections:
    * **Resource Isolation**: Enforces `COOP` and `CORP` to prevent cross-origin data leaks and side-channel attacks.
    * **Zero-Trust CSP**: Strict Content Security Policy that locks down script/object sources to `'self'`.
    * **Hardware Lockdown**: Permissions Policy that explicitly disables access to camera, microphone, and geolocation.
    * **Production Guard**: Automatic **HSTS** enforcement (`1-year max-age`) and server signature stripping.

## 🛠 Tech Stack

* **Backend**: Python 3.10+, FastAPI
* **Database**: Amazon DynamoDB
* **Rate Limiter**: Slowapi
* **SDK**: Boto3 (`AWS SDK for Python`)

## 🛣 API Endpoints

| Method | Endpoint | Description | Rate Limit |
| :--- | :--- | :--- | :--- |
| `GET` | `/jokes/random` | Get one random joke | `2/sec` |
| `GET` | `/jokes/random/ten` | Get a batch of 10 random jokes | `2/sec` |
| `GET` | `/jokes/{joke_id}` | Get a specific joke by UUID | `2/sec` |
| `GET` | `/jokes/category` | List all unique joke categories | `1/min` |
| `GET` | `/jokes/category/{name}` | Get jokes from a specific category | `1/min` |


# 📦 How to run it locally

## Virtual env

### Linux / macOS

```bash
python -m venv venv
source venv/Scripts/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Run locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
