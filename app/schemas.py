from pydantic import BaseModel 
from decimal import Decimal

class AccountCreate(BaseModel):
    name: str
    balance: Decimal = 0


class AccountRead(BaseModel):
    id:int
    name:str
    balance: Decimal

    class Config:
        orm_mode = True

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: Decimal
    idempotency_key: str | None = None

