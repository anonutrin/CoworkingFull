import io
import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from admin_dashboard.master_locations.app_models import Location, Auto
from config.settings import settings
from database.commands.telegram_users import select_user
from handlers.admin.catalog import send_location_info
from utils.telegram import get_user_avatar

app = FastAPI()
protocol = 'http'
server_host = '212.193.50.28'
server_port = 8099

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
map_file_dir = os.path.join(current_dir, "static\\map.html")
menu_file_dir = os.path.join(current_dir, "static\\index.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


async def filter_locations(max_price: float = None, category: str = None):
    queryset = Location.objects.all()
    if category and category.lower() != 'все':
        queryset = queryset.filter(category__iexact=category.capitalize())

    if max_price is not None and max_price > 0:
        queryset = queryset.filter(price_number__lte=max_price)

    return queryset


@app.get("/show")
async def show_location(location_id: str, chat_id: int | None = None):
    print(chat_id, location_id)
    if chat_id and location_id:
        await send_location_info(chat_id, location_id)
    return {'success': True}


@app.get("/user-info")
async def get_user_info(chat_id: int = None):
    try:
        if chat_id is None:
            raise Exception()
        user = await select_user(chat_id)
        if user is None:
            coordinates = [55.76, 37.64]
        else:
            city = user.chose_location
            coordinates = settings.CITIES[city]

        return {
            'user_photo': await get_user_avatar(chat_id),
            'balance': 0,
            'latitude': coordinates[0],
            'longitude': coordinates[1]
        }

    except Exception as ex:
        return {
            'user_photo': None,
            'balance': None,
            'latitude': None,
            'longitude': None
        }


async def convert_short_location_model_to_list(locations):
    return [
        {
            'id': location.id,
            'title': location.title,
            'short_description': location.short_description,
            'price': location.price,
            'contact_link': location.contact_link,
            'work_schedule': location.work_schedule,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'category': location.category,
            'emodji': location.emodji,
            'imageUrl': f'{protocol}://{server_host}:{server_port}/image/{location.id}'
        }
        for location in locations
    ]


async def convert_full_location_model_to_list(locations):
    return [
        {
            'id': location.id,
            'title': location.title,
            'short_description': location.short_description,
            'price': location.price,
            'contact_link': location.contact_link,
            'work_schedule': location.work_schedule,
            'full_address': location.full_address,
            'category': location.category,
            'emodji': location.emodji,
            'imageUrl': f'{protocol}://{server_host}:{server_port}/image/{location.id}'
        }
        for location in locations
    ]


async def convert_auto_model_to_list(autos):
    return [
        {
            'id': auto.id,
            'brand': auto.brand,
            'model': auto.model,
            'equipment': auto.equipment,
            'year_of_issue': auto.year_of_issue,
            'class_type': auto.class_type,
            'color': auto.color,
            'body': auto.body,
            'drive_unit': auto.drive_unit,
            'fuel_type': auto.fuel_type,
            'transmission': auto.transmission,
            'power': auto.power,
            'volume_engine': auto.volume_engine,
            'fuel_volume': auto.fuel_volume,
            'acceleration_to100': auto.acceleration_to100,
            'seats_number': auto.seats_number,
            'city': auto.city,
            'rent_cost_per_day': auto.rent_cost_per_day,
            'rent_cost_per_month': auto.rent_cost_per_month,
            'description': auto.description,
            'links': auto.links.split(';'),
            'imageUrl': f'{protocol}://{server_host}:{server_port}/image/auto/{auto.id}'
        }
        for auto in autos
    ]


@app.get('/locations')
async def get_locations(
        category: Optional[str] = None,
        max_price: Optional[float] = None,
):

    return await convert_short_location_model_to_list(await filter_locations(max_price, category))


# @app.get('/chunkLocations')
# async def get_locations(
#         page: Optional[int] = Query(1, ge=1),
# ):
#     items_per_page = 14
#     offset = (page - 1) * items_per_page
#
#     try:
#         total_count = Location.objects.count()
#         locations = Location.objects.all()[offset:offset + items_per_page]
#         locations = await convert_full_location_model_to_list(locations)
#         return {"items_per_page": items_per_page, "total_count": total_count, "locations": locations}
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.get('/chunkLocations')
async def get_locations(
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        page: Optional[int] = Query(1, ge=0),
):
    if page == 0:
        page = 1

    items_per_page = 14
    offset = (page - 1) * items_per_page

    try:
        queryset = await filter_locations(max_price, category)

        total_count = queryset.count()

        locations = queryset[offset:offset + items_per_page]
        locations = await convert_full_location_model_to_list(locations)

        return {
            "items_per_page": items_per_page,
            "total_count": total_count,
            "locations": locations
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/chunkAutos')
async def get_autos(
        page: Optional[int] = Query(1, ge=1),
):
    items_per_page = 14
    offset = (page - 1) * items_per_page

    try:
        total_count = Auto.objects.count()
        autos = Auto.objects.all()[offset:offset + items_per_page]
        autos = await convert_auto_model_to_list(autos)
        return {"items_per_page": items_per_page, "total_count": total_count, "autos": autos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_image_bytes(image_folder):
    try:
        files = os.listdir(image_folder)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Not found')

    image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg'))]

    if not image_files:
        raise HTTPException(status_code=404, detail='Image file not found')

    image_path = os.path.join(image_folder, image_files[0])
    try:
        image_data = open(image_path, 'rb').read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail='Error reading image file')

    return StreamingResponse(io.BytesIO(image_data), media_type='image/jpeg')


@app.get('/image/{id}')
async def get_image(id: int):
    image_folder = f'storage/images/location_{id}'
    print(image_folder)
    try:
        return await get_image_bytes(image_folder)
    except Exception as ex:
        raise
        # raise


@app.get('/image/auto/{id}')
async def get_auto_image(id: int):
    image_folder = f'storage/images/auto/auto_{id}'
    print(image_folder)
    try:
        return await get_image_bytes(image_folder)
    except:
        raise


async def run_api_server(host="127.0.0.1", port=5001, debug: bool = False):
    global server_host, server_port
    server_host = host if not debug else "127.0.0.1"
    server_port = port

    if not debug:
        config = uvicorn.Config(app, host=server_host, port=server_port, loop="asyncio", ssl_keyfile="/etc/letsencrypt/live/allrenda.ru/privkey.pem",
                                ssl_certfile="/etc/letsencrypt/live/allrenda.ru/fullchain.pem")
    else:
        config = uvicorn.Config(app, host=server_host, port=port, loop="asyncio")

    server = uvicorn.Server(config)
    await server.serve()
