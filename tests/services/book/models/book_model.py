from pydantic import BaseModel, field_validator


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    cover: int
    inventory: int
    daily_fee: float

    @field_validator("title", "author", "cover", "inventory", "daily_fee")
    def fields_are_not_empty(cls, value):
        if value == "" or value is None:
            raise ValueError("Field is empty")
        else:
            return value
