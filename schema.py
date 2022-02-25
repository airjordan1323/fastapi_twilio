from pydantic import BaseModel


class Check(BaseModel):
    from_: str
    to_: str
