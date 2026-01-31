from datetime import date
from sqlalchemy import select, func, and_
from app.services.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.db import async_session_maker

class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        """
        Находит все отели в локации с свободными номерами
        """
        async with async_session_maker() as session:
            # Подзапрос: количество забронированных номеров по отелю
            booked_rooms_subq = (
                select(
                    Rooms.hotel_id,
                    func.count(Bookings.id).label("booked_count")
                )
                .select_from(Rooms)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from
                    )
                )
                .group_by(Rooms.hotel_id)
                .subquery()
            )
            
            # Подзапрос: общее количество номеров по отелю
            total_rooms_subq = (
                select(
                    Rooms.hotel_id,
                    func.count(Rooms.id).label("total_rooms"),
                    func.sum(Rooms.quantity).label("total_quantity")
                )
                .group_by(Rooms.hotel_id)
                .subquery()
            )
            
            # Основной запрос
            query = (
                select(
                    Hotels,
                    total_rooms_subq.c.total_rooms,
                    total_rooms_subq.c.total_quantity,
                    func.coalesce(booked_rooms_subq.c.booked_count, 0).label("booked_count"),
                    (total_rooms_subq.c.total_quantity - func.coalesce(booked_rooms_subq.c.booked_count, 0)).label("rooms_left")
                )
                .join(total_rooms_subq, Hotels.id == total_rooms_subq.c.hotel_id)
                .outerjoin(booked_rooms_subq, Hotels.id == booked_rooms_subq.c.hotel_id)
                .where(
                    and_(
                        Hotels.location.ilike(f"%{location}%"),
                        (total_rooms_subq.c.total_quantity - func.coalesce(booked_rooms_subq.c.booked_count, 0)) > 0
                    )
                )
            )
            
            result = await session.execute(query)
            return result.mappings().all()