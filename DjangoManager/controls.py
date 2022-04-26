import logging
import tkinter
from tkinter import ttk


log = logging.getLogger(__name__)


class ControlFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root.paned_window, style='Control.TFrame')
        return
        
        paned_window = tkinter.PanedWindow(self, orient='horizontal', **root.style.paned_window)
        paned_window.pack(fill='both', expand=True)
        
        console_pane = ttk.Frame(paned_window)
        console_pane.pack(side='left', fill='both')
        paned_window.add(console_pane, minsize=100, stretch='always')

        manage_pane = ttk.Frame(paned_window)
        manage_pane.pack(side='left', fill='both', expand=True)
        paned_window.add(manage_pane, minsize=100, stretch='always')
        
        left_sep = ttk.Frame(manage_pane, style='TabSeparator.TFrame', width=1)
        left_sep.pack(side='left', fill='y')
        
        right_sep = ttk.Frame(manage_pane, style='TabSeparator.TFrame', width=1)
        right_sep.pack(side='right', fill='y')
        
        admin_pane = ttk.Frame(paned_window)
        admin_pane.pack(side='left', fill='both', expand=True)
        paned_window.add(admin_pane, minsize=100, stretch='always')

