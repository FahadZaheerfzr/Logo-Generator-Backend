#model for open ai image generation
from pydantic import BaseModel

class Logo(BaseModel):
    name: str
    url: str