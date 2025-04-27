from pydantic import BaseModel, field_validator


class UserModel(BaseModel):
    email: str
    username: str
    phone: str

    @field_validator("email", "username", "phone")
    def fields_are_not_empty(cls, value):
        if value == "" or value is None:
            raise ValueError("Field is empty")
        else:
            return value
