from datetime import date
from fastapi import APIRouter, Query, HTTPException
from app.hotels.repository import HotelDAO
from app.hotels.schemas import SHotelWithRooms

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{location}")
async def get_hotels_by_location(
    location: str,
    date_from: date = Query(..., description="Дата заезда"),
    date_to: date = Query(..., description="Дата выезда"),
) -> list[SHotelWithRooms]:
    """Получить отели по локации с свободными номерами"""
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return [
        SHotelWithRooms(
            id=hotel.id,
            name=hotel.name,
            location=hotel.location,
            services=hotel.services,
            rooms_quantity=hotel.total_quantity,
            image_id=hotel.image_id,
            rooms_left=hotel.rooms_left
        )
        for hotel in hotels
    ]

@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotelWithRooms:
    """Получить отель по ID"""
    hotel = await HotelDAO.find_by_id(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return hotel