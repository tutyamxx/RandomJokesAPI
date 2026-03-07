import boto3
import os
import logging
import random
from dotenv import load_dotenv

from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# DynamoDB setup
AWS_REGION = os.getenv("AWS_REGION")
TABLE_NAME = os.getenv("DYNAMO_TABLE")

logger.info("☁️ [AWS] Initializing DynamoDB resource...")

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

table = dynamodb.Table(TABLE_NAME)
logger.info(f"☁️ [AWS] Connected to DynamoDB table: 💾 {TABLE_NAME} in region: 🌎 {AWS_REGION}")

# DynamoDB helper functions
def get_random_joke():
    try:
        logger.info("☁️[AWS] Scanning DynamoDB table for a random joke...")

        resp = table.scan()
        items = resp.get("Items", [])

        if not items:
            logger.warning("☁️ [AWS] No jokes found in the table.")
            return None

        joke = random.choice(items)
        logger.info(f"☁️ [AWS] Returning joke with id: {joke['id']}")
        return joke

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error connecting to DynamoDB: {e}")
        return None


def get_joke_by_id(joke_id: str):
    try:
        logger.info(f"☁️ [AWS] Fetching joke by ID: {joke_id}")
        resp = table.get_item(Key={"id": joke_id})
        item = resp.get("Item")

        if not item:
            logger.warning(f"☁️ [AWS] No joke found with id: {joke_id}")
            return None

        return item

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error fetching joke by ID: {e}")
        return None


def get_jokes_by_category(category: str):
    try:
        logger.info(f"☁️ [AWS] Querying jokes in category: {category}")
        resp = table.scan(
            FilterExpression=Attr("category").eq(category)
        )
        items = resp.get("Items", [])

        if not items:
            logger.warning(f"☁️ [AWS] No jokes found in category: {category}")
        return items

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error querying jokes by category: {e}")
        return []
