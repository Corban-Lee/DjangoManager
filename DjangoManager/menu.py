import tkinter
import logging


log = logging.getLogger(__name__)


class MenuManager:
    
    def __init__(self, root):
        log.info('creating menu bar')
        self.menu = tkinter.Menu(root.window, bg='black')
        
        # filemenu
        filemenu = tkinter.Menu(self.menu, tearoff=False)
        filemenu.add_command(label='Open', command=None)
        self.menu.add_cascade(menu=filemenu, label='File')
        
        root.window.config(menu=self.menu)
