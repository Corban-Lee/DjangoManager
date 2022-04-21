import tkinter
from tabs import TabManager


__version__ = '0.0.0'
__author__ = 'Corban-Lee'


class Root:
    
    window = tkinter.Tk()
    tabs = TabManager(window)
    
    def __init__(self):
        self.window.protocol('WM_DELETE_WINDOW', self.on_exit)
    
    def run(self) -> None:
        self.window.mainloop()
        
    def on_exit(self) -> SystemExit:
        self.window.destroy()
        raise SystemExit
        
        
if __name__ == '__main__':
    Root().run()
    