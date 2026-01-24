from fastapi import APIRouter

from app.bookings.repository import BookingDAO
from app.bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("", response_model=list[SBooking])
async def get_bookings():
    bookings = await BookingDAO.find_all()
    
    result = []
    for booking in bookings:
        if hasattr(booking, "Bookings"):
            result.append(SBooking.model_validate(booking.Bookings))
        elif isinstance(booking, dict) and "Bookings" in booking:
            result.append(SBooking.model_validate(booking["Bookings"]))
        elif hasattr(booking, "__dict__"):
            data = {k: v for k, v in booking.__dict__.items() if not k.startswith('_')}
            result.append(SBooking.model_validate(data))
        else:
            result.append(SBooking.model_validate(booking))
    
    return result