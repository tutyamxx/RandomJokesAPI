import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    # DynamoDB table and AWS region
    DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE", "jokes_table")
    AWS_REGION = os.environ.get("AWS_REGION", "eu-west-2")

    # AWS credentials
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # API rate limit (can be like "10/second" or "100/minute")
    RATE_LIMIT = os.environ.get("RATE_LIMIT", "2/second")

settings = Settings()
