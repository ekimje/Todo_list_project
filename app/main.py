from __future__ import annotations

import tkinter as tk
from pathlib import Path
from datetime import date, datetime, timedelta
from app.logic import filter_items_by_date,sort_items
from app.models import TodoItem
from app.storage import Todostorage
from app.ui import TodowidgetUI

class TodoWidgetApp:
    def __init__(self, root:tk.Tk, data_file:Path) -> None:
        self.root = root
        self.storage = Todostorage(data_file)
        self.items:list[TodoItem] = self.storage.load()
        self.current_date = date.today()
        self.on_prev_day = self.move_prev_day
        self.on_next_day = self.move_next_day
        self.keep_window_bottom()
        
        self.ui=TodowidgetUI(
            root = root,
            on_add = self.add_item,
            on_toggle = self.toggle_item,
            on_close = self.on_close,
            on_edit= self.edit_item,
            on_delete=self.delete_item,
            on_prev_day=self.on_prev_day,
            on_next_day=self.on_next_day,
        )  
        self.refresh_ui()  
        
    def add_item(self, text:str)->None:
        created_at = datetime.combine(self.current_date, datetime.now().time())
        self.items.append(TodoItem(text=text, created_at=created_at))
        self.storage.save(self.items)
        self.refresh_ui()
        
    def refresh_ui(self) -> None:
        sorted_items = sort_items(self.items)
        filtered_items = filter_items_by_date(sorted_items,self.current_date)
        self.ui.render_items(self.current_date, filtered_items)
    
    def toggle_item(self, item:TodoItem)->None:
        item.done = not item.done
        self.storage.save(self.items)
        self.refresh_ui()
    
    def edit_item(self, item:TodoItem, text:str) -> None:
        item.text = text
        self.storage.save(self.items)
        self.refresh_ui()
    
    def delete_item(self, item:TodoItem) -> None:
        if item in self.items:
            self.items.remove(item)
        self.storage.save(self.items)
        self.refresh_ui()
        
    def move_prev_day(self) -> None:
        self.current_date -= timedelta(days=1)
        self.refresh_ui()
        
    def move_next_day(self) -> None:
        self.current_date += timedelta(days=1)
        self.refresh_ui()
        
    def on_close(self)->None:
        self.storage.save(self.items)
        self.root.destroy()
        
    def keep_window_bottom(self) -> None:
        #최상위 창 속성 해제. 다른 창 뒤에 있도록 설정
        self.root.attributes("-topmost", False)
        self.root.after(0,self.root.lower) #창을 가장 뒤로 보내기
   
def main()->None:
    root = tk.Tk()
    root.geometry("320x420+100+100")
    data_file = Path("todo_data.json")
    app = TodoWidgetApp(root = root, data_file = data_file) 
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
    
if __name__ == "__main__":
    main()  