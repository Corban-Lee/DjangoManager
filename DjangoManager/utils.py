import os
import json
import logging
import tkinter
from tkinter import ttk
from typing import Any
from PIL import Image, ImageTk
from dataclasses import dataclass

from constants import CONFIG_FILENAME, IMAGES_DIR


log = logging.getLogger(__name__)


def get_all_children(widget:tkinter.Widget|tkinter.Tk) -> list[tkinter.Widget]:
    """Returns a list of every widget below the entered widget"""
    children = widget.winfo_children()
    for child in children:
        children.extend(child.winfo_children())
    return children


def text_length_check(text:str, length:int):
    """Replaces long strings with a shortened copy ending in '...'"""
    if len(text) > length:
        return text[:length - 3] + '...'
    return text

def get_json(fp:str) -> Any:
    with open(fp, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def write_json(fp:str, data:Any) -> None:
    with open(fp, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def clone_widget(widget:ttk.Widget, parent:ttk.Widget|None) -> ttk.Widget:
    """Returns a clone of the widget. Parent is the same if left as NoneType"""
    if parent is None:
        parent = widget.nametowidget(widget.winfo_parent())
    clone = widget.__class__(parent)
    for key in widget.configure():
        if key in ('class',):
            continue
        clone.configure({key: widget.cget(key)})
    return clone

def label_to_button(widget:ttk.Label, command:Any) -> None:
    """Gives labels button-like properties"""
    def clicked():
        widget.bind('<ButtonRelease-1>', lambda e: command())
        widget.bind('<Leave>', lambda e: leave(), add=True)
    def leave():
        widget.unbind('<ButtonRelease-1>')
        widget.bind('<Enter>', lambda e: clicked(), add=True)
    widget.bind('<Button-1>', lambda e: clicked())
    
def set_widget_image(
        widget:ttk.Widget, width:int, height:int, 
        default_img_fn:str, active_img_fn:str|None=None
    ) -> None:
    """Set an image to a tkinter widget"""
    default_image = Image.open(IMAGES_DIR + '/' + default_img_fn)
    default_image = ImageTk.PhotoImage(default_image.resize((width, height), Image.ANTIALIAS))
    widget._default_image = default_image
    if active_img_fn:
        active_image = Image.open(IMAGES_DIR + '/' + active_img_fn)
        active_image = ImageTk.PhotoImage(active_image.resize((width, height), Image.ANTIALIAS))
        widget._active_image = active_image
        widget.bind('<Enter>', lambda e: widget.configure(image=active_image))
        widget.bind('<Leave>', lambda e: widget.configure(image=default_image))
    widget.configure(image=default_image)

@dataclass
class Project:
    name: str
    dir: str
    env: str


class ConfigManager:
    """Manages project settings"""
    data: dict = {}
    _default: dict = {
        'tabs': {
            'trough_height': 25
        }
    }
    
    def __init__(self, root):
        self.dir = root.dirs.user_config_dir + '/' + CONFIG_FILENAME
        self.read()
        
    def restore_defaults(self) -> None:
        """Restore default values to config file"""
        log.info('restoring defaults to log file')
        self.data = self._default
        filemode = 'w' if os.path.exists(self.dir) else 'x'
        self.write(filemode)
    
    def read(self) -> None:
        """Read data from the config file and save it as a dictionary: 'self.data'"""
        try:
            self.data = get_json(self.dir)
        except FileNotFoundError:
            log.error(f"couldn't find config file in {self.dir}")
            self.restore_defaults()
        except json.JSONDecodeError:
            log.error(f"config file in {self.dir} couldn't be read")
            self.restore_defaults()                                             
        
    def write(self, mode:str='w'):
        """Writes the current config to the config file'"""
        write_json(self.dir, self.data)
        
        
class Titlebar(ttk.Frame):
    def __init__(self, root):
        super().__init__(root.window, height=30)
        self.pack_propagate(False)
        self.pack(side='top', fill='x')
        self.bind('<Button-1>', self.on_click)
        self.window = root.window
        self.root = root
        
        title = ttk.Label(self, text=root.window.title(), style='WindowTitle.TLabel')
        title.place(relx=.5, rely=.5, anchor='center')
        title.bind('<Button-1>', self.on_click)
        
        
        self.close_btn = ttk.Button(self, style='WindowClose.TLabel')
        self.close_btn.pack(side='right', fill='y')
        set_widget_image(
            self.close_btn, width=15, height=15, 
            default_img_fn='close_dark.png',
            active_img_fn='close_light.png' 
            )
        label_to_button(self.close_btn, command=self.on_close)
        
        self.maximize_btn = ttk.Button(self, style='WindowBtn.TLabel')
        self.maximize_btn.pack(side='right', fill='y')
        set_widget_image(
            self.maximize_btn, width=15, height=15, 
            default_img_fn='maximize_dark.png',
            )
        label_to_button(self.maximize_btn, command=print)
        
        self.minimize_btn = ttk.Button(self, style='WindowBtn.TLabel')
        self.minimize_btn.pack(side='right', fill='y')
        set_widget_image(
            self.minimize_btn, width=15, height=15, 
            default_img_fn='minimize_dark.png',
            )
        label_to_button(self.minimize_btn, command=print)
        
        self.pin_btn = ttk.Button(self, style='WindowBtn.TLabel')
        self.pin_btn.pack(side='right', fill='y')
        set_widget_image(
            self.pin_btn, width=15, height=15, 
            default_img_fn='pin_dark.png',
            )
        label_to_button(self.pin_btn, command=self.on_pin)
                
        log.info('Created custom titlebar')
        
    def on_close(self) -> None:
        self.root.on_exit()
        
    def on_pin(self) -> None:
        self.window.attributes('-topmost', not self.window.attributes('-topmost'))
        
    def on_click(self, event:tkinter.Event) -> None:
        start_x = event.x_root
        start_y = event.y_root
        window_x = self.window.winfo_x() - start_x
        window_y = self.window.winfo_y() - start_y
        
        def move_window(event:tkinter.Event):
            self.window.geometry(f'+{event.x_root + window_x}+{event.y_root + window_y}')
        
        event.widget.bind('<B1-Motion>', move_window)
        
        
