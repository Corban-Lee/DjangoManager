import tkinter
import logging
from pathlib import Path
from appdirs import AppDirs
from PIL import Image, ImageTk

import logs
from tabs import TabManager
from utils import ConfigManager
from menu import MenuManager
from style import StyleManager
from controls import ControlFrame
from msgbox import MessageBox
from constants import IMAGES_DIR


log = logging.getLogger(__name__)

__version__ = '0.0.0'
__author__ = 'Corban-Lee'


class Root:
    name = 'Django Manager'
    safe_name = 'DjangoManager'
    window = tkinter.Tk()
    dirs = AppDirs(safe_name, __author__, __version__)

    def __init__(self):
        self._validate_dirs()
        logs.setup(self.name, __version__, self.dirs)
        
        # setup window
        self.window.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.window.minsize(700, 400)
        self.window.title(self.name)
        self.window.iconphoto(False, ImageTk.PhotoImage(Image.open(IMAGES_DIR+'/icon.png')))
        
        self.paned_window = tkinter.PanedWindow(
            self.window, orient='vertical', sashwidth=1, bd=0,
            background='#a3a2a2'
        )
        self.paned_window.pack(side='top', fill='both', expand=True)

        # Get & setup managers
        self.cfg = ConfigManager(self)
        self.style = StyleManager(self)  # must be called first
        self.tabs = TabManager(self)
        self.menu = MenuManager(self)
        
        self.control_frame = ControlFrame(self)
        self.control_frame.pack(side='bottom', fill='both', expand=True)
        
        self.paned_window.add(self.tabs, minsize=25)
        self.paned_window.add(self.control_frame, minsize=20)

    def run(self) -> None:
        """Start the app"""
        log.info('starting window main loop')
        self.window.mainloop()
        
    def on_exit(self) -> SystemExit:
        """Properly exits the app"""
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
    