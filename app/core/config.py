import os
from dotenv import load_dotenv

# Load .env file
# load_dotenv()

class Settings:
    # Environment (development or production)
    ENV = os.environ.get("ENV", "development")

    # DynamoDB configuration
    DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE", "jokes_table")
    AWS_REGION = os.environ.get("AWS_REGION", "eu-west-2")

    # AWS credentials
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # Standard limit for /random and /{id}
    RATE_LIMIT_STANDARD = os.environ.get("RATE_LIMIT_STANDARD", "2/second")

    # Slightly stricter for /category/{name} as it may involve more DynamoDB scanning
    RATE_LIMIT_SEARCH = os.environ.get("RATE_LIMIT_SEARCH", "1/minute")

settings = Settings()
