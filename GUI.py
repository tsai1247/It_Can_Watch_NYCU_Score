#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
from time import sleep
import tkinter as tk
from It_Can_Watch_NYCU_Score import getScores


def task():
    data = getScores(label)
    if data is None:
        sleep(1)
        label.config(text=label.cget('text') + '\n請嘗試排除錯誤後重新執行此程式\n')
        return

    titles, data = data
    sleep(0.2)

    label.grid_forget()
    
    canvas = tk.Canvas(window)
    canvas.grid(sticky='news')

    frame = tk.Frame(canvas)

    i, j = 0, 0
    max_width = 0
    for cnt in range(len(data)):
        semester = data[cnt]
        # title
        if cnt == 0 or titles[cnt] != titles[cnt-1]:
            i, j = i+1, 0
            d = tk.Label(frame, text=titles[cnt], font=font_title)
            d.grid(row=i, column = j, sticky='w')
            i, j = i+1, 0

        # field name
        for key in semester[0].keys():
            d = tk.Label(frame, text=key, font=font_title)
            d.grid(row=i, column = j)
            i, j = i, j+1

        # field value
        for subject in semester:
            i, j = i+1, 0
            for key, value in subject.items():
                d = tk.Label(frame, text=value, font=font_content)
                d.grid(row=i, column = j, sticky = 'w' if '名稱' in key else None)
                i, j = i, j+1
        i, j = i+1, 0
        d = tk.Label(frame, text=" ", font=font_title)
        d.grid(row=i, column = j, sticky='w')
        i, j = i+1, 0

    scrollbar=tk.Scrollbar(window, orient="vertical", width=15, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set) 
    scrollbar.grid(row=0, column=1, sticky='ns')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    canvas.config(width=frame.winfo_width(), height=min(frame.winfo_height(), 600))
    canvas.config(scrollregion=canvas.bbox("all"))

window = tk.Tk()
window.title('你的成績')
window.attributes('-topmost', True)
window.resizable(False, False)
font_title = ('標楷體', 14, 'bold')
font_content = ('微軟正黑體', 12)

label = tk.Label(window, text='開始爬成績...\n', font=font_title, justify='left')
label.grid(row=0, column=0, padx=5, pady=5)
threading.Thread(target=task).start()

window.mainloop()