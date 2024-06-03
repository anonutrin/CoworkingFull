import re
from typing import Tuple

from admin_dashboard.master_locations.models import Location
from utils.logger import logger


async def select_location_by_id(location_id, **kwargs):
    """ Get location query by location id.
    Return None if error """
    try:
        return Location.objects.filter(id=location_id, **kwargs).first()
    except Exception as ex:
        logger.error(ex)
        return None


async def select_location(**kwargs):
    try:
        return Location.objects.filter(**kwargs).first()
    except Exception as ex:
        logger.error(ex)
        return False


async def add_location(
        title, description, short_description, price, work_schedule, latitude, longitude, full_address, contact_link,
        category, emodji
):
    """return [location.id, location.title]"""
    try:
        location, _ = Location.objects.get_or_create(
            title=title,
            description=description,
            short_description=short_description,
            price=price,
            work_schedule=work_schedule,
            latitude=latitude,
            longitude=longitude,
            full_address=full_address,
            contact_link=contact_link,
            category=category,
            emodji=emodji
        )
        return [location.id, location.title]
    except Exception as ex:
        logger.error(ex)
        return [None, None]


def extract_number_from_string(text: str) -> float:
    match = re.search(r'(\d[\d\s]*(\.\d+)?)', text)
    if match:
        number_str = match.group(1).replace(' ', '')
        return float(number_str)
    else:
        return 0.0


async def update_or_create_location(location_id, title, description, short_description,
                                    price, work_schedule, latitude, emodji,
                                    longitude, full_address, contact_link, category) -> Tuple[Location, bool]:
    location, created = Location.objects.update_or_create(
        id=location_id,
        defaults={
            'title': title,
            'description': description,
            'short_description': short_description,
            'price': price,
            'price_number': extract_number_from_string(price),
            'work_schedule': work_schedule,
            'latitude': latitude,
            'longitude': longitude,
            'contact_link': contact_link,
            'emodji': emodji,
            'category': category,
            'full_address': full_address
        }
    )
    location.category = category
    location.save()

    return location, created
