"""Lupusec Custom Component"""

import logging

from homeassistant import config_entries, core
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: core.HomeAssistant, config: ConfigType) -> bool:
    """Set up the GitHub Custom component from yaml configuration."""
    _LOGGER.debug("Lupuhome/__init__.py: async_setup() called...")
    _LOGGER.debug("DOMAIN=%s" % (DOMAIN))
    hass.data.setdefault(DOMAIN, {})

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True