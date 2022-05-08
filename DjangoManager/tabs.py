import logging
from select import select
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

from utils import text_length_check
from constants import IMAGES_DIR


log = logging.getLogger(__name__)


class Project:
    # maybe use a dataclass ??
    last_run: datetime = None
    last_migration: datetime = None
    
    def __init__(self, root, name:str, path:str, env_path:str):
        self.root = root
        self.name = name
        self.path = path
        self.env_path = env_path


class Tab(ttk.Frame):
    """
        Tab widget. Can be dragged along a trough and moved between 
        other tab widgets.
    """
    selected: bool = False

    def __init__(self, master, project):
        super().__init__(master, style=f'Tab.TFrame', width=100)
        self.project: Project = project
        self.rowconfigure(index=1, weight=1)
        self.bind('<Button-1>', self.drag)
        
        # add widget to the end of the trough. This will automatically
        # put the widget on the right side of existing tab widgets.
        self.pack(side='left', fill='y')
        
        self.text = tkinter.StringVar(value=project.name)
        self.text.trace_add(
            'write', 
            lambda v, *_: v.set(text_length_check(v.get(), 20))
        )
        
        self.label = ttk.Label(self, textvariable=self.text)
        self.label.grid(column=1, row=1, sticky='nsew')
        self.label.bind('<Button-1>', self.drag)

        # get light and dark 'x' images for the close button
        self.close_imgs = {}
        for color in ('light', 'dark'):
            img = Image.open(f'{IMAGES_DIR}/close_{color}.png')
            img = img.resize((15, 15))
            img = ImageTk.PhotoImage(img)
            self.close_imgs[color] = img
        
        self.close_btn = ttk.Button(
            self, cursor='hand2',
            command=self._destroy
        )
        self.close_btn.grid(column=2, row=1, sticky='nes')

        right_border = ttk.Frame(
            self, width=1,
            style='TabSeparator.TFrame'
        )
        right_border.grid(column=3, row=1, sticky='ns')

        # dont grid this border. it should only be shown when the tab
        # is being dragged by the user. It should be removed when the
        # tab is released by the user.
        self.left_border = ttk.Frame(
            self, width=1,
            style='TabSeparator.TFrame'
        )

        # this widget will replace the tab's original position when the
        # tab is being moved. It will be ungridded when the tab is 
        # released by the user.
        self.reserved_space = ttk.Frame(self.master)
        self.reserved_space.pack_propagate(False)
        reserved_vert_border = ttk.Frame(
            self.reserved_space, width=1,
            style='TabSeparator.TFrame'
        )
        reserved_vert_border.pack(side='right', fill='y')
        
        # deselecting changes all of the child widget styles to their
        # defaults. So instead of setting styles above where the 
        # children have been created, just call deselect to set the 
        # style. This means that code hasn't been repeated.
        self.deselect()
        
        log.debug(f'initialized tab with name: {self.text.get()}')
        
    def select(self):
        """Called when the tab is clicked"""
        self.selected = True
        self.update_style()
    
    def deselect(self):
        """Called when a different instance of Tab is selected"""
        self.selected = False
        self.update_style()
        
    def update_style(self, select_override:bool=None):
        """Updates this tab's style and updates it's childrens style"""
        s = select_override if select_override is not None else self.selected
        if s:
            style = 'SelectedTab.TFrame'
            label_style = 'SelectedTabText.TLabel'
            button_style = 'SelectedTabBtn.TLabel'
            image_colour = 'dark'
        else:
            style = 'Tab.TFrame'
            label_style = 'TabText.TLabel'
            button_style = 'TabBtn.TLabel'
            image_colour = 'dark'
            
        # change styles to active varients.
        self.config(style=style)
        self.label.config(style=label_style)
        self.close_btn.config(style=button_style)
        
        # change the 'x' image for the close button to match the 
        # background colours.
        img = self.close_imgs[image_colour]
        self.close_btn.image = img
        self.close_btn.config(image=img)
            
    def _destroy(self):
        self.master.remove_tab(self)
        log.debug(f'destroyed tab with name: {self.text.get()}')

    def drag(self, event:tkinter.Event) -> None:
        """Allows the user to drag the tab"""
        
        # inform tab manager of selection
        self.master.on_tab_select(self)
        
        # create reserved space for the widget
        self.reserved_space.config(width=self.winfo_width())
        self.reserved_space.pack(side='left', fill='y', before=self)
        
        # add left side border while moving
        self.left_border.grid(column=0, row=1, sticky='ns')
        
        # if the tab isn't raised it can appear below other
        # tabs and reserved space
        self.tkraise()
        
        original_x = self.winfo_x() - 1  # account for left border
        current_x = original_x - event.x_root
        trough_height = self.master.winfo_height()
        
        def release(event:tkinter.Event) -> None:
            """Left mouse button is released"""
            
            # create a list of everything on the tab trough excluding self
            self.left_border.grid_forget()
            items = self.master.tabs.copy()
            items.append(self.reserved_space)
            items.remove(self)

            # 'x' coordinate, used to determine where to put the widget when dropped
            x: int = int(self.winfo_x() + (self.winfo_width() / 3))

            # determine where to place released tab
            for item in items:
                
                # is this tab overlapping another tab?
                tab_x = item.winfo_x()
                if x in range(tab_x, tab_x + item.winfo_width()):
                    break  # break the loop to confinue with the current iterated tab

                # widget is offscreen to the left. put it before the first item then 
                # return nothing to end the func call.
                if x <= 0 and tab_x == 0:
                    self.pack(side='left', fill='y', before=item)
                    self.reserved_space.pack_forget()
                    return
                
            # self is not overlapping any items: move it to the end of
            # the trough.
            else:
                self.pack(side='left', fill='y')
                self.reserved_space.pack_forget()
                return
                
            # now that we have confirmed self is hovering on an item we need
            # to determine if self has moved from left to right or vise versa.
            #
            # 'original_x' is the pos of self before the user clicked & dragged
            # on it.
            #
            # 'x' is the current x coordinate of self.
            
            # self moved left to right
            if x > original_x:
                self.pack(side='left', fill='y', after=item)
                
            # self moved right to left
            else:
                self.pack(side='left', fill='y', before=item)

            # clear the reserved space
            self.reserved_space.pack_forget()

        def move(event:tkinter.Event) -> None:
            """Cursor is moved while left mouse button is active"""
            
            new_x = event.x_root + current_x
            
            # prevent tab going past the trough border -> uncomment & indent below to reactivate
            # if not (new_x >= self.master.winfo_width() - self.winfo_width() or new_x < 0):
            self.place(x=new_x, h=trough_height)
    
            # TODO: did this to reduce fps lag. Don't know if it actually works. Test it?
            self.update()

        event.widget.bind('<B1-Motion>', move)
        event.widget.bind('<ButtonRelease-1>', release)
        move(event)

        


