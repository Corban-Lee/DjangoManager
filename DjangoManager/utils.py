import json
import logging
import tkinter
from tkinter import ttk
from typing import Any
from PIL import Image, ImageTk

from constants import IMAGES_DIR, ButtonState


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

# def label_to_button(widget:ttk.Label, command:Any) -> None:
#     """Gives labels button-like properties"""
#     def clicked():
#         widget.bind('<ButtonRelease-1>', lambda e: command())
#         widget.bind('<Leave>', lambda e: leave(), add=True)
#     def leave():
#         widget.unbind('<ButtonRelease-1>')
#         widget.bind('<Enter>', lambda e: clicked(), add=True)
#     widget.bind('<Button-1>', lambda e: clicked())

def make_button(widget:ttk.Label, command=None) -> ttk.Label:
    """
        Gives labels button-like properties. Use this instead of
        tkinter.Button / ttk.Button to avoid the foreground text or
        image moving vertically when clicked.
    """
    def on_click(widget:ttk.Label, event:tkinter.Event):
        # only let the click go through if the mouse is still
        # inside the button and the command is callable.
        if (
            widget.btn_state.get() == str(ButtonState.HOVER) 
            and callable(widget.command)
            ):
            widget.command(event)
    # make the command an attribute for easy access
    widget.command = command
    # the button uses the ButtonState enum to determine when to
    # allow the clicks to register.
    widget.btn_state = tkinter.StringVar(value=ButtonState.REST)
    widget.bind(
        sequence='<Enter>', add=True,
        func=lambda e: widget.btn_state.set(ButtonState.HOVER)
    )
    widget.bind(
        sequence='<Leave>', add=True, 
        func=lambda e: widget.btn_state.set(ButtonState.REST)
    )
    widget.bind('<ButtonRelease-1>', lambda e: on_click(widget, e))
    
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
