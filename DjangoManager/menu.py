import logging
import tkinter
from tkinter import simpledialog
from typing import Any


log = logging.getLogger(__name__)


class MenuManager(tkinter.Menu):
    
    def __init__(self, root):
        super().__init__(root.window)
        self.root = root
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
        
        debugmenu.add_command(label='Add Tab', command=self.debug_add_tab)
        debugmenu.add_command(label='Add Tab With Text', command=self.debug_add_tab_with_text)
        
        root.window.config(menu=self)

    def debug_add_tab(self, title:str|None=None):
        title = f'Tab Number {len(self.root.tabs.tabs)}' if title is None else title
        self.root.tabs.add_tab(title)

    def debug_add_tab_with_text(self):
        title = simpledialog.askstring('Tab Name', 'Provide a name for this new tab:')
        self.debug_add_tab(title)
