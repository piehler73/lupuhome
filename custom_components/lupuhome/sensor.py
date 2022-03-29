"""Lupusec sensor platform."""
import logging
from datetime import datetime, timedelta

# Import Lupulib Library
import lupulib
from lupulib.exceptions import LupusecException

# Import from HomeAssistant Core
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import PLATFORM_SCHEMA

# Import from HomeAssistant Helpers
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

# Import pre-defined constants from HA
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)

# Import specific constants from HA.Lupuhome
from custom_components.lupuhome.const import (
    DOMAIN,
    ATTR_SENSORS,
)


# Setup Logger
_LOGGER = logging.getLogger(__name__)

# Time between updating data from Lupusec
SCAN_INTERVAL = timedelta(seconds=10)


# TODO: change cv.string to cv.ip_address later
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)



async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType=None,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.debug("Lupuhome/sensor.py: async_setup_platform() called...")

    # Create asynchrinous session
    session = async_create_clientsession(hass)
    
    # Get config data from HA configuration.yaml
    user = config.get(CONF_USERNAME)
    pwd = config.get(CONF_PASSWORD)
    ip = config.get(CONF_IP_ADDRESS)  
    _LOGGER.debug("ConfigData: domain=%s, ip=%s, user=%s, pwd=%s" % (DOMAIN, ip, user, pwd))
    _LOGGER.debug("CustomConfigData: ATTR_SENSORS=%s" % (ATTR_SENSORS))

    # Contact Lupusec Alarm System and Login
    try:
        _LOGGER.debug("try to login to LupusecSystem...")
        hass.data[DOMAIN] = await LupusecSystem(user, pwd, ip)
        _LOGGER.debug("...login successful.")
    except LupusecException as ex:
        _LOGGER.error(ex)


class LupusecSystem:
    """Lupusec System class."""

    def __init__(self, user, pwd, ip):
        """Initialize the system."""
        _LOGGER.debug("Lupuhome/__init__.py: LupusecSystem.__init__ callled...")
        self.lupusec = lupulib.Lupusec(user, pwd, ip)



class LupusecDevice(Entity):
    """Representation of a Lupusec device."""

    def __init__(self, data, device):
        """Initialize a sensor for Lupusec device."""
        _LOGGER.debug("Lupuhome/__init__.py: LupusecDevice.__init__ callled...")
        self._data = data
        self._device = device

    def update(self):
        """Update automation state."""
        _LOGGER.debug("Lupuhome/__init__.py: LupusecDevice.update() callled...")
        self._device.refresh()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._device.name




