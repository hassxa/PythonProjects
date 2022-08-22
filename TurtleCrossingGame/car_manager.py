from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:

    def __init__(self):
        self.cars = []
        self.speed = STARTING_MOVE_DISTANCE
        self.generate_car()

    def generate_car(self):
        car = Turtle()
        car.shape("square")
        car.shapesize(stretch_wid=1, stretch_len=2)
        car.color(random.choice(COLORS))
        car.penup()
        car.setheading(180)
        car.goto(x=320, y=random.randint(-250, 250))
        self.cars.append(car)
        self.move()

    def move(self):
        for c in self.cars:
            c.forward(self.speed)

    def level_up(self):
        self.speed += MOVE_INCREMENT
