from pathlib import Path
import tkinter as tk

class TodoWidgetApp:
    def __init__(self, root:tk.Tk, data_file:Path)->None:
        self.root = root
        self.storage = Todostroage(data_file)
        self.items:list[TodoItem] = self.storage.load()
        
        self.ui=TodowidgetUI(
            root = root,
            on_add = self.add_item,
            on_toggle = self.toggle_item,
            on_close = self.on_close,
        )
        self.ui.render_items(self.items)
        
    def add_item(self, text:str)->None:
        self.items.append(TodoItem(text=text,done=False))
        self.storage.save(self.items)
        self.ui.render_items(self.items)