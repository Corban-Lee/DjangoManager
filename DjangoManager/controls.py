import logging
import tkinter
from tkinter import ttk


log = logging.getLogger(__name__)


class ControlFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root.paned_window, style='Control.TFrame')

        wrapper = ttk.Frame(self)
        wrapper.place(x=0, rely=.5, relw=1, relh=.75, anchor='w')
        
        paned_window = tkinter.PanedWindow(wrapper, orient='horizontal', background='#D9D9D9', sashwidth=5)
        paned_window.pack(fill='both', expand=True)
        
        
        details_pane = ttk.Frame(paned_window)
        details_pane.pack(side='left', fill='both')
        paned_window.add(details_pane, minsize=100, stretch='always')

        details_header = ttk.Label(details_pane, text='Project Details', style='Header.TLabel')
        details_header.pack(side='top', anchor='w')
 
        
        manage_pane = ttk.Frame(paned_window)
        manage_pane.pack(side='left', fill='both', expand=True)
        paned_window.add(manage_pane, minsize=100, stretch='always')

        manage_header = ttk.Label(manage_pane, text='Management', style='Header.TLabel')
        manage_header.pack(side='top', anchor='w')
        
        left_sep = ttk.Frame(manage_pane, style='TabSeparator.TFrame', width=1)
        left_sep.place(x=0, rely=.5, relh=1, anchor='w')
        
        right_sep = ttk.Frame(manage_pane, style='TabSeparator.TFrame', width=1)
        right_sep.place(relx=1, rely=.5, relh=1, anchor='e')
        

        admin_pane = ttk.Frame(paned_window)
        admin_pane.pack(side='left', fill='both', expand=True)
        paned_window.add(admin_pane, minsize=100, stretch='always')

        admin_header = ttk.Label(admin_pane, text='Administration', style='Header.TLabel')
        admin_header.pack(side='top', anchor='w')

