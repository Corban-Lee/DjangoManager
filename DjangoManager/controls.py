import sys
import logging
import tkinter
from tkinter import ttk
from datetime import datetime, timedelta
from subprocess import Popen, PIPE
from threading import Thread

from utils import clone_widget
from tabs import Project


log = logging.getLogger(__name__)


class Console(tkinter.Text):
    def __init__(self, master:ttk.Widget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        
    def write(self, text) -> None:
        self.insert('end', text)
        self.see('end')  # auto scroll to bottom
        
    def flush(self) -> None:
        pass


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
        
        ttk.Button(
            self, text='Run Server', 
            command=self.on_run
        ).pack(side='left', padx=(10, 0), pady=10)
        ttk.Button(
            self, text='Migrate', 
            command=self.on_migrate
        ).pack(side='left', padx=(10, 0), pady=10)
        ttk.Button(
            self, text='Make Migrations', 
            command=self.on_make_migrations
        ).pack(side='left', padx=(10, 0), pady=10)
        
        return
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
            
    def on_run(self) -> None:
        
        def execute():
            self.master.tab.project.is_running = True
            project: Project = self.master.tab.project
            cmd = [
                project.env_path + '/Scripts/Python.exe',
                project.path + '/manage.py', 
                'runserver', '0.0.0.0:8000'
            ]
            p = Popen(cmd, stdout=PIPE, bufsize=1, text=True)
            while p.poll() is None:
                msg = p.stdout.readline().strip()
                if msg:
                    print(msg)
                
        thread = Thread(target=execute)
        thread.start()

    def on_migrate(self) -> None:
        print('migrating ...')

    def on_make_migrations(self) -> None:
        print('making migrations ...')

class ProjectFrame(ttk.Frame):
    def __init__(self, root, master):
        super().__init__(master)
        self.window = root.window
        self.root = root
        
        self.project_name = tkinter.StringVar()
        self.project_path = tkinter.StringVar()
        self.project_env_path = tkinter.StringVar()
        self.project_last_run = tkinter.StringVar(
            # temp
            value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        )
        self.project_last_migration = tkinter.StringVar(
            # temp
            value=datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
        )
        
        paned_window = tkinter.PanedWindow(self)
        paned_window.pack(fill='both', expand=True)
        
        # overlay when no project selected
        self.modem = ttk.Frame(self)
        ttk.Label(
            self.modem, style='Header.TLabel',
            text='Open a project to continue.'
        ).place(relx=.5, rely=.5, anchor='center')
        
        self.controls = ControlFrame(self)
        self.controls.pack(side='bottom', fill='x')
        
        self.console = Console(paned_window, width=1, height=1, borderwidth=0)
        
        container = ttk.Frame(self)
        ttk.Label(
            container, style='Header.TLabel', 
            textvariable=self.project_name
        ).grid(
                column=0, columnspan=2, row=0, 
                sticky='w', padx=15, pady=15
            )
        
        # project path
        ttk.Label(container, text='Path:'
        ).grid(column=0, row=1, sticky='w', padx=(15, 5))
        ttk.Label(container, textvariable=self.project_path
        ).grid(column=1, row=1, sticky='w')
        
        # environment path
        ttk.Label(container, text='Environment Path:'
        ).grid(column=0, row=2, sticky='w', padx=(15, 5))
        ttk.Label(container, textvariable=self.project_env_path
        ).grid(column=1, row=2, sticky='w')
        
        # last server run
        ttk.Label(container, text='Last Run:'
        ).grid(column=0, row=3, sticky='w', padx=(15, 5))
        ttk.Label(container, textvariable=self.project_last_run
        ).grid(column=1, row=3, sticky='w')
        
        # last migration
        ttk.Label(container, text='Last Migration:'
        ).grid(column=0, row=4, sticky='w', padx=(15, 5))
        ttk.Label(container, textvariable=self.project_last_migration
        ).grid(column=1, row=4, sticky='w')
        
        paned_window.add(container, minsize=200, stretch='first')
        paned_window.add(self.console, minsize=200, stretch='first')
        self.unload('all')  
        
    def load(self, tab) -> None:
        self.tab = tab
        project = tab.project
        self.project_name.set(project.name)
        self.project_path.set(project.path)
        self.project_env_path.set(project.env_path)
        self.modem.place_forget()
        sys.stdout = self.console
        
    def unload(self, project:str) -> None:
        if project == 'all':
            self.modem.place(x=0, y=0, relw=1, relh=1, anchor='nw')
            self.modem.lift()
        