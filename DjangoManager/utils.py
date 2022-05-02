import os
import json
import logging
import tkinter
from tkinter import ttk

from constants import CONFIG_FILENAME


log = logging.getLogger(__name__)


def get_all_children(widget:tkinter.Widget|tkinter.Tk) -> list[tkinter.Widget]:
    """Returns a list of every widget below the entered widget"""
    children = widget.winfo_children()
    for child in children:
        children.extend(child.winfo_children())
    return children


def text_length_check(text:str, length:int):
    """Replaces long strings with a shortened copy ending in '...'"""
    if len(text) > length:
        return text[:length - 3] + '...'
    return text


class ConfigManager:
    data: dict = {}
    _default: dict = {
        'tabs': {
            'trough_height': 25
        }
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
            with open(self.dir, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            log.error(f"couldn't find config file in {self.dir}")
            self.restore_defaults()
        except json.JSONDecodeError:
            log.error(f"config file in {self.dir} couldn't be read")
            self.restore_defaults()                                             
        
    def write(self, mode:str='w'):
        """Writes the current config to the config file'"""
        with open(self.dir, mode, encoding='utf-8') as file:
            json.dump(self.data, file)
        
