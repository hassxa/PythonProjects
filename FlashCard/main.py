from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

# Import data file
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    data_words = original_data.to_dict(orient="records")
else:
    data_words = data.to_dict(orient="records")


# Press button function
def press_button():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_words)
    french_word = current_card["French"]
    canvas.itemconfigure(canvas_title, text="French", fill="black")
    canvas.itemconfigure(canvas_word, text=french_word, fill="black")
    canvas.itemconfigure(canvas_image, image=card_front_img)
    flip_timer = window.after(3000, func=show_translation)

    words_to_learn = pd.DataFrame(data_words)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)


def press_button_right():
    press_button()
    data_words.remove(current_card)


def show_translation():
    english_word = current_card["English"]
    canvas.itemconfigure(canvas_title, text="English", fill="white")
    canvas.itemconfigure(canvas_word, text=english_word, fill="white")
    canvas.itemconfigure(canvas_image, image=card_back_img)


# Window
window = Tk()
window.title("Flashy")
window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=show_translation)

# Canvas
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=wrong_img, highlightthickness=0, command=press_button)
button_wrong.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
button_right = Button(image=right_img, highlightthickness=0, command=press_button_right)
button_right.grid(row=1, column=1)

press_button_right()

window.mainloop()
