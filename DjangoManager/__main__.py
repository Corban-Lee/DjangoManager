import tkinter
import logging
from time import sleep
from pathlib import Path
from appdirs import AppDirs
from PIL import Image, ImageTk

import logs
from tabs import TabManager
from utils import ConfigManager, Titlebar
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
        self.window.configure(bg='gray20')
        self.window.iconphoto(False, ImageTk.PhotoImage(Image.open(IMAGES_DIR+'/icon.png')))
        self._setup_titlebar()
        
        # this paned window exists to allow the tab trough to be expanded vertically
        self.paned_window = tkinter.PanedWindow(
            self.window, orient='vertical', sashwidth=1, bd=0,
            background='#a3a2a2'
        )
        self.paned_window.pack(side='top', fill='both', expand=True, padx=1, pady=(0, 1))

        # Get & setup managers
        self.cfg = ConfigManager(self)
        self.style = StyleManager(self)
        self.tabs = TabManager(self)
        # self.menu = MenuManager(self)
        log.info('Initialized all managers')
        
        self.control_frame = ControlFrame(self)
        self.control_frame.pack(side='bottom', fill='both', expand=True)
        
        self.paned_window.add(self.tabs, minsize=25)
        self.paned_window.add(self.control_frame, minsize=20)
        
        self.style.switch_theme('light')

    def run(self) -> None:
        """Start the app"""
        log.info('starting window main loop')
        self.window.mainloop()
        
    def on_exit(self) -> SystemExit:
        """Properly exits the app"""
        log.info('exiting app')
        sleep(.2)  # delay makes the close feel realistic
        self.window.destroy()
        raise SystemExit
    
    def _validate_dirs(self) -> None:
        """Creates app directories if they don't already exist."""
        log.info('validating app dirs')
        Path(self.dirs.user_cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.dirs.user_config_dir).mkdir(parents=True, exist_ok=True)
        Path(self.dirs.user_log_dir).mkdir(parents=True, exist_ok=True)
        
    def _setup_titlebar(self) -> None:
        """Create and configure the custom titlebar"""
        self.window.overrideredirect(True)
        self.titlebar = Titlebar(self)
        


if __name__ == '__main__':
    Root().run()
    