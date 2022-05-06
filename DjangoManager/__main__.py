import logging
import tkinter
from tkinter import ttk, simpledialog
from pathlib import Path
from appdirs import AppDirs
from PIL import Image, ImageTk
from ctypes import windll

import logs
from tabs import TabManager
from cfg import ConfigManager
from style import StyleManager
from controls import ControlFrame
from utils import make_button, set_widget_image
from constants import (
    IMAGES_DIR,
    GWL_EXSTYLE,
    WS_EX_APPWINDOW,
    WS_EX_TOOLWINDOW
)


__version__ = '0.0.0'
log = logging.getLogger(__name__)


class DropMenu(ttk.Frame):
    def __init__(self, root):
        super().__init__(
            root.window, width=150, height=180, 
            style='Menu.TFrame'
        )
        self.root = root
        self.grid_propagate(False)
        self.columnconfigure(index=0, weight=1)
        
        # create border on bottom and right sides
        ttk.Frame(self, style='Border.TFrame'
        ).place(x=0, rely=1, relw=1, anchor='sw')
        ttk.Frame(self, style='Border.TFrame'
        ).place(relx=1, y=0, relh=1, anchor='ne')
        
        ttk.Label(
            self, text='Project Menu', style='MenuHeader.TLabel'
        ).grid(column=0, row=0, sticky='we', padx=5, pady=(7, 0))
        ttk.Frame(self, style='Border.TFrame'
        ).grid(column=0, row=1, sticky='we', padx=10, pady=(3, 5))
        
        # project menu options
        ttk.Button(  # create a new project (unfunctional)
            self, text='Create New', style='MenuBtn.TLabel'
        ).grid(column=0, row=2, sticky='we', padx=5)
        ttk.Button(  # add existing project from file (unfunctional)
            self, text='Add Existing', style='MenuBtn.TLabel'
        ).grid(column=0, row=3, sticky='we', padx=5)
        ttk.Button(  # close currently selected project tab (unfunctional)
            self, text='Close Project Tab', style='MenuBtn.TLabel'
        ).grid(column=0, row=4, sticky='we', padx=5)
        ttk.Button(  # delete currently selected project (unfunctional)
            self, text='Remove Project', style='MenuBtn.TLabel'
        ).grid(column=0, row=5, sticky='we', padx=5)
        
        # debug menu options
        ttk.Button(  # add a new empty tab
            self, text='Add Tab', style='MenuBtn.TLabel', 
            command=lambda: self.on_btn(self.on_add_tab)
        ).grid(column=0, row=6, sticky='we', padx=5)
        ttk.Button(  # add a new tab with custom text
            self, text='Add Tab With Text', style='MenuBtn.TLabel',
            command=lambda: self.on_btn(self.on_add_text_tab)
        ).grid(column=0, row=7, sticky='we', padx=5)
        ttk.Button(  # add a tab tied to a project (unfunctional)
            self, text='Add Real Tab', style='MenuBtn.TLabel',
            command=lambda: self.on_btn(self.on_add_real_tab)
        ).grid(column=0, row=8, sticky='we', padx=(5, 7))
        
    def on_btn(self, command) -> None:
        self.root.titlebar.on_menu()
        command()
        
    def on_add_tab(self, title:str|None=None) -> None:
        title = f'Tab Number {len(self.root.tabs.tabs)}' if title is None else title
        self.root.tabs.add_tab(title)
    
    def on_add_text_tab(self) -> None:
        title = simpledialog.askstring('Tab Name', 'Provide a name for this new tab:')
        self.on_add_tab(title)
    
    def on_add_real_tab(self) -> None:
        pass


