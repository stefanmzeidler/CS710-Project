import tkinter as tk
from tkinter import Label, Frame, Button
from PIL import Image, ImageTk

class GameUI:
    def __init__(self, image_dir="card_images", card_size=(100, 140)):
        self.root = tk.Tk()
        self.root.title("Sushi Go!")
        self.card_size = card_size
        self.image_dir = image_dir
        self.card_choice = None

        # Layout
        self.hand_frame = Frame(self.root)
        self.hand_frame.pack(pady=10)

        self.opponent_frame = Frame(self.root)
        self.opponent_frame.pack(pady=10)

        self.score_frame = Frame(self.root)
        self.score_frame.pack(pady=10)

        self.prompt_label = Label(self.root, text="Choose a card:")
        self.prompt_label.pack()

    def update_hand(self, hand, callback):
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        for card in hand:
            img = self.load_card_image(card.name)
            btn = Button(self.hand_frame, image=img, command=lambda c=card: callback(c))
            btn.image = img
            btn.pack(side="left", padx=5)

    def update_table_state(self, players, human_name):
        for widget in self.opponent_frame.winfo_children():
            widget.destroy()

        for player in players:
            label = tk.Label(self.opponent_frame, text=player.name, font=('Arial', 12, 'bold'))
            label.pack(anchor='w')

            card_row = tk.Frame(self.opponent_frame)
            card_row.pack(anchor='w', pady=2)

            for card in player.chosen_cards:
                try:
                    img = self.load_card_image(card.name)
                    lbl = tk.Label(card_row, image=img)
                    lbl.image = img
                    lbl.pack(side='left', padx=2)
                except FileNotFoundError:
                    lbl = tk.Label(card_row, text=card.name)
                    lbl.pack(side='left', padx=2)

    # def update_opponents(self, players, human_name):
    #     for widget in self.opponent_frame.winfo_children():
    #         widget.destroy()
    #     for player in players:
    #         if player.name != human_name:
    #             text = f"{player.name} played: {player.chosen_cards[-1] if player.chosen_cards else '—'}"
    #             Label(self.opponent_frame, text=text).pack()

    def update_scores(self, players):
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        for player in players:
            Label(self.score_frame, text=f"{player.name}: {player.score} pts").pack()

    def load_card_image(self, card_name):
        path = f"{self.image_dir}/{card_name}.png"
        img = Image.open(path).resize(self.card_size)
        return ImageTk.PhotoImage(img)

    def mainloop(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()
