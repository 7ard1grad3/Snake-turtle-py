from turtle import Turtle
from random import randint


class Food:
    def __init__(self):
        self.food = Turtle("turtle")
        self.food.reset()
        self.food.goto((randint(-280, 280), randint(-280, 280)))
        self.food.color("green")

    def pos(self):
        return self.food.pos()
