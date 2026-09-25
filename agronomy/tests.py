import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock, AsyncMock
from .models import FarmField, Crop
from .tasks import analyze_crop_with_ai

class AgronomyTasksTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')

        self.field = FarmField.objects.create(
            owner=self.user,
            name="Parcela",
            location_lat=-35.4264,
            location_lng=-71.6554,
            total_area_hectares=15.5
        )

        self.crop = Crop.objects.create(
            farm_field=self.field,
            name="Trigo",
            crop_type="TRIGO",
            sowing_date="2026-05-15"
        )

    @patch('agronomy.tasks.fetch_weather_data', new_callable=AsyncMock)
    def test_sync_field_weather_success(self, mock_fetch):
        mock_fetch.return_value = {
            'current_weather': {
                'temperature': 14.5,
                'windspeed': 12.0
            }
        }

        from .tasks import sync_field_weather
        sync_field_weather(self.field.id)
        self.field.refresh_from_db()

        mock_fetch.assert_called_once_with(self.field.location_lat, self.field.location_lng)

    @patch('agronomy.tasks.get_channel_layer')
    @patch('agronomy.tasks.Groq')
    def test_analyze_crop_with_ai_success(self, mock_openai, mock_channel_layer):
        mock_openai_instance = MagicMock()
        mock_openai.return_value = mock_openai_instance

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = json.dumps({
            "crop_name": "Trigo", 
            "risk_level": "Bajo", 
            "water_requirements": "Riego moderado", 
            "ai_recommendation": "Condiciones óptimas simuladas"
        })
        mock_openai_instance.chat.completions.create.return_value = mock_completion

        mock_channel_layer_instance = MagicMock()
        mock_channel_layer_instance.group_send = AsyncMock()
        mock_channel_layer.return_value = mock_channel_layer_instance

        analyze_crop_with_ai(self.crop.id)

        mock_openai_instance.chat.completions.create.assert_called_once()
        mock_channel_layer_instance.group_send.assert_called_once()

        call_args = mock_channel_layer_instance.group_send.call_args[0]
        self.assertEqual(call_args[0], 'agronomy_notifications')

        sent_payload = call_args[1]['message']
        self.assertEqual(sent_payload['risk_level'], 'Bajo')
        self.assertEqual(sent_payload['ai_recommendation'], 'Condiciones óptimas simuladas')

