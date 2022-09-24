from tkinter import *
import requests


def get_quote():
    response = requests.get(url="https://api.whatdoestrumpthink.com/api/v1/quotes/random/")
    response.raise_for_status()
    data = response.json()
    quote = data["message"]
    canvas.itemconfig(canvas_text, text=quote)


window = Tk()
window.title("Mr. Trump says...")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
background_image = PhotoImage(file="background.png")
canvas_image = canvas.create_image(150, 207, image=background_image)
canvas_text = canvas.create_text(150, 207, text="Donald Trump Quote Goes HERE",
                                 width=300, font=("Courier", 18, "bold"))
canvas.grid(row=0, column=0)

trump_image = PhotoImage(file="trump.png")
button = Button(image=trump_image, highlightthickness=0, command=get_quote)
button.grid(row=1, column=0)


window.mainloop()
