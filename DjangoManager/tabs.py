import logging
import tkinter
from tkinter import ttk


log = logging.getLogger(__name__)


class Tab(ttk.Frame):

    def __init__(self, master, text:str):
        super().__init__(master, style='Tab.TFrame')
        self.pack(side='left', fill='y')
        
        # tab label
        self.text = ttk.Label(self, text=text, style='TabText.TLabel')
        self.text.pack(side='left', fill='both', expand=True)
        self.text.bind('<Button-1>', self.drag)
        
        # close button
        self.btn = ttk.Button(self, text='X', style='TabClose.TButton', width=5, command=self._destroy)
        self.btn.pack(side='right', fill='y')
        
    def _calculate_start_pos(self):
        length = 0
        for tab in self.master.tabs:
            length += tab.winfo_width()
            
    def _destroy(self):
        self.destroy()
        self.master.tabs.remove(self)
     
    def _snap_to_pos(self, event:tkinter.Event):
        self.pack(side='left', fill='y')
        
    def _reserve_space(self) -> ttk.Frame:
        
        try:
            before = self.master.tabs[self.master.tabs.index(self) ]
        except IndexError:
            before = None
        
        reserve_block = ttk.Frame(
            self.master,
            width=self.winfo_width(),
            style='TabReserved.TFrame'
        )
        reserve_block.pack(side='left', fill='y', before=before)
        return reserve_block
        

    def drag(self, event:tkinter.Event) -> None:
        reserved = self._reserve_space()
        self.tkraise()
        selfx = self.winfo_x() - event.x_root
        trough_height = self.master.winfo_height() - 3
        
        def finish(event:tkinter.Event) -> None:
            reserved.destroy()
            self._snap_to_pos(event)
        
        def move(event:tkinter.Event) -> None:
            newx = event.x_root + selfx
            if not (newx >= self.master.winfo_width() - self.winfo_width() or newx < 0):
                self.place(x=newx, h=trough_height)
    
            # calculate position to snap to
            self.master.update()

        self.text.bind('<B1-Motion>', move)
        self.text.bind('<ButtonRelease-1>', finish)
        move(event)

        


class TabManager(ttk.Frame):
    
    tabs: list[Tab] = []
    
    def __init__(self, root):
        super().__init__(root.window, height=25, style='TabTrough.TFrame')
        self.pack_propagate(False)
        self.pack(side='top', fill='x')
        
        ttk.Separator(self, orient='horizontal').pack(side='bottom', fill='x', pady=(1,0))
        
        self.add_tab(text='This is a tab')
        self.add_tab(text='this is another tab')
        self.add_tab(text='third tab here')
        
        
    def add_tab(self, text:str):
        self.tabs.append(Tab(self, text))
        
    
    def remove_tab(self):
        pass
        