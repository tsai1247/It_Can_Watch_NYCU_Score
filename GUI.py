#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
from time import sleep
import tkinter as tk
from It_Can_Watch_NYCU_Score import getScores
from os.path import isfile

def task():
    def retry():
        restart_btn.grid_forget()
        label.config(text='開始爬成績...\n')
        threading.Thread(target=task).start()

    data = getScores(label)
    if data is None:
        sleep(1)
        label.config(text=label.cget('text') + '\n請嘗試排除錯誤後重新執行此程式\n')
        restart_btn = tk.Button(window, text="重試", command=retry)
        restart_btn.grid(row=1, column=0, padx=5, pady=5)
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

def confirmed():
    open('account', 'w', encoding='utf-8').write(f'{acnt_var.get()}\n{pwd_var.get()}\n')
    window.destroy()

def on_closing():
    window.destroy()
    exit()

font_title = ('標楷體', 14, 'bold')
font_content = ('微軟正黑體', 12)

if not isfile('account') or len(open('account', 'r', encoding='utf-8').read()) == 0:
    window = tk.Tk()
    window.title('第一次使用')
    frame = tk.Frame(window)
    frame.grid(padx=8, pady=8)

    title = tk.Label(frame, text='第一次使用請先輸入帳號密碼', font=font_title, pady=5)
    title.grid(row=0, column=0, columnspan=2, sticky='w')

    account_label = tk.Label(frame, text='帳號：', font=font_content, pady=5)
    password_label = tk.Label(frame, text='密碼：', font=font_content, pady=5)
    account_label.grid(row=1, column=0)
    password_label.grid(row=2, column=0)

    acnt_var = tk.StringVar()
    account = tk.Entry(frame, textvariable=acnt_var, font=font_content)
    account.grid(row=1, column=1)
    pwd_var = tk.StringVar()
    password = tk.Entry(frame, textvariable=pwd_var, show='*', font=font_content)
    password.grid(row=2, column=1)
    
    confirm = tk.Button(frame, text='確認', command=confirmed, font=font_content, padx=15, pady=3)
    confirm.grid(row=3, column=0, columnspan=2)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

window = tk.Tk()
window.title('你的成績')
window.attributes('-topmost', True)
window.resizable(False, False)

label = tk.Label(window, text='開始爬成績...\n', font=font_title, justify='left')
label.grid(row=0, column=0, padx=5, pady=5)
threading.Thread(target=task).start()

window.mainloop()