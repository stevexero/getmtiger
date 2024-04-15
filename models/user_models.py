from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    user_id: constr(min_length=1)
    email: EmailStr
