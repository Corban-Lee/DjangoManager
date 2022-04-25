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
        
        ###########
        
        # Styles for tabs
        
        # the trough contains tabs
        self.configure(
            'TabTrough.TFrame',
            background='#E9E9E9'
        )
        
        # the tabs themselves
        self.configure(
            'Tab.TFrame',
            border=1,
            relief='flat',
            background='#F1F1F1'
        )
        
        # the text on the tabs
        self.configure(
            'TabText.TLabel',
            background='#F1F1F1'
        )
        
        # the close button for the tabs
        self.configure(
            'TabBtn.TLabel',
            background='#F1F1F1',
            padding=(5, 0, 5, 0)
        )
        self.map(
            'TabBtn.TLabel',
            background=(
                ('pressed', '#F1F1F1'), 
                ('active', '#F1F1F1')
            )
        )
        
        # reserved space is a sunken looking color that occupies the emptied space when
        # a tab is actively being moved.
        self.configure(
            'TabReserved.TFrame',
            background='#DFDFDF'
        )
        
        ########
        
        # Alternative tab styles (for when tabs are selected/active/whatever)
        
        self.configure(
            'SelectedTab.TFrame',
            background='gray',
            relief='flat'
        )
        
        self.configure(
            'SelectedTabText.TLabel',
            background='gray',
            foreground='white'
        )
        
        self.configure(
            'SelectedTabBtn.TLabel',
            background='gray',
            padding=(5, 0, 5, 0)
        )
        self.map(
            'SelectedTabBtn.TLabel',
            background=(
                ('pressed', 'red'), 
                ('active', 'orange')
            )
        )
        
        
        ##########
