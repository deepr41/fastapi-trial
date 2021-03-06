from fastapi import FastAPI

from . import models
from .database import engine
from .routers import posts,users,auth,vote

# Removed after creation of alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {"message":"Hello World"}
