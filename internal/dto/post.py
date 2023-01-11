from pydantic import BaseModel


class PostDTO(BaseModel):
    title: str
    text: str

    class Config:
        allow_mutations = False
        from_orm = True