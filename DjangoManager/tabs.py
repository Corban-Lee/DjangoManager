import tkinter
import logging


log = logging.getLogger(__name__)


class TabManager:
    
    def __init__(self, root):
        self.window = root.window