from fastapi import APIRouter

from app.bookings.repository import BookingDAO

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def home():
    return await BookingDAO.find_all()