from .database.database import engine
from sqlmodel import SQLModel
from fastapi import FastAPI
from routers import usercrud,listingMembers

from fastapi.middleware.cors import CORSMiddleware


app=FastAPI(
    title="jci_members",
    version="1.0",
    description="""a simple api to manage members of a jci club""",
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

SQLModel.metadata.create_all(engine)

app.include_router(usercrud.router)
app.include_router(listingMembers.router)
