import logging
import os
import random
import uuid

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from .models import Joke

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
logger.info("☁️ [AWS] Connected to DynamoDB table: 💾 %s in region: 🌎 %s", TABLE_NAME, AWS_REGION)

# TODO: Later try not to hardcode it? But then again, it requires a full db scan, thats expensive, find an alternative
categoriesdatabase = ['dad', 'short', 'yomama', 'programming', 'chuck-norris', 'web-scrape', 'general', 'misc', 'pun', 'insult']

"""
+----------------------+----------------+----------------+--------------------------------------------------------------+
|      INDEX NAME      |   PARTITION    |      SORT      |      PROJECTION                                              |
+----------------------+----------------+----------------+--------------------------------------------------------------+
| RandomShardIndex     | random_shard   | id             | INCLUDE                                                      |
|                      | (Number)       | (String)       | Attributes: id, category, joke                               |
|                      |                |                | Note: 10 shards (1-10) for ~380k items, O(1) random access   |
+----------------------+----------------+----------------+--------------------------------------------------------------+
| CategoryIndex        | category       | id             | ALL                                                          |
|                      | (String)       | (String)       |                                                              |
+----------------------+----------------+----------------+--------------------------------------------------------------+
"""

# DynamoDB helper functions
def get_random_joke():
    """
    Uses the RandomShardIndex GSI to jump to a random spot across shards.
    """
    try:
        logger.info("☁️ [AWS] Querying 🧊 RandomShardIndex for a random joke...")

        # Pick a random shard (1-10) and a random UUID seed for the jump
        selected_shard = random.randint(1, 10)  # noqa: S311
        random_seed = str(uuid.uuid4())

        query_params = {
            'IndexName': 'RandomShardIndex',
            'KeyConditionExpression': Key('random_shard').eq(selected_shard),
            'Limit': 1,
            'ConsistentRead': False,
            'ProjectionExpression': "id, category, joke"
        }

        # Query the GSI starting from that random ID within the selected shard
        response = table.query(**query_params, ExclusiveStartKey={'random_shard': selected_shard, 'id': random_seed})
        items = response.get("Items", [])

        # Fallback: If the seed was at the very end of the shard, look backwards from the end to grab the last available joke.
        if not items:
            logger.info("☁️ [AWS] Seed hit the end of 🧊 shard %s, grabbing last item...", selected_shard)

            # We remove ExclusiveStartKey and flip the search direction
            response = table.query(**query_params, ScanIndexForward=False)
            items = response.get("Items", [])

        raw_joke = items[0] if items else None

        if raw_joke:
            logger.info("☁️ [AWS] Random joke found: %s", raw_joke["id"])
            joke_model = Joke(**raw_joke)

            return joke_model.model_dump()

        logger.warning("☁️ [AWS] No jokes found in 🧊 shard: %s", selected_shard)
        return None

    except ClientError as e:
        logger.error("☁️ [AWS] DynamoDB Error: %s", e)
        return None

def get_random_ten_jokes():
    """
    Fetch 10 random jokes across shards using the RandomShardIndex GSI.
    """
    try:
        jokes = []
        max_jokes = 10

        attempts = 0
        max_attempts = 5

        while len(jokes) < max_jokes and attempts < max_attempts:
            attempts += 1

            selected_shard = random.randint(1, 10)  # noqa: S311
            random_seed = str(uuid.uuid4())

            query_params = {
                "IndexName": "RandomShardIndex",
                "KeyConditionExpression": Key("random_shard").eq(selected_shard),
                "Limit": 5,
                "ConsistentRead": False,
                "ProjectionExpression": "id, category, joke"
            }

            logger.info("☁️ [AWS] Querying 🧊 shard %s with seed %s (attempt #%d)", selected_shard, random_seed, attempts)

            # Query the GSI starting from that random ID within the selected shard
            resp = table.query(**query_params, ExclusiveStartKey={"random_shard": selected_shard, "id": random_seed})
            items = resp.get("Items", [])

            # Fallback (Look backwards from the end if the jump hit the end of the shard)
            if not items:
                logger.info("☁️ [AWS] Fallback query for 🧊 shard %s (no items found with seed)", selected_shard)

                # Flip search direction to grab the last 5 items in the shard
                resp = table.query(**query_params, ScanIndexForward=False)
                items = resp.get("Items", [])

            for item in items:
                if len(jokes) >= max_jokes:
                    break

                # Basic deduplication check
                if item not in jokes:
                    jokes.append(item)

        joke_models = [Joke(**j).model_dump() for j in jokes]
        random.shuffle(joke_models)

        logger.info("☁️ [AWS] Retrieved %d jokes", len(joke_models))
        return joke_models

    except Exception as e:
        logger.error("☁️ [AWS] Dynamo Error in get_random_ten: %s", e)
        return []

def get_joke_by_id(joke_id: str):
    """
    Retrieves a specific joke using its unique partition key.
    Uses ProjectionExpression to avoid fetching the random_shard metadata.
    """
    try:
        logger.info("☁️ [AWS] Fetching joke by ID: %s", joke_id)

        resp = table.get_item(Key={"id": joke_id}, ConsistentRead=False, ProjectionExpression="id, category, joke")
        item = resp.get("Item")

        if not item:
            logger.warning("☁️ [AWS] No joke found with id: %s", joke_id)
            return None

        # Use the Pydantic model for validation + ordered output
        joke_model = Joke(**item)

        return joke_model.model_dump()

    except ClientError as e:
        logger.error("☁️ [AWS] Error fetching joke by ID: %s", e)
        return None

def get_jokes_by_category(category: str):
    """
    Retrieves jokes matching a specific category using the CategoryIndex GSI.
    Uses ProjectionExpression to minimize data transfer costs.
    """
    try:
        logger.info("☁️ [AWS] Querying jokes in category: %s", category)

        resp = table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(category.lower()),
            ConsistentRead=False,
            Limit=20,
            ProjectionExpression="id, category, joke"
        )
        items = resp.get("Items", [])

        if not items:
            logger.warning("☁️ [AWS] No jokes found in category: %s", category)
            return []

        # Reconstruct using the Pydantic model
        joke_models = []

        for item in items:
            joke_models.append(Joke(**item).model_dump())

        return joke_models

    except ClientError as e:
        logger.error("☁️ [AWS] Error querying jokes by category: %s", e)
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

        logger.info("☁️ [AWS] Current table item count: %s", count)
        return count

    except ClientError as e:
        logger.error("☁️ [AWS] Error retrieving count from DynamoDB: %s", e)
        return 0
