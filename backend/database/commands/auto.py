from typing import Tuple

from admin_dashboard.master_locations.app_models import Auto


async def update_or_create_auto(
        number, model, brand, equipment,
        year_of_issue, class_type, color,
        body, drive_unit, fuel_type, transmission,
        power, volume_engine, fuel_volume,
        acceleration_to100, seats_number, city,
        rent_cost_per_day, rent_cost_per_month, description,
        links
) -> Tuple[Auto, bool]:
    auto, created = Auto.objects.update_or_create(
        id=number,
        defaults={
            'brand': brand,
            'model': model,
            'equipment': equipment,
            'year_of_issue': year_of_issue,
            'class_type': class_type,
            'color': color,
            'body': body,
            'drive_unit': drive_unit,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'power': power,
            'volume_engine': volume_engine,
            'fuel_volume': fuel_volume,
            'acceleration_to100': acceleration_to100,
            'seats_number': seats_number,
            'city': city,
            'rent_cost_per_day': rent_cost_per_day,
            'rent_cost_per_month': rent_cost_per_month,
            'description': description,
            'links': links
        }
    )
    auto.save()

    return auto, created
