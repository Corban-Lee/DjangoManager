import tkinter
import logging


log = logging.getLogger(__name__)


class MenuManager(tkinter.Menu):
    
    def __init__(self, root):
        super().__init__(root.window)
        log.info('initialising menubar manager')

        # filemenu
        filemenu = tkinter.Menu(self, tearoff=False)
        self.add_cascade(menu=filemenu, label='File')
        
        filemenu.add_command(label='New Project', command=None)
        filemenu.add_command(label='Open Project', command=None)
        filemenu.add_separator()
        filemenu.add_command(label='Save Project', command=None)
        filemenu.add_separator()
        filemenu.add_command(label='Close Project', command=None)
        
        # editmenu
        editmenu = tkinter.Menu(self, tearoff=False)
        self.add_cascade(menu=editmenu, label='Edit')
        
        # viewmenu
        viewmenu = tkinter.Menu(self, tearoff=False)
        self.add_cascade(menu=viewmenu, label='View')
        
        # debugmenu
        debugmenu = tkinter.Menu(self, tearoff=False)
        self.add_cascade(menu=debugmenu, label='Debug')
        
        debugmenu.add_command(label='Add Empty Tab', command=lambda:root.tabs.add_tab(f'Tab Number {len(root.tabs.tabs)}'))
        
        root.window.config(menu=self)
