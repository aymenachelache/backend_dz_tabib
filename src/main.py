from src.database.db_setup import create_tables
from fastapi import FastAPI
from src.auth.routes import router as auth_router
from src.auth.backgroundTasks import delete_expired_tokens
import asyncio


app = FastAPI()

# Include the authentication router
app.include_router(auth_router)

@app.on_event("startup")
async def on_startup():
    create_tables()
    asyncio.create_task(delete_expired_tokens())
    print("Application is starting up...")

@app.get("/")
async def root():
    return {"message": "Welcome to DZ-Tabib!"}


@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down.")

# Additional routers can be included here if you have other modules
