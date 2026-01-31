from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.repository import BookingDAO
from app.users.models import Users
from app.users.dependencies import get_current_user
from datetime import date
from pydantic import BaseModel
from ..exceptions import RoomCannotBeBooked
from app.bookings.schemas import SBookingWithDetails

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

class BookingCreate(BaseModel):
    room_id: int
    date_from: date
    date_to: date

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(
    booking: BookingCreate,
    user: Users = Depends(get_current_user)
    ):
    print(f"Received booking: {booking}")
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=booking.room_id,
        date_from=booking.date_from,
        date_to=booking.date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    
@router.get("")
async def get_user_bookings(
    current_user: Users = Depends(get_current_user)
) -> list[SBookingWithDetails]:
    """Получить бронирования текущего пользователя"""
    bookings = await BookingDAO.find_all_by_user(current_user.id)
    
    return [
        SBookingWithDetails(
            id=booking.id,
            room_id=booking.room_id,
            user_id=booking.user_id,
            date_from=booking.date_from,
            date_to=booking.date_to,
            price=booking.price,
            total_cost=booking.total_cost,
            total_days=booking.total_days,
            room_name=booking.room_name,
            room_description=booking.room_description,
            room_services=booking.room_services,
            room_image_id=booking.room_image_id
        )
        for booking in bookings
    ]

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user)
):
    """Удалить бронирование пользователя"""
    # Проверяем, что бронирование принадлежит пользователю
    booking = await BookingDAO.find_one_or_none(id=booking_id, user_id=current_user.id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено или у вас нет прав на его удаление"
        )
    
    # Удаляем через BaseDAO.delete()
    success = await BookingDAO.delete(booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить бронирование"
        )
    
    return None