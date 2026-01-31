from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

class SBooking(BaseModel):
    id: Optional[Union[int, str]] = None
    room_id: Optional[Union[int, str]] = None
    user_id: Optional[Union[int, str]] = None
    
    date_from: Optional[Union[date, datetime, str]] = None
    date_to: Optional[Union[date, datetime, str]] = None
    
    price: Optional[Union[int, float, Decimal]] = None
    total_cost: Optional[Union[int, float, Decimal]] = None
    total_days: Optional[Union[int, float]] = None

    model_config = ConfigDict(from_attributes=True)

class SBookingWithDetails(SBooking):
    room_name: Optional[Union[int, str]] = None
    room_description: Optional[str] = None
    room_services: Optional[dict] = None
    room_image_id: Optional[Union[int, str]] = None