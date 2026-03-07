from pydantic import BaseModel

class Joke(BaseModel):
    id: str
    category: str
    joke: str