class TabManager(ttk.Frame):
    """
        Tab manager for all of the tab widgets. 
        Also acts as a tab trough widget.
    """
    tabs: list[Tab] = []
    selected_tab: Tab = None
    
    def __init__(self, root):
        super().__init__(root.window, style='TabTrough.TFrame')
        self.root = root

        # dont want children to determine the size of this widget.
        self.pack_propagate(False)
        self.pack(side='top', fill='x')

        # saves the height of the scrollbar to the config file so it will be the
        # same when the user next loads the app.
        self.bind('<Configure>', self.on_trough_resize)
        self.config(height=root.cfg.data['tabs']['trough_height'])  # get height from config
        
    def add_tab(self, project):
        """Append a new tab to the trough."""
        self.tabs.append(Tab(self, project))
        
    def on_trough_resize(self, event:tkinter.Event):
        """Writes the current height of the trough to the config"""
        self.root.cfg.data['tabs']['trough_height'] = self.winfo_height()
        
    def on_tab_select(self, clicked_tab:Tab):
        """Deselects any tab that wasn't the last clicked tab"""
        for tab in self.tabs:
            if tab.selected:
                tab.deselect()
                break  
            
        clicked_tab.select()
        self.selected_tab = clicked_tab
        self.root.project_frame.load(clicked_tab.project)
        
        # update config
        self.root.cfg.data['tabs']['last_tab'] = clicked_tab.project.name


    def remove_tab(self, tab:Tab):
        """Remove and destroy a tab"""
        self.tabs.remove(tab)
        
        # try to select another tab if any exist
        if self.tabs:
            unload = tab.project
            if tab.selected:
                new_tab = self.tabs[-1]
        else:
            unload = 'all'
            
        self.root.project_frame.unload(unload)
        try:
            self.on_tab_select(new_tab)
        except UnboundLocalError:
            pass
        
        # update config            
        self.root.cfg.data['projects'].pop(tab.project.name)

        tab.destroy()
        
    def auto_load_tabs(self) -> None:
        data = self.root.cfg.data
        for project_name, project in data['projects'].items():
            project = Project(
                self.root, 
                project_name, 
                project['path'],
                project['env_path']
            )
            self.add_tab(project)
            
        last_tab = data['tabs']['last_tab']
        if last_tab:
            for tab in self.tabs:
                if tab.project.name == last_tab:
                    self.on_tab_select(tab)
                    break