from celery import shared_task
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import requests
from django.conf import settings
from .models import FurtoEquipamento
import logging

retry_strategy = Retry(total=3, status_forcelist=[429, 500, 502], backoff_factor=0.7)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.session()
session.mount('https://', adapter)

logger = logging.getLogger(__name__)


BASE_PATH = 'https://us1.locationiq.com/v1/search/structured'
TOKEN = settings.LOCATIONIQ_TOKEN

def geocode_address(address_dict):
    params = address_dict.copy()
    params['format'] = 'json'
    params['key'] = TOKEN

    try:
        response = session.get(BASE_PATH, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0].get('lat'), data[0].get('lon')
    except requests.RequestException as e:
        logger.error(f'API request failed: {e}')
    except (ValueError, IndexError) as e:
        logging.error(f"Failed to parse API response: {e}")

    return None, None


@shared_task(rate_limit='85/m')
def geocode_furto_equipamento(instance_id):
    try:
        instance = FurtoEquipamento.objects.get(pk=instance_id)
    except FurtoEquipamento.DoesNotExist:
        logger.warning(f'Furto de Equipamento with id={instance_id} does not exist.')
        return

    if instance.status != FurtoEquipamento.Status.AGUARDANDO_GEO.value:
        logger.info(f'Geocoding for FurtoEquipamento id={instance_id} already processed. Skipping')
        return

    logger.info(f"Starting geocoding for FurtoEquipamento ID: {instance_id}")

    address_to_geocode = {
        'street': f'{instance.numero},'
                  f' {instance.logradouro}',
        'city': instance.cidade,
        'state': instance.uf,
        'countrycodes': 'br'
    }

    lat, long = geocode_address(address_to_geocode)

    if lat and long:
        instance.latitude = lat
        instance.longitude = long
        instance.status = FurtoEquipamento.Status.AGUARDANDO_VERIFICACAO
        instance.save(update_fields=['latitude', 'longitude', 'status'])
        logger.info(f"Successfully geocoded FurtoEquipamento ID: {instance_id}")
    else:
        instance.status = FurtoEquipamento.Status.GEO_FALHOU
        instance.save(update_fields='status')
        logger.warning(f"Geocoding failed for Location ID: {instance_id}.")
