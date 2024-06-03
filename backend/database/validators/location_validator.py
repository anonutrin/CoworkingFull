from typing import Optional, Union

from pydantic import Field, BaseModel, field_validator


class LocationValidator(BaseModel):
    location_id: int
    title: str = Field(max_length=256, default='')
    description: str = Field(max_length=720, default='')
    short_description: str = Field(max_length=256, default='')
    price: str = Field(max_length=25, default='')
    contact_link: Optional[str] = Field(max_length=1024, default='')
    emodji: Optional[str] = Field(max_length=10)
    work_schedule: Optional[str] = Field(max_length=25)
    latitude: Optional[Union[float, str]] = None
    longitude: Optional[Union[float, str]] = None
    category: str = Field(max_length=10)
    full_address: Optional[str] = ''
    images_link: Optional[str] = ''

    @field_validator('contact_link')  # TODO url validation
    def validate_contact_link(cls, value):
        return value
