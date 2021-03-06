import time
import turtle

from food import Food


# playsound('fail.wav')
# winsound.PlaySound('fail.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)


class Snake:
    starting_size = 3
    eating_radius = 20
    walls = 290

    def __init__(self):
        self.screen = self.init_screen()
        self.speed = 0.07
        self.score = 0
        with open('score.txt') as file:
            score = file.read()
            if score:
                self.high_score = int(score)
            else:
                self.high_score = 0
        self.moved = False
        self.snake = []
        self.food = Food()
        self.board = self.init_board()
        self.start()

    def init_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=600, height=600)
        self.screen.bgcolor("black")
        self.screen.title("Snake")
        self.screen.tracer(0)
        self.screen.listen()
        return self.screen

    def init_board(self):
        self.board = turtle.Turtle()
        self.board.clear()
        self.board.color("dim gray")
        self.board.penup()
        self.board.goto(-250, 250)
        self.board.ht()
        self.board.write(f'SCORE: {self.score} | Highest score {self.high_score}'.upper(), font=("Arial", 25, "normal"))
        return self.board

    def init_snake(self):
        starting_point = 0

        for index in range(Snake.starting_size):
            self.snake.append(turtle.Turtle("square"))
            self.snake[index].penup()
            self.snake[index].color("white")
            self.snake[index].setx(starting_point)
            starting_point -= 20

    def add_size(self):
        last = len(self.snake)
        self.snake.append(turtle.Turtle("square"))
        self.snake[last].penup()
        self.snake[last].color("white")
        self.snake[last].sety(self.snake[last - 1].ycor())
        self.snake[last].setx(self.snake[last - 1].xcor() - 20)
        new_speed = int(len(self.snake) / 5)
        if len(self.snake) % 5 == 0:
            self.speed_up()

    def speed_up(self):
        if self.speed > 0.04:
            self.speed -= 0.01

    def up(self):
        if self.head().heading() != 270 and not self.moved:
            self.moved = True
            self.head().setheading(90)

    def down(self):
        if self.head().heading() != 90 and not self.moved:
            self.moved = True
            self.head().setheading(270)

    def left(self):
        if self.head().heading() != 0 and not self.moved:
            self.moved = True
            self.head().setheading(180)

    def right(self):
        if self.head().heading() != 180 and not self.moved:
            self.moved = True
            self.head().setheading(0)

    def move(self):
        while True:
            time.sleep(self.speed)
            self.screen.update()
            for snake_part in range(len(self.snake) - 1, 0, -1):
                new_x = self.snake[snake_part - 1].xcor()
                new_y = self.snake[snake_part - 1].ycor()
                self.snake[snake_part].goto((new_x, new_y))

            self.screen.onkey(self.up, "w")
            self.screen.onkey(self.down, "s")
            self.screen.onkey(self.left, "a")
            self.screen.onkey(self.right, "d")

            self.head().forward(20)
            self.moved = False
            self.eat_food()
            if self.is_wall_or_tail():
                self.game_over()
                break

    def head(self):
        return self.snake[0]

    def tail(self):
        return self.snake[1:]

    def is_wall_or_tail(self):
        if self.head().xcor() > Snake.walls or self.head().xcor() < -Snake.walls or \
                self.head().ycor() > Snake.walls or self.head().ycor() < -Snake.walls:
            return True
        for segment in self.tail():
            if self.head().distance(segment) < 10:
                return True
        return False

    def eat_food(self):
        if -Snake.eating_radius < self.food.pos()[1] - self.head().pos()[1] <= Snake.eating_radius \
                and -Snake.eating_radius < self.food.pos()[0] - self.head().pos()[0] <= Snake.eating_radius:
            self.score += 1
            self.food.food.reset()
            self.food = Food()
            self.board.reset()
            self.board = self.init_board()
            self.add_size()
            self.eat_sound()  # Launch created thread

    def eat_sound(self):
        pass
        # winsound.PlaySound('eat.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)

    def start(self):
        self.init_screen()
        self.init_snake()
        self.move()
        self.screen.reset()

    def game_over(self):
        board = turtle.Turtle()
        board.color("white")
        board.penup()
        board.ht()
        if self.score > self.high_score:
            self.high_score = self.score
            with open('score.txt', mode='w') as file:
                file.write(f"{self.high_score}")
            board.write(f'New high score {self.high_score}', font=("Arial", 30, "normal"), align="center")
        else:
            board.write(f'Game Over', font=("Arial", 30, "normal"), align="center")
        time.sleep(1)
