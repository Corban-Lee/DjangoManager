import os
import json
import logging

from utils import get_json, write_json
from constants import CONFIG_FILENAME


log = logging.getLogger(__name__)


class ConfigManager:
    """Manages project settings"""
    data: dict = {}
    _default: dict = {
        'tabs': {
            'trough_height': 25,
            'last_tab': ''
        },
        'projects': {}
    }
    
    def __init__(self, root):
        self.dir = root.dirs.user_config_dir + '/' + CONFIG_FILENAME
        self.read()
        
    def restore_defaults(self) -> None:
        """Restore default values to config file"""
        log.info('restoring defaults to log file')
        self.data = self._default
        filemode = 'w' if os.path.exists(self.dir) else 'x'
        self.write(filemode)
    
    def read(self) -> None:
        """Read data from the config file and save it as a dictionary: 'self.data'"""
        try:
            self.data = get_json(self.dir)
        except FileNotFoundError:
            log.error(f"couldn't find config file in {self.dir}")
            self.restore_defaults()
        except json.JSONDecodeError:
            log.error(f"config file in {self.dir} couldn't be read")
            self.restore_defaults()                                             
        
    def write(self, mode:str='w'):
        """Writes the current config to the config file'"""
        write_json(self.dir, self.data)
