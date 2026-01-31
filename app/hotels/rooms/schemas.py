from pydantic import BaseModel, ConfigDict
from typing import Optional

class SRoom(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    price: Optional[int] = None
    services: Optional[dict] = None
    quantity: Optional[int] = None
    image_id: int

class SRoomWithAvailability(SRoom):
    rooms_left: int
    total_cost: int