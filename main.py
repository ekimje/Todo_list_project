from pathlib import Path
from storage import Todostorage
from models import TodoItem
from ui import TodowidgetUI
import tkinter as tk

class TodoWidgetApp:
    def __init__(self, root:tk.Tk, data_file:Path)->None:
        self.root = root
        self.storage = Todostorage(data_file)
        self.items:list[TodoItem] = self.storage.load()
        self.keep_window_bottom()
        
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
    
    def toggle_item(self,index:int)->None:
        self.items[index].done = not self.items[index].done
        self.storage.save(self.items)
        self.ui.render_items(self.items)
        
    def on_close(self)->None:
        self.storage.save(self.items)
        self.root.destroy()
        
    def keep_window_bottom(self):
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