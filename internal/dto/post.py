from pydantic import BaseModel


class PostDTO(BaseModel):
    title: str
    text: str
    user_id: str