class Titlebar(ttk.Frame):
    _last_min_valid = True
    
    def __init__(self, root):
        super().__init__(root.win_border, height=30, style='WinTB.TFrame')
        self.menu = DropMenu(root)
        self.pack_propagate(False)
        self.pack(side='top', fill='x', padx=1, pady=(1, 0))
        self.bind('<Button-1>', self.on_click)
        self.window = root.window
        self.root = root 
        
        title = ttk.Label(self, text=root.window.title(), style='WinTitle.TLabel')
        title.place(relx=.5, rely=.5, anchor='center')
        title.bind('<Button-1>', self.on_click)
        
        btn_colour = 'light'  # temp variable. Will later be controlled by config.
        
        # 'X' button to close the window
        close_btn = ttk.Button(self, style='WinClose.TLabel')
        close_btn.pack(side='right', fill='y')
        make_button(close_btn, command=self.on_close)
        set_widget_image(
            close_btn, width=15, height=15, 
            default_img_fn=f'close_{btn_colour}.png',
        )
        
        # maximize window button
        self.max_btn = ttk.Button(self, style='WinBtn.TLabel')
        self.max_btn.pack(side='right', fill='y')
        make_button( self.max_btn, command=self.on_maximize)
        set_widget_image(
            self.max_btn, width=15, height=15, 
            default_img_fn=f'maximize_{btn_colour}.png',
        )
        
        # restore window button
        self.res_btn = ttk.Button(self, style='WinBtn.TLabel')
        make_button(self.res_btn, command=self.on_restore)
        set_widget_image(
            self.res_btn, width=15, height=15, 
            default_img_fn=f'restore_{btn_colour}.png',
        )
        
        # minimize window button
        min_btn = ttk.Button(self, style='WinBtn.TLabel')
        min_btn.pack(side='right', fill='y')
        make_button(min_btn, command=self.on_minimize)
        set_widget_image(
            min_btn, width=15, height=15, 
            default_img_fn=f'minimize_{btn_colour}.png',
        )
        
        # application menu button - toggles drop down menu
        self.menu_btn = ttk.Button(self, style='WinBtn.TLabel')
        self.menu_btn.pack(side='left', fill='y')
        make_button(self.menu_btn, command=self.on_menu)
        set_widget_image(
            self.menu_btn, width=15, height=15,
            default_img_fn=f'menu_{btn_colour}.png'
        )
        
        # application pin button - toggles 'keep window on top layer'
        self.pin_btn = ttk.Button(self, style='WinBtn.TLabel')
        self.pin_btn.pack(side='left', fill='y')
        make_button(self.pin_btn, command=self.on_pin)
        set_widget_image(
            self.pin_btn, width=15, height=15, 
            default_img_fn=f'pin_{btn_colour}.png',
            )
                
        root.window.bind('<Map>', self.on_map)
        log.info('Titlebar initialized')
        
    def on_map(self, event:tkinter.Event=None) -> None:
        self.window.overrideredirect(True)
        if self._last_min_valid:
            self.root._set_appwindow()
            self._last_min_valid = False
        
        
    def on_close(self, event:tkinter.Event) -> None:
        self.root.on_exit()
        
    def on_maximize(self, event:tkinter.Event) -> None:
        self.window.state('zoomed')
        self.res_btn.pack(side='right', fill='y', before=self.max_btn)
        self.max_btn.pack_forget()
    
    def on_restore(self, event:tkinter.Event=None) -> None:
        self.window.state('normal')
        self.max_btn.pack(side='right', fill='y', before=self.res_btn)
        self.res_btn.pack_forget()
    
    def on_minimize(self, event:tkinter.Event) -> None:
        if self.window.state() == 'zoomed':
            self.on_restore()
        def minimize():
            self.window.state('withdrawn')
            self.window.overrideredirect(False)
            self.window.state('iconic')
            self._last_min_valid = True
        self.after(10, minimize)
        
    def on_menu(self, event:tkinter.Event=None) -> None:
        self.menu.lift()
        if self.menu.winfo_ismapped():
            self.menu.place_forget()
            style = 'WinBtn.TLabel'
        else:
            self.menu.place(x=1, y=31)
            style = 'WinBtnOn.TLabel'
        self.menu_btn.config(style=style)
        
    def on_pin(self, event:tkinter.Event) -> None:
        pin = not self.window.attributes('-topmost')
        self.window.attributes('-topmost', pin)
        style = 'WinBtnOn.TLabel' if pin else 'WinBtn.TLabel'
        self.pin_btn.config(style=style)
        
    def on_click(self, event:tkinter.Event) -> None:
        """Prepares the titlebar to drag the root window"""
        start_x = event.x_root
        start_y = event.y_root
        # this check is necessary to avoid the window being dragged
        # from a cursor on the opposite side of the screen after starting
        # the drag from a maximized state.
        if self.window.state() == 'zoomed':
            self.on_restore()
            window_x = 0
            window_y = 0
        else:
            window_x = self.window.winfo_x() - start_x
            window_y = self.window.winfo_y() - start_y        
        def move_window(event:tkinter.Event):
            """Updates the coordinates of the root window"""
            self.window.geometry(f'+{event.x_root + window_x}+{event.y_root + window_y}')
        
        event.widget.bind('<B1-Motion>', move_window)
        event.widget.bind('<ButtonRelease-1>', lambda e: event.widget.config(cursor='arrow'))
        event.widget.configure(cursor='fleur')


