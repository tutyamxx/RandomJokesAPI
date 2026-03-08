# 🤡 RandomJokesAPI ⚡

A high-performance, serverless-ready **FastAPI** application that serves up jokes from **AWS DynamoDB**, synced automatically from **S3**.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Amazon DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white)](https://aws.amazon.com/dynamodb/)
[![Amazon S3](https://img.shields.io/badge/Amazon%20S3-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Uvicorn](https://img.shields.io/badge/uvicorn-%23209285.svg?style=for-the-badge&logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)

## 🚀 Features

* **FastAPI Core**: Blazing fast asynchronous endpoints.
* **DynamoDB Backend**: NoSQL storage designed for ultra-low latency.
* **Smart Rate Limiting**: Built-in protection using `slowapi` to prevent API abuse.
* **Hardened Security Middleware**: Custom-built `SecurityHeadersMiddleware` implementing high-level browser protections.

## 🛠 Tech Stack

* **Backend**: Python 3.10+, FastAPI
* **Database**: Amazon DynamoDB
* **Rate Limiter**: Slowapi
* **SDK**: Boto3 (`AWS SDK for Python`)

## 🛣 API Endpoints

**Base URL:** [https://random-jokes-api-roan.vercel.app](https://random-jokes-api-roan.vercel.app)

| Method | Endpoint | Description | Rate Limit |
| :--- | :--- | :--- | :--- |
| `GET` | [/jokes/count](https://random-jokes-api-roan.vercel.app/jokes/count) | Get the total number of jokes in the database. DynamoDB updates this count approximately every `6 hours`. | `2/sec` |
| `GET` | [/jokes/random](https://random-jokes-api-roan.vercel.app/jokes/random) | Get one random joke | `2/sec` |
| `GET` | [/jokes/random/ten](https://random-jokes-api-roan.vercel.app/jokes/random/ten) | Get a batch of `10` random jokes | `2/sec` |
| `GET` | [/jokes/{joke_id}](https://random-jokes-api-roan.vercel.app/jokes/316c700d-cb0a-4a41-b853-5e6142867c2e) | Get a specific joke by UUID | `2/sec` |
| `GET` | [/jokes/category/{name}](https://random-jokes-api-roan.vercel.app/jokes/category/programming) | Get `20` jokes from a specific category | `1/min` |
| `GET` | [/jokes/countbycategory](https://random-jokes-api-roan.vercel.app/jokes/countbycategory) | Get the total number of jokes **per category** | `2/sec` |


# 📦 How to run it locally

## Virtual env

### Linux / macOS

```bash
python -m venv venv && source venv/Scripts/activate
```

### Windows

```bash
python -m venv venv && venv\Scripts\activate
```

## Install requirements

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

## Install developer requirements

```bash
pip install --upgrade pip && pip install -r requirements-dev.txt
```

## Run the linting

```bash
python -m ruff check .
```

## Run locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
