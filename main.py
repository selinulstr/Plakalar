from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

window = Tk()
window.title("Plaka Kodları")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

try:
    data = pandas.read_csv("data/ogrenilecek_plakalar.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/plakalar.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



def next_card():
    global current_card, delay
    window.after_cancel(delay)
    current_card = choice(to_learn)
    kod = current_card["kod"]
    canvas.itemconfig(current_side, image=card_front)
    canvas.itemconfig(card_word, text=kod, fill="black")
    canvas.itemconfig(card_title, text="Plaka Kodu", fill="black")
    delay = window.after(4000, flip_card)


def flip_card():
    canvas.itemconfig(current_side, image=card_back)
    il = current_card["il"]
    canvas.itemconfig(card_word, text=il, fill="white")
    canvas.itemconfig(card_title, text="İl", fill="white")


def is_known():
    to_learn.remove(current_card)
    data2 = pandas.DataFrame(to_learn)
    data2.to_csv("data/ogrenilecek_plakalar.csv", index=False)
    next_card()


delay = window.after(3000, flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
current_side = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"), text="")
card_word = canvas.create_text(400, 253, font=("Ariel", 60, "bold"), text="")
canvas.grid(row=0, column=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)


next_card()


window.mainloop()
