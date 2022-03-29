"""Lupusec sensor platform."""
import logging
from datetime import timedelta

# Import from HomeAssistant
from homeassistant.components.binary_sensor import DEVICE_CLASSES, BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

# Import constants from HA
from homeassistant.const import (
    ATTR_NAME,
    CONF_ACCESS_TOKEN,
    CONF_NAME,
    CONF_PATH,
    CONF_URL,
)

# Import Lupulib Library
import lupulib


# Import constants from lupuhome
from .const import (
    ATTR_SENSORS,
)


# Setup Logger
_LOGGER = logging.getLogger(__name__)

# Time between updating data from Lupusec
SCAN_INTERVAL = timedelta(seconds=10)



async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    session = async_get_clientsession(hass)
    github = GitHubAPI(session, "requester", oauth_token=config[CONF_ACCESS_TOKEN])
    sensors = [GitHubRepoSensor(github, repo) for repo in config[CONF_REPOS]]
    async_add_entities(sensors, update_before_add=True)


