from fastapi import FastAPI
from auth_routes import router as auth_router
app=FastAPI(title="My FastAPI Project")
app.include_router(auth_router,prefix="/auth")
@app.get("/")
def root():
    print("TEST API HIT")
    return{"message":"FASTAPI WORKING"}