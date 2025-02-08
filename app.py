from database.database import engine
from sqlmodel import SQLModel
from fastapi import FastAPI
from routers import usercrud,listingMembers
from dependencies import set_sqlite_pragmas
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI is starting...")
    set_sqlite_pragmas()
    SQLModel.metadata.create_all(engine)
    yield
    print("🛑 FastAPI is shutting down...")


app=FastAPI(
    title="jci_members",
    version="1.0",
    description="""a simple api to manage members of a jci club""",
    lifespan=lifespan
)
origins=[
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(usercrud.router)
app.include_router(listingMembers.router)
