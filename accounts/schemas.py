from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=3)
    balance: float = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3)

class AccountUpdate(BaseModel):
    name: str | None = None
    balance: float | None = None