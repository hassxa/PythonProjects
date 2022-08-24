import turtle
import pandas as pd

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

data = pd.read_csv("50_states.csv")
states = data["state"].to_list()

end_of_game = False
correct_guesses = []
score = 0
while not end_of_game:
    answer_state = screen.textinput(title=f"{score}/{len(states)} States Correct",
                                    prompt="What's another state's name?").title()
    if answer_state in states:
        state_data = data[data.state == answer_state]
        x_cor = state_data["x"]
        y_cor = state_data["y"]
        writer.goto(x=int(x_cor), y=int(y_cor))
        writer.write(answer_state, align="center", font=("Courier", 8, "normal"))
        correct_guesses.append(answer_state)
        score += 1

    if len(states) == len(correct_guesses) or answer_state == "Exit":
        end_of_game = True

with open("states_to_learn.csv", mode='w') as file:
    for state in states:
        if state not in correct_guesses:
            file.write(state + "\n")

turtle.mainloop()
