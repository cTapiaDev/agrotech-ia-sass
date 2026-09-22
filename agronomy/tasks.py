import logging
import httpx
import asyncio
from celery import shared_task
from .models import FarmField, WeatherLog

logger = logging.getLogger(__name__)

async def fetch_weather_data(lat, lng):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5.0)
        response.raise_for_status()
        return response.json()

@shared_task
def sync_field_weather(field_id):
    logger.info(f"Iniciando sincronización de clima para el campo: {field_id}")

    try:
        field = FarmField.objects.get(pk=field_id)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(fetch_weather_data(field.location_lat, field.location_lng))

        current_weather = data.get('current_weather', {})

        WeatherLog.objects.create(
            farm_field=field,
            temperature=current_weather.get('temperature', 0.0),
            wind_speed=current_weather.get('windspeed', 0.0),
            is_successful=True
        )
        logger.info(f"Clima sincronizado con éxito para {field.name}")

    except httpx.TimeoutException:
        error_msg = "Timeout: La API tardó demasiado en responder."
        logger.error(error_msg)
        WeatherLog.object.create(
            farm_field_id=field_id,
            temperature=0,
            wind_speed=0,
            is_successful=False,
            error_message=error_msg
        )

    except httpx.RequestError as exc:
        error_msg = f"Error al consultar la API: {str(exc)}"
        logger.error(error_msg)
        WeatherLog.object.create(
            farm_field_id=field_id,
            temperature=0,
            wind_speed=0,
            is_successful=False,
            error_message=error_msg
        )

    except FarmField.DoesNotExist:
        logger.error(f"El campo con ID {field_id} no existe en la base de datos.")

    except Exception as exc:
        logger.exception(f"Error inesperado en sync_field_weather: {str(exc)}")