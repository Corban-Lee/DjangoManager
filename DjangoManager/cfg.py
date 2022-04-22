import json
import logging


log = logging.getLogger(__name__)


class ConfigManager:
    
    data: dict = {}
    _default: dict = {
        
    }
    _filename: str = 'config.json'
    
    def __init__(self, root):
        self.dirs = root.dirs
        
    def restore_defaults(self) -> None:
        cfg_dir = self.dirs.user_config_dir
        log.info('restoring defaults to log file')
        self.data = self._default
        with open(f'{cfg_dir}\{self._filename}', 'x') as file:
            json.dump(self.data, file)
    
    def read(self) -> None:
        cfg_dir = self.dirs.user_config_dir
        try:
            with open(f'{cfg_dir}\{self._filename}', 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            log.error(f"couldn't find config file in {cfg_dir}")
            self.restore_defaults()
        except json.JSONDecodeError:
            log.error(f"config file in {cfg_dir} couldn't be read")
            self.restore_defaults()                                       
            
    
    def set(self):
        pass