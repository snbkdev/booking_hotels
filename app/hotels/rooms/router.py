from datetime import date
from fastapi import APIRouter, Query, HTTPException
from app.hotels.rooms.repository import RoomDAO
from app.hotels.rooms.schemas import SRoomWithAvailability

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])

@router.get("")
async def get_rooms_by_hotel(
    hotel_id: int,
    date_from: date = Query(..., description="Дата заезда"),
    date_to: date = Query(..., description="Дата выезда"),
) -> list[SRoomWithAvailability]:
    """Получить номера в отеле с информацией о доступности"""
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    if not rooms:
        raise HTTPException(status_code=404, detail="Номера не найдены или отель не существует")
    
    return [
        SRoomWithAvailability(
            id=room.id,
            hotel_id=room.hotel_id,
            name=room.name,
            description=room.description,
            price=room.price,
            services=room.services,
            quantity=room.quantity,
            image_id=room.image_id,
            rooms_left=room.rooms_left,
            total_cost=room.total_cost
        )
        for room in rooms
    ]