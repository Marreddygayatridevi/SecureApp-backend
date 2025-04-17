from fastapi import FastAPI
import models
from database import engine
from auth import router as auth_router
from Notes import router as notes_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(notes_router, prefix="/note", tags=["Notes"])
