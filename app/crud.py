from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Account
from decimal import Decimal
from fastapi import HTTPException

async def create_account(db:AsyncSession, name:str, balance:Decimal):
    acc = Account(name=name, balance=balance)
    db.add(acc)
    await db.commit()
    await db.refresh(acc)
    return acc

async def get_account(db:AsyncSession, account_id:int):
    res = await db.execute(select(Account).where(Account.id == account_id))
    return res.scalar_one_or_none()


async def transfer(db: AsyncSession, from_id: int, to_id:int, amount:Decimal):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    async with db.begin():
        res1 = await db.execute(select(Account).where(Account.id ==from_id).with_for_update())
        from_acc = res1.scalar_one_or_none()
        res2 = await db.execute(select(Account).where(Account.id == to_id).with_for_update())
        to_acc = res2.scalar_one_or_none()

        if not from_acc or not to_acc:
            raise HTTPException(status_code=404, detail="Account not found")
        if from_acc.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficeint funds")
        from_acc.balance -= amount
        to_acc.balance +=amount

        db.add(from_acc)
        db.add(to_acc)

    return {"from Account": from_acc, "to_account": to_acc}