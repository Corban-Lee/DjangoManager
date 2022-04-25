import tkinter
from tkinter import ttk


def get_all_children(widget:tkinter.Widget|ttk.Widget):
    children = widget.winfo_children()
    for child in children:
        children.extend(child.winfo_children())
    return children
