# from src.database.db_setup import create_tables
from src.database.db_setup import initialize_database
from fastapi import FastAPI
from src.auth.routes import router as auth_router
from src.doctors.routes import router as doctor_router
from src.adv_search.routes import router as adv_search_router
from src.homepage.routes import router as homepage_router
from src.evaluate.routes import router as evaluate_router
from src.working_days.routes import router as working_days_router
from src.appointment.routes import router as appointment_router
from src.auth.backgroundTasks import delete_expired_tokens
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Additional routers can be included here if you have other modules

from fastapi import FastAPI


app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads/photos"), name="uploads")

# Allow requests from your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the authentication router
# src/main.py

from fastapi import FastAPI
from src.evaluate.routes import router as evaluate_router


app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(working_days_router)
app.include_router(homepage_router)
app.include_router(adv_search_router)
app.include_router(evaluate_router)

@app.on_event("startup")
async def on_startup():
    # create_tables()
    initialize_database()
    asyncio.create_task(delete_expired_tokens())
    print("Application is starting up...")


@app.get("/")
async def root():
    return {"message": "Welcome to DZ-Tabib!"}


@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down.")
