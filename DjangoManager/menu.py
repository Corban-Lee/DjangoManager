import tkinter
import logging


log = logging.getLogger(__name__)


class MenuManager:
    
    def __init__(self, root):
        log.info('creating menu bar for app window')
        
        self.menu = tkinter.Menu(root.window)
        
        # filemenu
        filemenu = tkinter.Menu(self.menu, tearoff=False)
        filemenu.add_command(label='New Project', command=None)
        filemenu.add_command(label='Open Project', command=None)
        filemenu.add_separator()
        filemenu.add_command(label='Save Project', command=None)
        filemenu.add_separator()
        filemenu.add_command(label='Close Project', command=None)
        self.menu.add_cascade(menu=filemenu, label='File')
        
        # editmenu
        editmenu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(menu=editmenu, label='Edit')
        
        # viewmenu
        viewmenu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(menu=viewmenu, label='View')
        
        root.window.config(menu=self.menu)
