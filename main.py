from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

import routes
from db.base import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(routes.router)
