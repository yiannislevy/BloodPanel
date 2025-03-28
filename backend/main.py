from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import orm_models
from routers import upload, sessions

# Initialize FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows CORS for frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST etc.)
    allow_headers=["*"],  # Allows all headers
)

# Create tables
orm_models.Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(upload.router)
app.include_router(sessions.router)