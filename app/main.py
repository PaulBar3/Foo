import uvicorn
from fastapi import FastAPI
from routers import router as expenses_router
from contextlib import asynccontextmanager
from database import create_db



@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(expenses_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



