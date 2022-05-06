import os
import logging
from tkinter import ttk, font

from utils import get_json, get_all_children
from constants import THEME_DIR


log = logging.getLogger(__name__)


class StyleManager(ttk.Style):
    
    tk_settings = {}
    
    def __init__(self, root):
        super().__init__(root.window)
        self.default_font = font.nametofont('TkDefaultFont')
        self._load_themes()
                
    def _load_themes(self) -> None:
        for filename in os.listdir(THEME_DIR):
            if filename.endswith('.json'):
                self._create_theme(filename)
            else:
                log.error(f"Unknown file type in themes directory: '{filename}'")

    def switch_theme(self, theme_name:str) -> None:
        """Change the current theme"""
        self.theme_use(theme_name)
        # Remove focus outline from buttons
        self.layout(
            'TButton', [
                ('Button.button', {'sticky': 'nsew', 'children': [
                    ('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [
                        ('Button.padding', {'sticky': 'nswe', 'children': [
                            ('Button.label', {'sticky': 'nswe'})
                        ]})
                    ]})
                ]})
            ]
        )
        # TODO: apply tk settings here
        # for widget in get_all_children(self.master):
        #     break 
        log.info(f"Switched to theme: '{theme_name}'")
            
    def _create_theme(self, filename:str) -> None:
        """
            Looks for argument filename in themes directory and 
            attempts to load it.
        """
        data = get_json(THEME_DIR + '/' + filename)
        theme_name = data['name']  # retrieve data here to avoid doing a lookup twice
        fnt_fam, fnt_size = data['default_font']
        self.tk_settings[theme_name] = data['tk_settings']
        self.default_font.configure(family=fnt_fam, size=fnt_size)
        self.theme_create(
            themename=theme_name,
            parent=data['parent'],
            settings=data['ttk_settings']
        )
        log.info(f"Created theme: {theme_name}")
