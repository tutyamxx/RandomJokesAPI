import logging
import os
import random

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from dotenv import load_dotenv

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
    """
    Retrieves a single random joke from the DynamoDB table.

    Performs a full table scan with eventually consistent reads to optimize
    throughput, then selects one item at random from the result set.

    Returns:
        dict | None: A dictionary containing 'id', 'category', and 'joke'
            if successful. Returns None if the table is empty or an
            AWS service error occurs.

    Example:
        {
            "id": "012edec0-8638-4513-af41-aa34f5062d1b",
            "category": "programming",
            "joke": "Why do programmers prefer dark mode? Because light attracts bugs."
        }
    """
    try:
        logger.info("☁️ [AWS] Scanning DynamoDB table for a random joke...")

        # ConsistentRead=False doubles the throughput for the same cost
        resp = table.scan(ConsistentRead=False)
        items = resp.get("Items", [])

        if not items:
            logger.warning("☁️ [AWS] No jokes found in the table.")
            return None

        joke = random.choice(items)  # noqa: S311
        logger.info(f"☁️ [AWS] Returning joke with id: {joke['id']}")

        return joke

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error connecting to DynamoDB: {e}")
        return None

def get_random_ten_jokes():
    """
    Scans a pool of jokes and returns 10 randomly selected items.

    Fetches a limited set of items from the table (up to 50) to create a shuffle pool,
    then returns a subset to simulate randomness without scanning the entire table.

    Returns:
        list[dict]: A list containing up to 10 joke items.
            Returns an empty list if no items are found or an error occurs.
    """
    try:
        # We scan more than 10 to ensure we have a pool to shuffle from
        response = table.scan(Limit=50)
        items = response.get('Items', [])

        if not items:
            return []

        # Shuffle the results and grab 10
        random.shuffle(items)

        return items[:10]
    except Exception as e:
        print(f"Dynamo Error: {e}")  # noqa: T201
        return []

def get_joke_by_id(joke_id: str):
    """
    Retrieves a specific joke from DynamoDB using its unique partition key.

    Args:
        joke_id (str): The UUID or unique identifier of the joke.

    Returns:
        dict | None: The joke object if found, otherwise None.
            Uses eventually consistent reads to minimize RCU consumption.
    """
    try:
        logger.info(f"☁️ [AWS] Fetching joke by ID: {joke_id}")

        resp = table.get_item(
            Key={"id": joke_id},
            ConsistentRead=False  # Eventually consistent read (cheaper)
        )
        item = resp.get("Item")

        if not item:
            logger.warning(f"☁️ [AWS] No joke found with id: {joke_id}")
            return None

        return item

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error fetching joke by ID: {e}")
        return None


def get_jokes_by_category(category: str):
    """
    Filters the joke table for all items matching a specific category.

    Note:
        This implementation uses a Scan with a FilterExpression. While functional,
        this is O(n) complexity. For large datasets, consider a Global Secondary
        Index (GSI) on the 'category' attribute for O(1) Query performance.

    Args:
        category (str): The category name to filter by (e.g., 'programming').

    Returns:
        list[dict]: A list of jokes matching the category.
            Returns an empty list if no matches are found or on error.
    """
    try:
        logger.info(f"☁️ [AWS] Querying jokes in category: {category}")

        # Scans are expensive; ConsistentRead=False makes them 50% cheaper
        resp = table.scan(
            FilterExpression=Attr("category").eq(category),
            ConsistentRead=False
        )
        items = resp.get("Items", [])

        if not items:
            logger.warning(f"☁️ [AWS] No jokes found in category: {category}")
        return items

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error querying jokes by category: {e}")
        return []
