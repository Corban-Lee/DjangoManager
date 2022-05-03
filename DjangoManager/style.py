import logging
from tkinter import ttk

from utils import get_json
from constants import THEME_DIR


log = logging.getLogger(__name__)


class StyleManager(ttk.Style):
    def __init__(self, root):
        super().__init__(root.window)
        
        self._create_theme('light.json')
        self.theme_use('light')
        
        # redefined tbutton layout without dotted focus outline
        self.layout(
            'TButton',
            [('Button.button', {'sticky': 'nsew', 'children': [
                ('Button.border', 
                    {'sticky': 'nswe', 'border': '1', 'children': [
                        ('Button.padding', {'sticky': 'nswe', 'children': [
                            ('Button.label', {'sticky': 'nswe'})
            ]})]})]})]
            )
        
    def _create_theme(self, filename:str):
        """
            Looks for argument filename in themes directory and 
            attempts to load it.
        """
        data = get_json(THEME_DIR + '/' + filename)
        self.theme_create(
            themename=data['name'],
            parent=data['parent'],
            settings=data['settings']
        )
        
        # self.configure(
        #     'Header.TLabel',
        #     font=('TkDefaultFont', 13),
        #     padding=(0, 0, 0, 15),
        # )
        
        # self.configure('TLabel', background='#E4E4E4')

        # self.configure('TabSeparator.TFrame', background='#a5a4a5')
        
        # self.configure('TFrame', background='#E4E4E4')
        # self.paned_window = {
        #     'background': '#E4E4E4',
        #     'sashwidth': 3
        # }
        
        # self.configure('TButton', borderwidth=0)
        # self.configure('BtnBorder.TFrame', background='#a5a4a5')
        
        # self.configure(
        #     'TEntry',
        #     background='gray90',
        #     borderwidth=0,
        #     padding=(5,2,5,2)
        # )
        
        # ###########
        
        # # Styles for tabs
        
        # # the trough contains tabs
        # self.configure(
        #     'TabTrough.TFrame',
        #     background='gray95'
        # )
        
        # # the tabs themselves
        # self.configure(
        #     'Tab.TFrame',
        #     border=1,
        #     relief='flat',
        #     background='#D9D9D9'
        # )
        
        # # the text on the tabs
        # self.configure(
        #     'TabText.TLabel',
        #     background='#D9D9D9',
        #     padding=(5, 1, 25, 0)
        # )

        # # the close button for the tabs
        # self.configure(
        #     'TabBtn.TLabel',
        #     background='#D9D9D9',
        #     padding=(5, 0, 5, 0)
        # )
        # self.map(
        #     'TabBtn.TLabel',
        #     background=(
        #         ('pressed', 'gray75'), 
        #         ('active', 'gray80')
        #     )
        # )
        
        # # reserved space is a sunken looking color that occupies the emptied space when
        # # a tab is actively being moved.
        # self.configure(
        #     'TabReserved.TFrame',
        #     background='gray45'
        # )
        
        # ########
        
        # # Alternative tab styles (for when tabs are selected/active/whatever)
        
        # self.configure(
        #     'SelectedTab.TFrame',
        #     background='gray70',
        #     relief='flat'
        # )
        
        # self.configure(
        #     'SelectedTabText.TLabel',
        #     background='gray70',
        #     padding=(5, 1, 25, 0)
        # )
        
        # self.configure(
        #     'SelectedTabBtn.TLabel',
        #     background='gray70',
        #     padding=(5, 0, 5, 0)
        # )
        # self.map(
        #     'SelectedTabBtn.TLabel',
        #     background=(
        #         ('pressed', 'gray60'), 
        #         ('active', 'gray65')
        #     )
        # )
        
        
        # ##########
