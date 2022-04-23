import logging
from tkinter import ttk


log = logging.getLogger(__name__)


class StyleManager(ttk.Style):
    def __init__(self, root):
        super().__init__(root.window)
        self.theme_use('default')
        
        # redefined tbutton layout without dotted focus outline
        self.layout(
            'TButton',
            [('Button.button', 
                {'sticky': 'nswe', 'children': [
                    ('Button.padding', {'sticky': 'nswe', 'children': [
                        ('Button.label', {'sticky': 'nswe'})
            ]})]})])
        
        # style for tabs
        self.configure(
            'TabTrough.TFrame',
            background='#E9E9E9'
        )
        self.configure(
            'Tab.TFrame',
            border=1,
            background='#F1F1F1'
        )
        self.configure(
            'TabText.TLabel',
            background='#F1F1F1'
        )
        self.configure(
            'TabClose.TButton',
            borderwidth=0,
            highlightthickness=0,
            focuscolor='#F1F1F1',
            background='#F1F1F1',
            foreground='black'
        )
        self.configure(
            'TabReserved.TFrame',
            background='#E9E9E9'
        )
