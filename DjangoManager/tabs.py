from fileinput import close
import logging
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk


log = logging.getLogger(__name__)


IMAGES_DIR = 'DjangoManager/images'


class Tab(ttk.Frame):
    
    selected: bool = False

    def __init__(self, master, text:str):
        super().__init__(master, style=f'Tab.TFrame')
        self.bind('<Button-1>', self.drag)
        
        self.text = ttk.Label(self, text=text, style=f'TabText.TLabel')
        self.text.pack(side='left', fill='both', expand=True, padx=15, pady=1)
        self.text.bind('<Button-1>', self.drag)
        
        # get 'x' image for close button
        img = Image.open(f'{IMAGES_DIR}/tab_close_dark.png')
        img = img.resize((15,15), Image.ANTIALIAS)
        close_btn_img = ImageTk.PhotoImage(img)
        
        self.close_btn = ttk.Button(self, image=close_btn_img, style='TabBtn.TLabel', command=self._destroy)
        self.close_btn.image = close_btn_img  # tk is dumb and requires an attribute of the Image obj. Attr name doesnt matter.
        self.close_btn.pack(side='right', fill='y', padx=(0, 1), pady=1)

        # reserves a space when moving the tab
        self.reserved_space = ttk.Frame(self.master, style='TabReserved.TFrame')
        
        self.pack(side='left', fill='y')
        
    def select(self):
        assert not self.selected
        self.selected = True
        
        self.config(style='SelectedTab.TFrame')
        self.text.config(style='SelectedTabText.TLabel')
        self.close_btn.config(style='SelectedTabBtn.TLabel')
    
    def deselect(self):
        assert self.selected
        self.selected = False
        
        self.config(style='Tab.TFrame')
        self.text.config(style='TabText.TLabel')
        self.close_btn.config(style='TabBtn.TLabel')
            
    def _destroy(self):
        self.destroy()
        self.master.tabs.remove(self)
     
    def _snap_to_pos(self, event:tkinter.Event):
        self.pack(side='left', fill='y')

    def drag(self, event:tkinter.Event) -> None:
        """Allows the user to drag the tab"""
        
        self.master.select_tab(self)
        
        # create reserved space for the widget
        self.reserved_space.config(width=self.winfo_width())
        self.reserved_space.pack(side='left', fill='y', before=self)
        
        # if the tab isn't raised it can appear below other tabs and reserved space
        self.tkraise()
        
        original_x = self.winfo_x()
        current_x = original_x - event.x_root
        trough_height = self.master.winfo_height() - 2  # accounts for margin
        
        def release(event:tkinter.Event) -> None:
            """Left mouse button is released"""
            
            # 'x' coordinate, used to determine where to put the widget when dropped
            x: int = int(self.winfo_x() + (self.winfo_width() / 3))

            # create a list of everything on the tab trough excluding self
            items = self.master.tabs.copy()
            items.append(self.reserved_space)
            items.remove(self)

            
            for item in items:
                
                # is self overlapping item?
                tab_x = item.winfo_x()
                if x in range(tab_x, tab_x + item.winfo_width()):
                    break
                
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
            
            # prevent tab going past the trough border
            if not (new_x >= self.master.winfo_width() - self.winfo_width() or new_x < 0):
                self.place(x=new_x, h=trough_height)
    
            # TODO: did this to reduce fps lag. Don't know if it actually works. Test it?
            self.update()

        event.widget.bind('<B1-Motion>', move)
        event.widget.bind('<ButtonRelease-1>', release)
        move(event)

        


class TabManager(ttk.Frame):
    
    tabs: list[Tab] = []
    
    def __init__(self, root):
        super().__init__(root.window, height=25, style='TabTrough.TFrame')
        self.pack_propagate(False)
        self.pack(side='top', fill='x')
        
        ttk.Separator(self, orient='horizontal').pack(side='bottom', fill='x')
        
    def add_tab(self, text:str):
        self.tabs.append(Tab(self, text))
        
    def select_tab(self, tab_to_select:Tab):
        for tab in self.tabs:
            if tab.selected:
                tab.deselect()
                break
            
        tab_to_select.select()
        print('new tab selected')
    
    def remove_tab(self):
        pass
        