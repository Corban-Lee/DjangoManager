import tkinter
from tkinter import ttk


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
