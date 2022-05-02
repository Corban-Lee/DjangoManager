import logging
import tkinter
from tkinter import ttk


log = logging.getLogger(__name__)


class ControlFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root.paned_window, style='Control.TFrame')
        
        paned_window = tkinter.PanedWindow(self, orient='horizontal', background='#a3a2a2', sashwidth=1, bd=0)
        paned_window.pack(fill='both', expand=True)
        
        project_pane = ttk.Frame(paned_window)
        project_pane.columnconfigure(index=0, weight=1)
        paned_window.add(project_pane, minsize=200)
        paned_window.add(ttk.Frame(paned_window), minsize=300)
        
        self.project_header = tkinter.StringVar(value='Project Title Here')
        self.project_path = tkinter.StringVar(value='C:/path/to/project')
        self.environment_path = tkinter.StringVar(value='C:/path/to/environment')
        
        # project header
        ttk.Label(project_pane, textvariable=self.project_header, style='Header.TLabel'
        ).grid(column=0, row=0, sticky='we', padx=15, pady=15)
        
        # project header (control)
        ttk.Label(project_pane, text='Project Title'
        ).grid(column=0, row=1, sticky='w', padx=15, pady=(0, 3))
        ttk.Entry(project_pane, textvariable=self.project_header
        ).grid(column=0, row=2, sticky='we', padx=15, pady=(0, 15))
       
        # project path
        ttk.Label(project_pane, text='Project Location'
        ).grid(column=0, row=3, sticky='w', padx=15, pady=(0, 3))
        ttk.Entry(project_pane, textvariable=self.project_path,
        ).grid(column=0, row=4, sticky='we', padx=15, pady=(0, 15))
        
        # environment path
        ttk.Label(project_pane, text='Environment Location',
        ).grid(column=0, row=5, sticky='w', padx=15, pady=(0, 3))
        ttk.Entry(project_pane, textvariable=self.environment_path,
        ).grid(column=0, row=6, sticky='we', padx=15, pady=(0, 15))
        
        # update attributes
        btn_border = ttk.Frame(project_pane, style='BtnBorder.TFrame')
        btn_border.grid(column=0, row=7, sticky='we', padx=15, pady=(5, 15))
        ttk.Button(btn_border, text='Save Changes'
        ).pack(fill='both', expand=True, padx=1, pady=1)
        
        
        ###########################################
        # console pane
        
        console_pane = ttk.Frame(paned_window)
        paned_window.add(console_pane, minsize=200)
        
        console = tkinter.Text(console_pane, width=1, height=1, bd=0)
        console.pack(fill='both', expand=True)
