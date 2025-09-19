import os
import asyncio
from fastapi import FastAPI, Depends, HTTPException

from decimal import Decimal
from database import engine, Base, get_db
import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession
import  redis.asyncio as  aioredis

app = FastAPI()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis = aioredis.from_url(REDIS_URL, encoding = "utf-8", decode_responses=True)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
@app.get("/")
async def root():
    return{"message": "hello welcome to my apis"}    
@app.post("/accounts/", response_model= schemas.AccountRead)
async def create_account(payload: schemas.AccountCreate, db:AsyncSession=Depends(get_db)):
    acc =  await crud.create_account(db, payload.name, payload.balance)
    return acc

@app.post("/transfer/")
async def transfer(req: schemas.TransferRequest, db:AsyncSession=Depends(get_db)):
    if req.idempotency_key:
        if await redis.get(req.idempotency_key):
            return {"status": "duplicate transaction"}
        
    await crud.transfer(db, req.from_account, req.to_account, req.amount)
    if req.idempotency_key:
        await redis.set(req.idempotency_key, "done", ex=3600)
    return {"status": "ok"}