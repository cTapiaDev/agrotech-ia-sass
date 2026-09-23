import json
import logging
import httpx
import asyncio
from openai import OpenAI
from google import genai
from google.genai import types
from celery import shared_task
from pydantic import BaseModel, ValidationError
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from .models import FarmField, WeatherLog, Crop

logger = logging.getLogger(__name__)

class AgroAnalysisSchema(BaseModel):
    crop_name: str
    risk_level: str
    water_requirements: str
    ai_recommendation: str

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


@shared_task
def analyze_crop_with_ai(crop_id):
    logger.info(f"Iniciando análisis de IA para cultivo: {crop_id}")

    try:
        crop = Crop.objects.select_related('farm_field').get(pk=crop_id)

        prompt = f"""
        Analiza el siguiente cultivo y devuelve estrictamente un objecto JSON con esta estructura:
        {{"crop_name": "string", "risk_level": "Alto/Medio/Bajo", "water_requirements": "string", "ai_recommendation: "string"}}

        Datos:
        Cultivos: {crop.name} ({crop.get_crop_type_display()})
        Siembre: {crop.sowing_date}
        Ubicación: Lat {crop.farm_field.location_lat}, Lng {crop.farm_field.location_lng}
        """

        try: 
            logger.info('Análisis con GROQ...')

            groq_client = OpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1"
            )

            completion = groq_client.chat.completions.create(
                # model="llama-3.3-70b-versatile",
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "Eres un agronómo experto. Responde exclusivamente en formato JSON puro, sin bloques de código markdown, comillas triples ni texto adicional."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            raw_json = json.loads(completion.choices[0].message.content)

        except Exception as groq_exc:
            logger.warning(f"GROQ falló ({str(groq_exc)})... Activamos GEMINI...")

            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )

            raw_json = json.loads(response.text)

        validated_data = AgroAnalysisSchema(**raw_json)

        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'agronomy_notifications',
                {
                    'type': 'send_notification',
                    'message': validated_data.model_dump()
                }
            )

        except Exception as ws_err:
            logger.error(f"Falló del WS: {ws_err}")

    except ValidationError as e:
        logger.error(f"Error de validación JSON: {e}")
    except json.JSONDecodeError:
        logger.error('Gemini no devolvió un JSON válido.')
    except Exception as exc:
        logger.exception(f"Falló GROQ y GEMINI: {str(exc)}")

        error_playload = {
            'crop_name': crop.name if 'crop' in locals() else 'Desconocido',
            'risk_level': 'Alto',
            'water_requirements': 'N/A',
            'ai_recommendation': 'Servicios de IA temporalmente no disponibles.'
        }

        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'agronomy_notifications',
                {
                    'type': 'send_notification',
                    'message': error_playload
                }
            )
        except Exception as ws_fallback_err:
            logger.error(f"Fallo crítico: {ws_fallback_err}")