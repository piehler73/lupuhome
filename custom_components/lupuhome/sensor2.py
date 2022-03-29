"""Lupusec Custom Component"""

import logging
from homeassistant import core

# Import lupulib - the actual library for interacting with a lupusec alarm system
import lupulib
import lupulib.constants as CONST
import voluptuous as vol

from homeassistant.components import persistent_notification
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)


DOMAIN = "lupuhome"

NOTIFICATION_ID = "lupusec_notification"
NOTIFICATION_TITLE = "Lupusec Security Setup"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_IP_ADDRESS): cv.string,
                vol.Optional(CONF_NAME): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

LUPUSEC_PLATFORMS = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]



async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Lupusec HomeAssistant Addon component."""
    
    _LOGGER.debug("Lupuhome/__init__.py: async_setup() callled...")

    # Get config data from HA configuration.yaml
    conf = config[DOMAIN]
    username = conf[CONF_USERNAME]
    password = conf[CONF_PASSWORD]
    ip_address = conf[CONF_IP_ADDRESS]
    name = conf.get(CONF_NAME)

    # Contact Lupusec Alarm System and Login
    try:
        _LOGGER.debug("try to login to LupusedSystem...")
        hass.data[DOMAIN] = LupusecSystem(username, password, ip_address, name)
    except LupusecException as ex:
        _LOGGER.error(ex)

        persistent_notification.create(
            hass,
            f"Error: {ex}<br />You will need to restart hass after fixing.",
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID,
        )
        return False

    # Load sensors from Lupusec Platform
    for platform in LUPUSEC_PLATFORMS:
        discovery.load_platform(hass, platform, DOMAIN, {}, config)

    return True


class LupusecSystem:
    """Lupusec System class."""

    def __init__(self, username, password, ip_address, name):
        """Initialize the system."""
        _LOGGER.debug("Lupuhome/__init__.py: LupusecSystem.__init__ callled...")
        self.lupusec = lupulib.Lupusec(username, password, ip_address)
        self.name = name


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




