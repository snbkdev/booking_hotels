from pydantic import BaseModel, ConfigDict
from typing import Optional

class SHotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    location: str
    services: Optional[dict] = None
    rooms_quantity: int
    image_id: int

class SHotelWithRooms(SHotel):
    rooms_left: int