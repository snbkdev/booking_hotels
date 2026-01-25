from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)

class HotelsSearchArgs:
    def __init__(
        self,
        location: str, 
        date_from: date, 
        date_to: date, 
        stars: Optional[int] = Query(None, ge=1, le=5), 
        has_spa: Optional[bool] = None
        ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa

class SHotel(BaseModel):
    address: str
    name: str
    stars: int

@app.get("/")
def get_hotels(location: str, 
               date_from: date, 
               date_to: date, 
               stars: Optional[int] = Query(None, ge=1, le=5), 
               has_spa: Optional[bool] = None) -> list[SHotel]:
    hotels = [
        {
            "address": "ул. Советскаяб 37, Бишкек",
            "name": "Hayyat",
            "stars": 4,
        },
    ]
    return hotels

@app.get("/hotels")
def search_hotels(search_args: HotelsSearchArgs = Depends()):
    return search_args

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

@app.post("/bookings")
def add_booking(booking: SBooking):
    pass