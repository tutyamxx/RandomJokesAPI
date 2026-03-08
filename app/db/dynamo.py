import logging
import os
import random
import uuid

# from collections import Counter
import boto3
from boto3.dynamodb.conditions import Key
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
    Uses the Category GSI to jump to a random spot.
    """
    categoriesdatabase = ['dad', 'short', 'yomama', 'programming', 'chuck-norris', 'web-scrape', 'general', 'misc', 'pun', 'insult']

    try:
        logger.info("☁️ [AWS] Querying CategoryIndex for a random joke...")

        random_cat = random.choice(categoriesdatabase).lower()  # noqa: S311
        random_seed = str(uuid.uuid4())

        # Query the GSI starting from that random ID
        resp = table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(random_cat),
            Limit=1,
            ExclusiveStartKey={
                'category': random_cat,
                'id': random_seed
            }
        )

        items = resp.get("Items", [])

        # Fallback: If the seed was at the very end of the list, just grab the first joke in that category.
        if not items:
            resp = table.query(
                IndexName='CategoryIndex',
                KeyConditionExpression=Key('category').eq(random_cat.lower()),
                Limit=1
            )
            items = resp.get("Items", [])

        raw_joke = items[0] if items else None

        if raw_joke:
            logger.info(f"☁️ [AWS] Random joke found: {raw_joke['id']}")

            # Reconstruct the dictionary to force key order: id, category, joke
            ordered_joke = {
                "id": raw_joke.get("id"),
                "category": raw_joke.get("category"),
                "joke": raw_joke.get("joke")
            }

            return ordered_joke
        else:
            logger.warning(f"☁️ [AWS] No jokes found in category: {random_cat}")

        return None

    except ClientError as e:
        logger.error(f"☁️ [AWS] DynamoDB Error: {e}")
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

        resp = table.get_item(Key={"id": joke_id}, ConsistentRead=False)
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
    Retrieves all jokes matching a specific category using the CategoryIndex GSI.
    """
    try:
        logger.info(f"☁️ [AWS] Querying jokes in category: {category}")

        resp = table.query(IndexName='CategoryIndex', KeyConditionExpression=Key('category').eq(category.lower()))
        items = resp.get("Items", [])

        if not items:
            logger.warning(f"☁️ [AWS] No jokes found in category: {category}")
            return []

        # Reconstruct each joke in the list to force the key order
        ordered_items = []

        for item in items:
            ordered_joke = {
                "id": item.get("id"),
                "category": item.get("category"),
                "joke": item.get("joke")
            }
            ordered_items.append(ordered_joke)

        return ordered_items

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error querying jokes by category: {e}")
        return []

def get_joke_count():
    """
    Retrieves the total number of items in the DynamoDB table.

    Note:
        DynamoDB updates this count approximately every 6 hours.

    Returns:
        int: The number of items in the table. Returns 0 if an AWS service error occurs or the table is empty.
    """
    try:
        logger.info("☁️ [AWS] Fetching item count from DynamoDB...")

        # This is a metadata look-up; it does not consume Read Capacity Units (RCUs)
        count = table.item_count

        logger.info(f"☁️ [AWS] Current table item count: {count}")
        return count

    except ClientError as e:
        logger.error(f"☁️ [AWS] Error retrieving count from DynamoDB: {e}")
        return 0
