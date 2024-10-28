import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class EmotionDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Diary")

    def main_page(self):
        self.clear_widgets()

        tk.Label(self.root, text="Emotion Diary", font=("Helvetica", 18)).pack(pady=10)

        # 일기 추가 버튼
        tk.Button(self.root, text="Add Diary Entry", command=self.open_diary_page).pack()

        # 년, 월 선택
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        # 화살표 버튼과 날짜 라벨
        navigation_frame = tk.Frame(self.root)
        navigation_frame.pack(pady=10)

        tk.Button(navigation_frame, text="<", command=self.previous_month).grid(row=0, column=0)
        self.date_label = tk.Label(navigation_frame, text="")  # 여기에서 date_label을 먼저 정의
        self.date_label.grid(row=0, column=1)
        tk.Button(navigation_frame, text=">", command=self.next_month).grid(row=0, column=2)

        self.update_date_label()  # 그 후에 update_date_label 호출

        # 일기 목록 리스트
        self.diary_listbox = tk.Listbox(self.root, width=50)
        self.diary_listbox.pack(pady=10)
        self.diary_listbox.bind("<Double-1>", self.open_diary_page)  # 더블 클릭으로 일기 열기

        self.load_diary_list()

    def open_diary_page(self, event=None):
        self.clear_widgets()

        # 일기 작성 공간
        tk.Label(self.root, text="Write your diary entry:", font=("Helvetica", 14)).pack(pady=10)
        self.diary_text = tk.Text(self.root, height=10, width=50)
        self.diary_text.pack(pady=10)

        # AI 코멘트 생성 버튼
        tk.Button(self.root, text="Generate AI Comment", command=self.generate_comment).pack(pady=5)

        # AI 코멘트 표시 공간
        self.comment_label = tk.Label(self.root, text="AI Comment will appear here", wraplength=400)
        self.comment_label.pack(pady=10)

        # 뒤로가기 버튼
        tk.Button(self.root, text="Back to Main", command=self.main_page).pack(pady=5)

    def generate_comment(self):
        # AI 코멘트 생성 예시 (API 연동 시 변경 가능)
        user_diary = self.diary_text.get("1.0", "end-1c")
        if user_diary.strip():
            # AI 모델에 연결 가능 시 API 호출
            ai_comment = "This is a placeholder comment. 실제 AI 코멘트를 여기 표시할 수 있습니다."
            self.comment_label.config(text=ai_comment)
        else:
            messagebox.showinfo("Error", "Please write something in the diary entry.")

    def load_diary_list(self):
        # 해당 월의 일기 목록을 불러오는 예시 (임시 데이터 사용)
        self.diary_listbox.delete(0, tk.END)
        # 실제 데이터베이스 연동 시 특정 년, 월의 일기 항목을 불러와서 추가 가능
        example_entries = ["Sample Entry 1", "Sample Entry 2", "Sample Entry 3"]
        for entry in example_entries:
            self.diary_listbox.insert(tk.END, entry)

    def update_date_label(self):
        self.date_label.config(text=f"{self.current_year}년 {self.current_month}월")

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_date_label()
        self.load_diary_list()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_date_label()
        self.load_diary_list()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# 프로그램 실행
root = tk.Tk()
app = EmotionDiaryApp(root)
root.mainloop()