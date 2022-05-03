import logging
import tkinter
from tkinter import ttk, simpledialog, messagebox, filedialog
from PIL import Image, ImageTk

from utils import text_length_check, Project
from constants import IMAGES_DIR


log = logging.getLogger(__name__)


class Tab(ttk.Frame):
    
    selected: bool = False

    def __init__(self, master, text:str, command):
        super().__init__(master, style=f'Tab.TFrame')
        self.bind('<Button-1>', self.drag)
        self.rowconfigure(index=1, weight=1)
        
        # text displayed on the tab
        self.text = ttk.Label(self, text=text_length_check(text, 20))
        self.text.grid(column=0, row=1, sticky='nsew')
        self.text.bind('<Button-1>', self.drag)

        # get 'x' images for close button
        self.close_imgs = {}
        for color in ('light', 'dark'):
            img = Image.open(f'{IMAGES_DIR}/tab_close_{color}.png')
            img = img.resize((15, 15))
            img = ImageTk.PhotoImage(img)
            self.close_imgs[color] = img
        
        self.close_btn = ttk.Button(self, command=self._destroy, cursor='hand2')
        self.close_btn.grid(column=1, row=1, sticky='nes')

        vert_sep = ttk.Frame(self, style='TabSeparator.TFrame', width=1)
        vert_sep.grid(column=2, row=1, sticky='ns')
        
        horz_sep = ttk.Frame(self, style='TabSeparator.TFrame', height=1)
        horz_sep.grid(column=0, columnspan=3, row=0, sticky='we')

        # reserves a space when moving the tab
        self.reserved_space = ttk.Frame(self.master)
        
        self.deselect()
        self.pack(side='left', fill='y')
        
    def select(self):
        assert not self.selected
        self.selected = True
        
        self.config(style='SelectedTab.TFrame')
        self.text.config(style='SelectedTabText.TLabel')
        self.close_btn.config(style='SelectedTabBtn.TLabel')
        
        # get 'x' image for close button
        img = self.close_imgs['dark'] # ['light']
        self.close_btn.image = img
        self.close_btn.config(image=img)
    
    def deselect(self):
        self.selected = False
        
        self.config(style='Tab.TFrame')
        self.text.config(style='TabText.TLabel')
        self.close_btn.config(style='TabBtn.TLabel')
        
        # get 'x' image for close button
        img = self.close_imgs['dark']
        self.close_btn.image = img
        self.close_btn.config(image=img)
            
    def _destroy(self):
        self.destroy()
        self.master.tabs.remove(self)
     
    def _snap_to_pos(self, event:tkinter.Event):
        self.pack(side='left', fill='y')

    def drag(self, event:tkinter.Event) -> None:
        """Allows the user to drag the tab"""
        
        self.master.on_tab_select(self)
        
        # create reserved space for the widget
        self.reserved_space.config(width=self.winfo_width())
        self.reserved_space.pack(side='left', fill='y', before=self)
        
        # if the tab isn't raised it can appear below other tabs and reserved space
        self.tkraise()
        
        original_x = self.winfo_x()
        current_x = original_x - event.x_root
        trough_height = self.master.winfo_height()
        
        def release(event:tkinter.Event) -> None:
            """Left mouse button is released"""

            # create a list of everything on the tab trough excluding self
            items = self.master.tabs.copy()
            items.append(self.reserved_space)
            items.remove(self)

            # 'x' coordinate, used to determine where to put the widget when dropped
            x: int = int(self.winfo_x() + (self.winfo_width() / 3))

            for item in items:
                
                # is self overlapping item?
                tab_x = item.winfo_x()
                if x in range(tab_x, tab_x + item.winfo_width()):
                    break

                # widget is offscreen to the left. put it before the first item then 
                # return nothing to end the func call.
                if x <= 0 and tab_x == 0:
                    self.pack(side='left', fill='y', before=item)
                    self.reserved_space.pack_forget()
                    print('placed item at front')
                    return
                
            # self is not overlapping any items: move it to the end of
            # the trough.
            else:
                self.pack(side='left', fill='y')
                self.reserved_space.pack_forget()
                return
                
            # now that we have confirmed self is hovering an item we need
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
    
    tabs: list[Tab] = []
    
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
        
    def add_tab(self, text:str='', command=None):
        """
            Append a new tab to the trough. Provide text that will be displayed on the tab and a
            command that will be called when the tab is clicked via the left mouse button.
        """
        if not text:
            titles = 'New Project'
            name = simpledialog.askstring(title=titles, prompt='Project Name:')
            messagebox.showinfo(
                title=titles, 
                message="Enter the project directory. This directory should contain the 'manage.py' file"
            )
            dir = filedialog.askdirectory(title=titles, mustexist=True)
            find_env = messagebox.askquestion(title=titles, message='Add a python environment path.')
        self.tabs.append(Tab(self, text, command))
        
    def on_trough_resize(self, event:tkinter.Event):
        """Writes the current height of the trough to the config file"""
        self.root.cfg.data['tabs']['trough_height'] = self.winfo_height()
        self.root.cfg.write()
        
    def on_tab_select(self, clicked_tab:Tab):
        """Deselects any tab that wasn't the last clicked tab"""
        for tab in self.tabs:
            if tab.selected:
                tab.deselect()

                # break because their should only be one tab active so
                # there is no need to re-iterate.
                break  
            
        clicked_tab.select()
