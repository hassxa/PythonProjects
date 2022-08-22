import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.title("Turtle Crossing Game")
screen.tracer(0)

player = Player()
car = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(fun=player.move, key="Up")

counter = 0
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car.move()

    if counter % 6 == 0:
        car.generate_car()

    for element in car.cars:
        if player.distance(element) < 20:
            scoreboard.game_over()
            game_is_on = False

    if player.reached_top():
        car.level_up()
        scoreboard.increase_level()

    counter += 1

screen.exitonclick()
