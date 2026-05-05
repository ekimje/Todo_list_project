from __future__ import annotations

import tkinter as tk
from datetime import date
from tkinter import font, simpledialog
from typing import Callable
from models import TodoItem

class TodowidgetUI:
    def __init__(self, root:tk.Tk, on_add:Callable[[str],None], on_toggle:Callable[[TodoItem],None], on_close:Callable[[],None])->None:
        self.root = root
        self.on_add = on_add
        self.on_toggle = on_toggle
        self.on_close = on_close
        
        self._drag_start_x = 0
        self._drag_start_y=0
        self.item_vars:list[tk.BooleanVar] = []
        
        self._build_layout()
        self._build_drag_events()
    
    def _build_layout(self) ->None:
        self.root.title("Todo List")
        self.root.attributes("-topmost",True)
        self.root.attributes("-alpha",0.9)
        self.root.overrideredirect(True)
        self.root.configure(bg="#0f0f0f")
        
        self.container = tk.Frame(self.root, bg="#141414",bd=1,pady=4,relief="solid")
        self.container.pack(fill="both",expand=True,padx=4,pady=4)
        
        self.header=tk.Frame(self.container,bg="#1d1d1d")
        self.header.pack(fill="x")
        
        self.title_label=tk.Label(
            self.header,
            text = "Todo list",
            bg="#1d1d1d",
            fg="#f3f3f3",
            font=("Arial",10,"bold"),
            padx=8,
            pady=6,
        )
        
        self.title_label.pack(side="left")
        
        self.close_button = tk.Button(
            self.header,
            text="X",
            command=self.on_close,
            bg="#1d1d1d",
            fg="#f3f3f3",
            bd=0,
            padx=10,
            pady=4,
            activebackground="#313131",
            activeforeground="#ffffff",
        )
        self.close_button.pack(side="right")
        
        self.list_frame = tk.Frame(self.container, bg="#141414")
        self.list_frame.pack(fill="both",expand=True,padx=10,pady=(8,6))
        
        self.bottom_bar=tk.Frame(self.container,bg="#141414")
        self.bottom_bar.pack(fill="x",padx=10,pady=(0,0))

        self.add_button = tk.Button(
            self.bottom_bar,
            text = "+",
            command = self._submit_new_todo,
            bg="#272727",
            fg="#f0f0f0",
            bd=0,
            padx=10,
            pady=6,
            activebackground="#3a3a3a",
            activeforeground="#ffffff",
        )
        self.add_button.pack(fill="x")
        
    def _build_drag_events(self)->None:
        for widget in (self.header,self.title_label):
            widget.bind("<ButtonPress-1>",self._start_drag)
            widget.bind("<B1-Motion>",self._do_drag)
    
    def _start_drag(self,event:tk.Event)->None:
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _do_drag(self,event)->None:
        x_pos = self.root.winfo_x() +(event.x - self._drag_start_x)
        y_pos = self.root.winfo_y() +(event.y - self._drag_start_y)
        self.root.geometry(f"+{x_pos}+{y_pos}")
        
    def _submit_new_todo(self)->None:
        text = simpledialog.askstring("일정 추가","할 일을 입력하세요 : ",parent=self.root)
        if not text:
            return
        trimmed = text.strip()
        if not trimmed:
            return
        self.on_add(trimmed)
        
    def render_items(self, grouped_items:dict[date,list[TodoItem]])->None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        self.item_vars=[]
        
        for item_date, date_items in grouped_items.items():
            date_label = tk.Label(
                self.list_frame,
                text=item_date.isoformat(),
                bg="#141414",
                fg="#9a9a9a",
                anchor="w",
                font=("Arial",9,"bold"),
            )
            date_label.pack(fill="x",pady=(8,2))
            
            for item in date_items:
                row = tk.Frame(self.list_frame, bg="#141414")
                row.pack(fill="x", pady=2)

                var = tk.BooleanVar(value=item.done)
                self.item_vars.append(var)

                checkbox = tk.Checkbutton(
                    row,
                    variable=var,
                    command=lambda item=item: self.on_toggle(item),
                    bg="#141414",
                    fg="#aeaeae",
                    selectcolor="#222222",
                    activebackground="#141414",
                )
                checkbox.pack(side="left")

                style = font.Font(family="Arial", size=10)
                fg_color = "#6f6f6f" if item.done else "#f0f0f0"
                if item.done:
                    style.configure(overstrike=1)

                label = tk.Label(
                    row,
                    text=item.text,
                    bg="#141414",
                    fg=fg_color,
                    font=style,
                    anchor="w",
                )
                label.pack(side="left", fill="x", expand=True)
