from datetime import date
from sqlalchemy import select, func, and_
from app.services.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.db import async_session_maker

class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        """
        Находит все номера в отеле с информацией о доступности
        """
        async with async_session_maker() as session:
            # Подзапрос: количество забронированных комнат каждого типа
            booked_rooms_subq = (
                select(
                    Bookings.room_id,
                    func.count(Bookings.id).label("booked_count")
                )
                .where(
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from
                    )
                )
                .group_by(Bookings.room_id)
                .subquery()
            )
            
            # Основной запрос
            query = (
                select(
                    Rooms,
                    func.coalesce(booked_rooms_subq.c.booked_count, 0).label("booked_count"),
                    (Rooms.quantity - func.coalesce(booked_rooms_subq.c.booked_count, 0)).label("rooms_left"),
                    (Rooms.price * (date_to - date_from).days).label("total_cost")
                )
                .outerjoin(booked_rooms_subq, Rooms.id == booked_rooms_subq.c.room_id)
                .where(
                    and_(
                        Rooms.hotel_id == hotel_id,
                        (Rooms.quantity - func.coalesce(booked_rooms_subq.c.booked_count, 0)) > 0
                    )
                )
            )
            
            result = await session.execute(query)
            return result.mappings().all()