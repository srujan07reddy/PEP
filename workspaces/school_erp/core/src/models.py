from pydantic import BaseModel

class CoreModel(BaseModel):
    id: str
    status: str
