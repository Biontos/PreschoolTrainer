import tkinter as tk
from tkinter import messagebox
import random

BG_MAIN = "#FFF7ED"
CARD_BG = "#FFFFFF"
ACCENT = "#F97316"
ACCENT_2 = "#FB923C"
TEXT = "#1F2937"
SUBTEXT = "#6B7280"
CORRECT = "#16A34A"
WRONG = "#DC2626"
BUTTONS = ["#FDE68A", "#BFDBFE", "#FBCFE8", "#C7D2FE"]

TASKS = [
    {"name": "яблоки", "emoji": "🍎"},
    {"name": "звёзды", "emoji": "⭐"},
    {"name": "мишки", "emoji": "🧸"},
    {"name": "машинки", "emoji": "🚗"},
    {"name": "шарики", "emoji": "🎈"},
    {"name": "котята", "emoji": "🐱"},
]


class RoundedLabel(tk.Label):
    pass


class PreschoolTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Детский тренажёр")
        self.root.geometry("980x720")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG_MAIN)

        self.total_rounds = 10
        self.score = 0
        self.lives = 3
        self.round_index = 0
        self.correct_answer = 0
        self.selected = False
        self.task = None

        self.build_ui()
        self.new_game()

    def build_ui(self):
        self.header = tk.Frame(self.root, bg=BG_MAIN)
        self.header.pack(fill="x", padx=24, pady=(20, 10))

        self.title_label = tk.Label(
            self.header,
            text="🌟 Весёлый тренажёр для дошкольников",
            font=("Arial", 24, "bold"),
            bg=BG_MAIN,
            fg=TEXT,
        )
        self.title_label.pack()

        self.stats_frame = tk.Frame(self.root, bg=BG_MAIN)
        self.stats_frame.pack(fill="x", padx=24, pady=10)

        self.score_card = self.make_stat_card(self.stats_frame, "Очки", "0")
        self.score_card.pack(side="left", expand=True, fill="x", padx=8)

        self.lives_card = self.make_stat_card(self.stats_frame, "Жизни", "❤❤❤")
        self.lives_card.pack(side="left", expand=True, fill="x", padx=8)

        self.round_card = self.make_stat_card(self.stats_frame, "Уровень", "1/10")
        self.round_card.pack(side="left", expand=True, fill="x", padx=8)

        self.main_card = tk.Frame(self.root, bg=CARD_BG, bd=0, highlightthickness=0)
        self.main_card.pack(fill="both", expand=True, padx=24, pady=14)

        self.question_label = tk.Label(
            self.main_card,
            text="Посчитай предметы",
            font=("Arial", 26, "bold"),
            bg=CARD_BG,
            fg=TEXT,
        )
        self.question_label.pack(pady=(25, 8))

        self.info_label = tk.Label(
            self.main_card,
            text="Посмотри на картинки и выбери правильное число",
            font=("Arial", 14),
            bg=CARD_BG,
            fg=SUBTEXT,
        )
        self.info_label.pack(pady=(0, 12))

        self.canvas = tk.Canvas(
            self.main_card,
            width=820,
            height=280,
            bg="#FFFDF8",
            highlightthickness=0,
        )
        self.canvas.pack(padx=30, pady=12)

        self.answer_frame = tk.Frame(self.main_card, bg=CARD_BG)
        self.answer_frame.pack(pady=18, fill="x", padx=120)
        self.answer_frame.grid_columnconfigure(0, weight=1, uniform="answers")
        self.answer_frame.grid_columnconfigure(1, weight=1, uniform="answers")

        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.answer_frame,
                text="1",
                font=("Arial", 22, "bold"),
                width=10,
                height=2,
                bd=0,
                relief="flat",
                cursor="hand2",
                activebackground=ACCENT_2,
                activeforeground="white",
                command=lambda idx=i: self.check_answer(self.answer_buttons[idx]["text"]),
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=16, pady=16, sticky="nsew", ipadx=10, ipady=10)
            self.answer_buttons.append(btn)

        self.result_label = tk.Label(
            self.main_card,
            text="",
            font=("Arial", 18, "bold"),
            bg=CARD_BG,
            fg=TEXT,
        )
        self.result_label.pack(pady=(5, 10))

        self.bottom_frame = tk.Frame(self.main_card, bg=CARD_BG)
        self.bottom_frame.pack(pady=(8, 24))

        self.restart_button = tk.Button(
            self.bottom_frame,
            text="Начать заново",
            font=("Arial", 14, "bold"),
            bg=ACCENT,
            fg="white",
            bd=0,
            relief="flat",
            padx=24,
            pady=12,
            cursor="hand2",
            activebackground=ACCENT_2,
            activeforeground="white",
            command=self.new_game,
        )
        self.restart_button.pack()

    def make_stat_card(self, parent, title, value):
        frame = tk.Frame(parent, bg=CARD_BG, padx=18, pady=16)
        title_label = tk.Label(frame, text=title, font=("Arial", 12), bg=CARD_BG, fg=SUBTEXT)
        title_label.pack(anchor="w")
        value_label = tk.Label(frame, text=value, font=("Arial", 22, "bold"), bg=CARD_BG, fg=TEXT)
        value_label.pack(anchor="w", pady=(6, 0))
        frame.value_label = value_label
        return frame

    def new_game(self):
        self.score = 0
        self.lives = 3
        self.round_index = 0
        self.update_stats()
        self.load_round()

    def update_stats(self):
        self.score_card.value_label.config(text=str(self.score))
        self.lives_card.value_label.config(text="❤" * self.lives)
        current_round = min(self.round_index + 1, self.total_rounds)
        self.round_card.value_label.config(text=f"{current_round}/{self.total_rounds}")

    def load_round(self):
        if self.round_index >= self.total_rounds or self.lives <= 0:
            self.show_final_screen()
            return

        self.selected = False
        self.result_label.config(text="", fg=TEXT)

        self.task = random.choice(TASKS)
        self.correct_answer = random.randint(1, 10)

        self.question_label.config(text=f"Посчитай: {self.task['name']}")
        self.info_label.config(text="Сколько предметов ты видишь на картинке?")

        self.draw_items(self.task["emoji"], self.correct_answer)
        self.prepare_options()
        self.update_stats()

    def draw_items(self, emoji, count):
        self.canvas.delete("all")
        self.canvas.create_rectangle(10, 10, 810, 270, outline="", fill="#FFFDF8")

        cols = 5
        spacing_x = 140
        spacing_y = 95
        start_x = 120
        start_y = 60

        for i in range(count):
            row = i // cols
            col = i % cols
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            self.canvas.create_text(x, y, text=emoji, font=("Arial", 42))

    def prepare_options(self):
        options = {self.correct_answer}
        while len(options) < 4:
            options.add(random.randint(1, 10))
        options = list(options)
        random.shuffle(options)

        for i, btn in enumerate(self.answer_buttons):
            btn.config(
                text=str(options[i]),
                bg=BUTTONS[i % len(BUTTONS)],
                fg=TEXT,
                state="normal",
            )

    def check_answer(self, answer):
        if self.selected:
            return
        self.selected = True

        answer = int(answer)
        for btn in self.answer_buttons:
            btn.config(state="disabled")

        if answer == self.correct_answer:
            self.score += 1
            self.result_label.config(text="Правильно! Молодец!", fg=CORRECT)
            for btn in self.answer_buttons:
                if int(btn["text"]) == self.correct_answer:
                    btn.config(bg="#BBF7D0")
        else:
            self.lives -= 1
            self.result_label.config(
                text=f"Почти! Правильный ответ: {self.correct_answer}",
                fg=WRONG,
            )
            for btn in self.answer_buttons:
                if int(btn["text"]) == answer:
                    btn.config(bg="#FECACA")
                if int(btn["text"]) == self.correct_answer:
                    btn.config(bg="#BBF7D0")

        self.update_stats()
        self.root.after(1200, self.next_round)

    def next_round(self):
        self.round_index += 1
        self.load_round()

    def show_final_screen(self):
        result = f"Игра окончена!\n\nТы набрал {self.score} из {self.total_rounds} очков"
        if self.score >= 8:
            result += "\n\nОтличный результат! 🏆"
        elif self.score >= 5:
            result += "\n\nХорошая работа! 🌟"
        else:
            result += "\n\nПопробуй ещё раз 🙂"

        retry = messagebox.askyesno("Результат", result + "\n\nСыграть ещё раз?")
        if retry:
            self.new_game()
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PreschoolTrainerApp(root)
    root.mainloop()
