from pydantic import BaseModel

class Game(BaseModel):
    id: int
    name: str
    poster: str  # URL or path to the game poster image
    description: str
