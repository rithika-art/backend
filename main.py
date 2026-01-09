from fastapi import FastAPI
from database import engine, Base
from auth.routes import router as auth_router
from accounts.account_routes import router as accounts_router
import models
Base.metadata.create_all(bind=engine)
app=FastAPI(title="My FastAPI Project")
app.include_router(auth_router,prefix="/auth")
app.include_router(accounts_router)
@app.get("/")
def root():
    print("TEST API HIT")
    return{"message":"FASTAPI WORKING"}