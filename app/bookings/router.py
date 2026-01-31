from fastapi import APIRouter, Depends

from app.bookings.repository import BookingDAO
from app.users.models import Users
from app.users.dependencies import get_current_user
from datetime import date
from pydantic import BaseModel
from ..exceptions import RoomCannotBeBooked

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