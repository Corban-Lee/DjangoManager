import logging
import tkinter
from tkinter import ttk

from utils import clone_widget


log = logging.getLogger(__name__)


class ControlFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style='Controls.TFrame')
        self.window = master.root.window
        self.root = master.root
        
        # top border
        ttk.Frame(self, style='Border.TFrame'
        ).pack(side='top', fill='x')
        
        ttk.Button(self, text='Close Project'
        ).pack(side='right', padx=(0, 10), pady=10)
        ttk.Button(self, text='Edit Project'
        ).pack(side='right', padx=(0, 10), pady=10)
        
        ttk.Button(self, text='Run Server'
        ).pack(side='left', padx=(10, 0), pady=10)
        ttk.Button(self, text='Migrate'
        ).pack(side='left', padx=(10, 0), pady=10)
        ttk.Button(self, text='Make Migrations'
        ).pack(side='left', padx=(10, 0), pady=10)
        
        for widget in self.winfo_children():
            if not isinstance(widget, (ttk.Button, ttk.Entry)):
                continue

            pack_details = widget.pack_info()
            widget.pack_forget()

            border = ttk.Frame(self, style='Border.TFrame')
            border.pack(pack_details)
            
            widget_clone = clone_widget(widget, parent=border)
            widget_clone.pack(fill='both', expand=True, padx=1, pady=1)
            widget.destroy()

class ProjectFrame(ttk.Frame):
    def __init__(self, root, master):
        super().__init__(master)
        self.window = root.window
        self.root = root
        
        self.project_name = tkinter.StringVar()
        self.project_path = tkinter.StringVar()
        self.project_env_path = tkinter.StringVar()
        
        # overlay when no project selected
        self.modem = ttk.Frame(self)
        ttk.Label(
            self.modem, style='Header.TLabel',
            text='Open a project to continue.'
        ).place(relx=.5, rely=.5, anchor='center')
        
        self.controls = ControlFrame(self)
        self.controls.pack(side='bottom', fill='x')
        
        console = ttk.Frame(self)
        console.pack(side='right', fill='both', expand=True)
        ttk.Label(console, text='TODO: output terminal here'
        ).place(relx=.5, rely=.5, anchor='center')
        
        ttk.Frame(self, style='Border.TFrame'
        ).pack(side='right', fill='y')
        
        container = ttk.Frame(self)
        container.pack(side='left', fill='both', expand=True)

        ttk.Label(
            container, style='Header.TLabel', 
            textvariable=self.project_name
        ).grid(column=0, row=0, sticky='w', padx=15, pady=15)    
        
        self.unload('all')  
        
    def load(self, project) -> None:
        self.project_name.set(project.name)
        self.project_path.set(project.path)
        self.project_env_path.set(project.env_path)
        self.modem.place_forget()
        
    def unload(self, project:str) -> None:
        print('unloaded project(s):', project)
        if project == 'all':
            self.modem.place(x=0, y=0, relw=1, relh=1, anchor='nw')
            self.modem.lift()
        