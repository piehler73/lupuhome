"""Lupusec Custom Component"""

# Import standard python libraries
import logging
import voluptuous as vol

# Import lupulib - the actual library for interacting with a lupusec alarm system
import lupulib
import lupulib.constants as CONST


# Import specific constants from HA.Lupuhome
from custom_components.lupuhome.const import (
    DOMAIN,
    ATTR_SENSORS,
)


# Import from Home Assistant
from homeassistant import core
from homeassistant.components import persistent_notification
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_PASSWORD,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.sensor import PLATFORM_SCHEMA


_LOGGER = logging.getLogger(__name__)

DOMAIN = "lupuhome"

NOTIFICATION_ID = "lupusec_notification"
NOTIFICATION_TITLE = "Lupusec Security Setup"

# TODO: change cv.string to cv.ip_address later
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

LUPUSEC_PLATFORMS = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


async def async_setup(hass: core.HomeAssistant, config: ConfigType) -> bool:
    """Set up the Lupusec HomeAssistant Addon component."""
    
    _LOGGER.debug("Lupuhome/__init__.py: async_setup() callled...")

    # Get config data from HA configuration.yaml
    _LOGGER.debug("DOMAIN=%s", DOMAIN)  
    _LOGGER.debug("CONF_IP_ADDRESS=%s", CONF_IP_ADDRESS) 
    _LOGGER.debug("CONF_USERNAME=%s", CONF_USERNAME)     
    _LOGGER.debug("CONF_PASSWORD=%s", CONF_PASSWORD) 
    _LOGGER.debug("LEN(config)=%s", len(config)) 
    for key, value in config.items():        
        print(key, ' : ', value)

    if (config != None):
        _LOGGER.debug("config is not null")  
        if (CONF_IP_ADDRESS in config):       
            #ip_address = config.get(CONF_IP_ADDRESS)
            ip_address = config.get(DOMAIN).get(CONF_IP_ADDRESS)            
        else:
            _LOGGER.error("ERROR (lupuhome): no IP-Address provided in configuration.yaml")              
        if (CONF_USERNAME in config):               
            #username = config.get(CONF_USERNAME)
            username = config.get(DOMAIN).get(CONF_USERNAME)             
        else: 
            _LOGGER.error("ERROR (lupuhome): no Username provided in configuration.yaml") 
        if (CONF_PASSWORD in config):                   
            #password = config.get(CONF_PASSWORD)
            password = config.get(DOMAIN).get(CONF_PASSWORD) 
        else:
            _LOGGER.error("ERROR (lupuhome): no Password provided in configuration.yaml") 


        # Contact Lupusec Alarm System and Login
        try:
            _LOGGER.debug("try to login to LupusecSystem...")
            _LOGGER.debug("LupusecSystem: ip-address=%s, username=%s, pwd=%s", 
                ip_address,username, password)
            hass.data[DOMAIN] = LupusecSystem(username, password, ip_address)
        except:
            _LOGGER.error("ERROR: Login to LupusecSystem not succesful.")

            persistent_notification.create(
                hass,
                f"Error: <br />You will need to restart hass after fixing.",
                title=NOTIFICATION_TITLE,
                notification_id=NOTIFICATION_ID,
            )
            return False

        # Load sensors from Lupusec Platform
        _LOGGER.debug("Login to LupusecSystem: successful")                
        _LOGGER.debug("Setup platforms...")            
        for platform in LUPUSEC_PLATFORMS:
            discovery.load_platform(hass, platform, DOMAIN, {}, config)

        return True

    else:
        _LOGGER.error("ERROR (lupuhome): configuration is missing.")
        return False   


class LupusecSystem:
    """Lupusec System class."""

    def __init__(self, username, password, ip_address, DOMAIN):
        """Initialize the system."""
        _LOGGER.debug("Lupuhome/__init__.py: LupusecSystem.__init__ callled...")
        self.lupusec = lupulib.Lupusec(username, password, ip_address)
        self.name = DOMAIN


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




