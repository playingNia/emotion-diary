from color import BLACK, SHADOW, WHITE, GRAY, BLUE, RED
import diary_manager

import tkinter as tk
from tkinter import messagebox
import openai
from datetime import datetime
import os

class EmotionDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Diary")
        self.root.geometry("400x750+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg=WHITE)

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.date = f"{self.current_year}.{self.current_month}.{datetime.now().day}"

    def load_api_key_page(self):
        self.clear_widgets()

        frame = tk.Frame(root, bg=WHITE)
        frame.pack(expand=True, anchor="center")

        label = tk.Label(frame, text="Open AI API key를 입력하세요.", bg=WHITE, fg=BLACK)
        label.pack()

        entry = tk.Entry(frame, width=34, fg=BLACK)
        entry.pack(pady=10)

        btn = tk.Button(frame, text="완료", bg=BLUE, fg=WHITE, width=30, height=2, relief="flat", command=lambda: self.submit_api_key(entry.get()))
        btn.pack()

    def load_main_page(self):
        self.clear_widgets()

        title_frame = tk.Frame(self.root, bg=WHITE)
        title_frame.pack(fill='x')

        title_label = tk.Label(title_frame, text="Emotion Diary", bg=WHITE, fg=BLACK, font=("Helvetica", 12))
        title_label.pack(side="left", anchor='w', fill='y', expand=True, padx=10, pady=10)

        date = f"{datetime.now().year}.{datetime.now().month}.{datetime.now().day}"
        add_diary_btn = tk.Button(title_frame, text='+', bg=BLUE, fg=WHITE, relief="flat", padx=4, command=lambda : self.open_diary_page(date))
        add_diary_btn.pack(side="right", anchor='e', expand=True, padx=10)

        shadow_frame = tk.Frame(self.root, height=1, bg=SHADOW)
        shadow_frame.pack(fill='x')

        calendar_frame = tk.Frame(self.root, bg=WHITE)
        calendar_frame.pack(pady=(20, 0))

        previous_month_btn = tk.Button(calendar_frame, text='<', bg=WHITE, fg=BLACK, relief="flat", font=("Helvetica", 10), command=self.previous_month)
        previous_month_btn.grid(row=0, column=0)
        self.date_label = tk.Label(calendar_frame, text="", bg=WHITE, fg=BLACK, font=("Helvetica", 10))
        self.date_label.grid(row=0, column=1)
        next_month_btn = tk.Button(calendar_frame, text='>', bg=WHITE, fg=BLACK, relief="flat", font=("Helvetica", 10), command=self.next_month)
        next_month_btn.grid(row=0, column=2)

        self.update_date_label()

        self.diary_list_frame = tk.Frame(self.root, bg=WHITE)
        self.diary_list_frame.pack(fill='x', pady=(20, 20), padx=10)

        self.add_diary_element(self.date)
        self.add_diary_element(self.date)
        self.add_diary_element(self.date)
        self.add_diary_element(self.date)
        self.add_diary_element(self.date)
        self.add_diary_element(self.date)

        # self.diary_listbox = tk.Listbox(self.root, width=50)
        # self.diary_listbox.pack(pady=10)
        # self.diary_listbox.bind("<Double-1>", self.open_diary_page)  # 더블 클릭으로 일기 열기

    def open_diary_page(self, date):
        self.clear_widgets()
        self.date = date

        diary_data = diary_manager.get_diary(self.date)

        title_frame = tk.Frame(self.root, bg=WHITE)
        title_frame.pack(fill='x')

        back_button = tk.Button(title_frame, text='<', relief="flat", bg=WHITE, fg=BLACK, font=("Helvetica", 12), command=self.load_main_page)
        back_button.pack(side="left", anchor='w', expand=True, padx=10)

        title_label = tk.Label(title_frame, text="", bg=WHITE, font=("Helvetica", 12))
        title_label.pack(side="left", anchor='w', fill='y', expand=True, padx=10, pady=10)

        title_right_frame = tk.Frame(title_frame, bg=WHITE)
        title_right_frame.pack(side="right", anchor='e', expand=True, padx=10)

        remove_diary_btn = tk.Button(title_right_frame, text='❌', bg=RED, fg=WHITE, relief="flat", padx=1, command=self.open_diary_page)
        remove_diary_btn.pack(side="left", padx=10)

        add_diary_btn = tk.Button(title_right_frame, text='✔', bg=BLUE, fg=WHITE, relief="flat", command=self.save_diary)
        add_diary_btn.pack(side="left")

        shadow_frame = tk.Frame(self.root, height=1, bg=SHADOW)
        shadow_frame.pack(fill='x')

        emotion_diary_label = tk.Label(self.root, text="감정 일기", bg=WHITE, fg=BLACK, font=("Helvetica", 10))
        emotion_diary_label.pack(anchor='w', padx=10, pady=(20, 0))

        diary_input_frame = tk.Frame(self.root, background=BLUE, padx=2, pady=2)
        diary_input_frame.pack(fill='x', padx=10, pady=(10, 0))

        self.diary_input = tk.Text(diary_input_frame, height=20, relief="flat", bg=WHITE, fg=BLACK, font=("Helvetica", 10))
        self.diary_input.pack()

        self.diary_input.delete("1.0", "end")
        self.diary_input.insert("1.0", diary_data[0])

        ais_reply_frame = tk.Frame(bg=WHITE)
        ais_reply_frame.pack(fill='x', padx=10, pady=(20, 0))

        ais_reply_label = tk.Label(ais_reply_frame, text="에이아의 답글", bg=WHITE, fg=BLACK, font=("Helvetica", 10))
        ais_reply_label.pack(side="left")

        generate_ais_reply_btn = tk.Button(ais_reply_frame, text='에이아의 답글 기다리기', bg=BLUE, fg=WHITE, relief="flat", font=("Helvetica", 10), command=self.generate_comment)
        generate_ais_reply_btn.pack(side="right")

        ais_input_frame = tk.Frame(self.root, background=BLUE, padx=2, pady=2)
        ais_input_frame.pack(fill='x', padx=10, pady=10)

        self.ais_input = tk.Text(ais_input_frame, height=10, relief="flat", bg=WHITE, fg=BLACK, font=("Helvetica", 10))
        self.ais_input.pack()

        self.ais_input.config(state="normal")
        self.ais_input.delete("1.0", "end")
        self.ais_input.insert("1.0", diary_data[1])
        self.ais_input.config(state="disabled")

    def submit_api_key(self, key):
        if key == "":
            return

        with open("api-key.txt", 'w') as file:
            file.write(key)

        self.load_main_page()

    def update_date_label(self):
        self.date_label.config(text=f"{self.current_year}년 {self.current_month}월")

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_date_label()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_date_label()

    def add_diary_element(self, date):
        shadow_frame = tk.Frame(self.diary_list_frame, bg=SHADOW)
        shadow_frame.pack(fill='x', pady=(0, 10))

        frame = tk.Frame(shadow_frame, bg=WHITE)
        frame.pack(fill='x', padx=(0, 2), pady=(0, 2))

        line = tk.Frame(frame, width=7, bg=BLUE)
        line.pack(side="left", fill='y')

        content_frame = tk.Frame(frame, bg="white")
        content_frame.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(5, 5))

        date_label = tk.Label(content_frame, text=date, bg=WHITE, fg=BLACK, font=("Helvetica", 10))
        date_label.pack(anchor='w')

        content_label = tk.Label(content_frame, text=diary_manager.get_diary(date)[0][:20], bg=WHITE, fg=BLACK, font=("Helvetica", 8))
        content_label.pack(anchor='w')


    def save_diary(self):
        diary_manager.set_diary(self.date, self.diary_input.get("1.0", "end-1c"), self.ais_input.get("1.0", "end-1c"))

    def generate_comment(self):
        with open("api-key.txt", "r") as file:
            api_key = file.read()
        openai.api_key = api_key

        diary_content = self.diary_input.get("1.0", "end-1c")
        question = f"""
                    \"{diary_content}\"
                    """

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "유저가 작성한 감정 일기를 보고, 공감과 코멘트를 남겨 줘."},
                      {"role": "user", "content": question}],
        )

        self.ais_input.config(state="normal")
        self.ais_input.delete("1.0", "end")
        self.ais_input.insert("1.0", response.choices[0]["message"]["content"])
        self.ais_input.config(state="disabled")
        diary_manager.set_diary(self.date, self.diary_input.get("1.0", "end-1c"), self.ais_input.get("1.0", "end-1c"))

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# 프로그램 실행
root = tk.Tk()
app = EmotionDiaryApp(root)
if not os.path.exists("api-key.txt"): app.load_api_key_page()
else: app.load_main_page()

root.protocol("WM_DELETE_WINDOW", lambda: diary_manager.save_diary())
root.mainloop()

