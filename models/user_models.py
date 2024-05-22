from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=8)
