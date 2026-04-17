from pydantic import BaseModel

class ContactForm(BaseModel):
    name: str
    phone: str | None = None
    email: str
    message: str