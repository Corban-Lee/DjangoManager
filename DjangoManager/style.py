import os
import logging
from tkinter import ttk

from utils import get_json, get_all_children
from constants import THEME_DIR


log = logging.getLogger(__name__)


class StyleManager(ttk.Style):
    
    tk_settings = {}
    
    def __init__(self, root):
        super().__init__(root.window)
        self._load_themes()
                
    def _load_themes(self) -> None:
        for filename in os.listdir(THEME_DIR):
            if filename.endswith('.json'):
                self._create_theme(filename)

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
        for widget in get_all_children(self.master):
            break
            
    def _create_theme(self, filename:str) -> None:
        """
            Looks for argument filename in themes directory and 
            attempts to load it.
        """
        data = get_json(THEME_DIR + '/' + filename)
        theme_name = data['name']  # retrieve data here to avoid doing a lookup twice
        self.tk_settings[theme_name] = data['tk_settings']
        self.theme_create(
            themename=theme_name,
            parent=data['parent'],
            settings=data['ttk_settings']
        )