from pydantic import BaseModel


class PosterRequest(BaseModel):
    bike_model: str
    bike_color: str
    background: str
    platform: str
    language: str
    dealer_name: str