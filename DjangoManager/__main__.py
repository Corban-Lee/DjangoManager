import tkinter
import logging
from pathlib import Path
from appdirs import AppDirs

import logs
from tabs import TabManager
from cfg import ConfigManager
from menu import MenuManager
from style import StyleManager


log = logging.getLogger(__name__)

__version__ = '0.0.0'
__author__ = 'Corban-Lee'


class Root:
    
    name = 'DjangoManager'  # name shouldn't contain spaces or special characters
    window = tkinter.Tk()
    dirs = AppDirs(name, __author__, __version__)
    logs.setup(name, __version__, dirs)

    def __init__(self):
        
        self._validate_dirs()
        
        # setup window
        self.window.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.window.minsize(700, 400)
        self.window.title(self.name)
        
        # Get & setup managers
        self.style = StyleManager(self)  # must be called first
        self.cfg = ConfigManager(self)
        self.tabs = TabManager(self)
        self.menu = MenuManager(self)
    
    def run(self) -> None:
        log.info('starting window main loop')
        self.window.mainloop()
        
    def on_exit(self) -> SystemExit:
        log.info('exiting app')
        self.window.destroy()
        raise SystemExit
    
    def _validate_dirs(self) -> None:
        """Creates app directories if they don't already exist."""
        log.info('validating app dirs')
        Path(self.dirs.user_cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.dirs.user_config_dir).mkdir(parents=True, exist_ok=True)
        Path(self.dirs.user_log_dir).mkdir(parents=True, exist_ok=True)
        
        
if __name__ == '__main__':
    Root().run()
    