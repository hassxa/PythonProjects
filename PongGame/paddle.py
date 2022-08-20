from turtle import Turtle

STRETCH_WID = 5
STRETCH_LEN = 1
SPEED = 20


class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=STRETCH_WID, stretch_len=STRETCH_LEN)
        self.penup()
        self.goto(position)

    def move_up(self):
        y_cor = self.ycor() + SPEED
        self.goto(self.xcor(), y_cor)

    def move_down(self):
        y_cor = self.ycor() - SPEED
        self.goto(self.xcor(), y_cor)
