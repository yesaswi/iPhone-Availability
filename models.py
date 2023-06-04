from pydantic import BaseModel

class CityInfo(BaseModel):
    city: str
    state: str