class Root:
    """Root of the entire application"""
    title = 'Django Manager'
    dir_name = 'DjangoManager'
    window = tkinter.Tk()
    dirs = AppDirs(dir_name, version=__version__)

    def __init__(self):
        self._validate_dirs()
        logs.setup(self.title, __version__, self.dirs)
        
        # setup window
        self.window.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.window.geometry('700x400+150+150')
        self.window.minsize(700, 400)
        self.window.title(self.title)
        self.win_border = tkinter.Frame(self.window, bg='gray20')
        self.win_border.pack(fill='both', expand=True)
        self._setup_titlebar()
        
        # this paned window exists to allow the tab trough to be expanded vertically
        self.paned_window = tkinter.PanedWindow(
            self.win_border, orient='vertical', sashwidth=1, bd=0,
            background='#a3a2a2'
        )
        self.paned_window.pack(side='top', fill='both', expand=True, padx=1, pady=(0, 1))

        # Get & setup managers
        self.cfg = ConfigManager(self)
        self.style = StyleManager(self)
        self.tabs = TabManager(self)
        # self.menu = MenuManager(self)
        log.info('Initialized all managers')
        
        self.control_frame = ControlFrame(self, master=self.win_border)
        self.control_frame.pack(side='bottom', fill='both', expand=True)
        
        self.paned_window.add(self.tabs, minsize=25)
        self.paned_window.add(self.control_frame, minsize=20)
        
        self.style.switch_theme('light')

    def run(self) -> None:
        """Start the app"""
        log.info('starting window main loop')
        self.window.mainloop()
        
    def on_exit(self) -> SystemExit:
        """Properly exits the app"""
        log.info('exiting app')
        self.window.destroy()
        raise SystemExit
    
    def _validate_dirs(self) -> None:
        """Creates app directories if they don't already exist."""
        log.info('validating app dirs')
        Path(self.dirs.user_cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.dirs.user_config_dir).mkdir(parents=True, exist_ok=True)
        Path(self.dirs.user_log_dir).mkdir(parents=True, exist_ok=True)
        
    def _setup_titlebar(self) -> None:
        """Create and configure the custom titlebar"""
        self.window.overrideredirect(True)
        self.window.after(10, self._set_appwindow)
        self.titlebar = Titlebar(self)
        
    def _set_appwindow(self):
        # allows windows to show this app on the taskbar
        hwnd = windll.user32.GetParent(self.window.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
        # re-assert the new window style
        self.window.wm_withdraw()
        self.window.after(10, lambda: self.window.wm_deiconify())
        

if __name__ == '__main__':
    Root().run()
    