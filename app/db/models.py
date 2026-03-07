from pydantic import BaseModel


class Joke(BaseModel):
    """
    Data transfer object representing a single joke entity.

    This model defines the schema for jokes stored in DynamoDB and
    returned by the API endpoints. It ensures type safety and
    automatic validation of joke data.

    Attributes:
        id (str): The unique identifier (UUID) for the joke.
        category (str): The genre or type of joke (e.g., 'programming', 'dad').
        joke (str): The actual text content of the joke.
    """
    id: str
    category: str
    joke: str
