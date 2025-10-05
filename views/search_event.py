import datetime

from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.event import EventDB, User
from models.event import VkUserInfo, Event, Payload


class Summary(BaseModel):
    pass

class SearchResult(BaseModel):
    summary: Summary


async def search_event(
    qr_id: str,
    from_: datetime.datetime,
    to_: datetime.datetime,
    session: AsyncSession,
) -> list[Event]:
    query = (
        select(EventDB, User)
        .join(User, EventDB.vk_user_id == User.vk_user_id)
        .where(
            and_(
                EventDB.timestamp.between(from_, to_),
                EventDB.qr_id == qr_id,
            )
        )
    )
    result = await session.execute(query)
    print(result)
    return [
        Event(
            event_type=event.event_type,
            timestamp=event.timestamp,
            vk_user_info=VkUserInfo(
                id=user.vk_user_id,
                first_name=user.first_name,
                last_name=user.last_name,
            ),
            payload=Payload(qr_id=event.qr_id),
        )
        for event, user in result.all()
    ]
