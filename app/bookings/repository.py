from app.services.base import BaseDAO
from app.bookings.models import Bookings
from app.hotels.models import Rooms
from sqlalchemy import select, func, and_, or_, insert
from datetime import date
from ..db import async_session_maker
from ..exceptions import RoomCannotBeBooked

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_cte = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from
                            )
                        )
                    )
                )
                .cte("booked")
            )
            
            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_cte.c.room_id)).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_cte, booked_cte.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_cte.c.room_id)
            )
            
            print(str(get_rooms_left.compile(compile_kwargs={"literal_binds": True})))
            
            result = await session.execute(get_rooms_left)
            rooms_left = result.scalar()
            
            print(f"Rooms left: {rooms_left}")

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(room_id=room_id, user_id=user_id, date_from=date_from, date_to=date_to, price=price).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return RoomCannotBeBooked