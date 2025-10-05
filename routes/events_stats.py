import datetime

import pydantic
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_sqlite_session
from views.search_event import search_event

router = APIRouter()


class SearchRequest(pydantic.BaseModel):
    qr_id: str
    from_: datetime.datetime | None = Field(default=None, alias="from")
    to: datetime.datetime | None = Field(default=None, alias="to")


@router.post("/events/links/stats")
async def post_events_stats(
    request: SearchRequest,
    session: AsyncSession = Depends(get_sqlite_session),
) -> dict:
    return {
        "events": await search_event(
            qr_id=request.qr_id,
            from_=request.from_,
            to_=request.to,
            session=session,
        )
    }
