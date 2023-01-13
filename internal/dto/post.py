from pydantic import BaseModel
from uuid import UUID

class CreatePostDTO(BaseModel):
    title: str
    text: str

    class Config:
        allow_mutations = False
        orm_mode = True


class PostDTO(CreatePostDTO):
    id: UUID