import time
from turtle import Turtle, Screen
from datetime import datetime
import random


class SpaceInvaders:

    def __init__(self):
        self.screen = Screen()
        self.screen.setup(1100, 600)
        self.screen.bgpic('space.gif')
        self.screen.title("Space Invaders")
        self.screen.addshape('ship.gif')
        self.screen.addshape('inv.gif')
        self.drawing_t = Turtle()

        self.invader = None
        self.invaders = None
        self.invaders_time_stamp = datetime.now()
        self.invaders_move_x = 18
        self.invader_fire = None
        self.invader_fires = []
        self.invaders_shoot_time_stamp = datetime.now()

        self.ship = Turtle()
        self.ship_fire = None
        self.fire_time_stamp = datetime.now()

        self.limits_x = 530
        self.limits_y = 280
        self.lives = 3
        self.difficulty = 30
        self.level = 1

        self.score = 0
        try:
            with open("high_score.txt") as file:
                contents = file.read()
                self.high_score = int(contents)
        except FileNotFoundError:
            self.high_score = 0

        self.screen.listen()
        self.screen.onkeypress(lambda: self.ship_move("to_the_left"), "Left")
        self.screen.onkeypress(lambda: self.ship_move("to_the_right"), "Right")
        self.screen.onkeypress(self.ship_init_fire, 'Control_L')

        self.screen.tracer(0)
        self.draw_frame_with_score_and_lives()
        self.ship_setting()
        self.invaders_setting()

        self.game()

    # --- SECTION FRAME AND TEXT ---
    def draw_frame_with_score_and_lives(self):
        # high score dealing
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", mode="w") as file:
                file.write(f"{self.high_score}")

        # writing on screen
        self.drawing_t.clear()
        self.drawing_t.color("white")
        self.drawing_t.hideturtle()
        self.drawing_t.penup()
        self.drawing_t.goto(self.limits_x, self.limits_y)
        self.drawing_t.pendown()
        for _ in range(2):
            self.drawing_t.right(90)
            self.drawing_t.forward(2 * self.limits_y)
            self.drawing_t.right(90)
            self.drawing_t.forward(2 * self.limits_x)
        self.drawing_t.penup()
        self.drawing_t.goto(self.limits_x, self.limits_y)
        font = ("Verdana", 10, "italic")
        self.drawing_t.write(f"Score: {self.score}      Lives: {self.lives}", align="right",font=font)
        self.drawing_t.goto(-self.limits_x, self.limits_y)
        self.drawing_t.write(f"Highest Score: {self.high_score}", align="left", font=font)
        self.drawing_t.goto(0, self.limits_y)
        self.drawing_t.write(f"Level: {self.level}", align="center", font = ("Verdana", 12, "bold"))

    def draw_game_over(self):
        self.drawing_t.goto(0, -20)
        self.drawing_t.write(f"   Game Over.\nYour score: {self.score}",
                             align="center",
                             font=("Verdana", 40, "bold"))

    def draw_level_up(self):
        self.drawing_t.goto(0, -20)
        self.drawing_t.write(f"Level up.\n +1 life", align="center", font=("Verdana", 30, "bold"))

    # --- SECTION SHIP ---
    def ship_setting(self):
        self.ship.color("white")
        self.ship.penup()
        self.ship.shape("ship.gif")
        self.ship.setheading(90)
        self.ship.shapesize(2, 1)
        self.ship.goto((0, -250))

    def ship_move(self, direction):
        new_x = self.ship.xcor()
        if direction == "to_the_left" and self.ship.xcor() > -self.limits_x + 60:
            new_x -= 12
        elif direction == "to_the_right" and self.ship.xcor() < self.limits_x - 60:
            new_x += 12
        y = self.ship.ycor()
        self.ship.goto(new_x, y)

    # --- SECTION INVADERS ---
    def invaders_setting(self):
        x_cors = [pos_x for pos_x in range(-100, 100, 50)]
        y_cors = [pos_y for pos_y in range(150, 260, 40)]
        # color_options = ["#59D5E0", "#F5DD61", "#FAA300", "#F4538A", "purple"]
        color = 0
        self.invaders = []
        for y_cor in y_cors:
            for x_cor in x_cors:
                self.invader = Turtle()
                self.invaders.append(self.invader)
                # self.invader.color(color_options[color])
                self.invader.penup()
                self.invader.shape('inv.gif')
                self.invader.setheading(90)
                self.invader.shapesize(1, 1)
                self.invader.goto((x_cor, y_cor))
            color += 1

    def invaders_move(self):
        current_time_stamp = datetime.now()
        if (current_time_stamp - self.invaders_time_stamp).total_seconds() > self.difficulty / 30:
            x_cors = [invader.xcor() for invader in self.invaders]
            if max(x_cors) > self.limits_x - 40 or min(x_cors) < - self.limits_x + 40:
                self.invaders_move_x *= -1
            for item in self.invaders:
                new_x = item.xcor() + self.invaders_move_x
                new_y = item.ycor()
                item.goto(new_x, new_y)
            self.invaders_time_stamp = datetime.now()

    # SECTION SHOOTING
    def ship_init_fire(self):
        if self.ship_fire is None:
            self.ship_fire = Turtle()
            self.ship_fire.penup()
            self.ship_fire.shape("square")
            self.ship_fire.color("yellow")
            self.ship_fire.shapesize(1, 0.05)
            self.ship_fire.goto((self.ship.xcor(), self.ship.ycor()))
            self.ship_fire.y_move = 12

    def invaders_shoot_init(self):
        current_time_stamp = datetime.now()
        if (current_time_stamp - self.invaders_shoot_time_stamp).total_seconds() > 0.5:
            grouped_invaders = {}

            for invader in self.invaders:
                x_cor = invader.xcor()
                if x_cor not in grouped_invaders:
                    grouped_invaders[x_cor] = []
                grouped_invaders[x_cor].append(invader)

            for x_cor, group in grouped_invaders.items():
                if group:
                    last_invader = group[0]
                    choices = range(1, self.difficulty, 1)
                    choice = random.choice(choices)
                    if choice == 1:
                        self.invader_fire = Turtle()
                        self.invader_fire.penup()
                        self.invader_fire.shape("circle")
                        self.invader_fire.color("white")
                        self.invader_fire.shapesize(1, 0.1)
                        self.invader_fire.goto((last_invader.xcor(), last_invader.ycor()))
                        self.invader_fire.y_move = 12
                        self.invader_fires.append(self.invader_fire)

            self.invaders_shoot_time_stamp = datetime.now()

    def fires_move(self):
        current_time_stamp = datetime.now()
        if (current_time_stamp - self.fire_time_stamp).total_seconds() > 0.05:
            # SHIP fire
            if self.ship_fire:
                new_x = self.ship_fire.xcor()
                new_y = self.ship_fire.ycor() + self.ship_fire.y_move
                self.ship_fire.goto(new_x, new_y)
                self.fire_time_stamp = datetime.now()
                if self.ship_fire.ycor() > self.limits_y:
                    self.ship_fire.hideturtle()
                    self.ship_fire = None

            # INVADERS fire
            for fire in self.invader_fires:
                new_x = fire.xcor()
                new_y = fire.ycor() - 7
                fire.goto(new_x, new_y)
                if fire.ycor() < -self.limits_y:
                    fire.hideturtle()

            self.fire_time_stamp = datetime.now()

    # --- SECTION GAME ITSELF ---
    def game(self):
        game_on = True
        while game_on:
            if self.invaders:
                self.invaders_move()
                self.invaders_shoot_init()
                self.fires_move()
            else:
                # shooting all invaders away
                if self.invader_fires:
                    for fire in self.invader_fires:
                        fire.hideturtle()
                        self.invader_fires.remove(fire)
                self.lives += 1
                self.draw_level_up()
                self.screen.update()
                time.sleep(3)
                self.invaders_setting()
                # making the game harder
                if self.difficulty > 10:
                    self.difficulty -= 5
                self.level += 1

                self.screen.update()
                self.draw_frame_with_score_and_lives()

            # detect hit ship -> invader
            if self.ship_fire:
                for an_invader in self.invaders:
                    if abs(self.ship_fire.ycor() - an_invader.ycor()) < 15 and abs(
                            self.ship_fire.xcor() - an_invader.xcor()) < 15:
                        an_invader.hideturtle()
                        self.invaders.remove(an_invader)
                        self.score += 10
                        self.draw_frame_with_score_and_lives()
                        self.ship_fire.hideturtle()
                        self.ship_fire = None
                        break

            # detect hit invader -> ship
            for fire in self.invader_fires:
                if abs(self.ship.ycor() - fire.ycor()) < 5 and abs(self.ship.xcor() - fire.xcor()) < 25:
                    self.lives -= 1
                    self.draw_frame_with_score_and_lives()
                    fire.hideturtle()
                    self.invader_fires.remove(fire)
                    # lost life effect
                    for _ in range(3):
                        self.ship.hideturtle()
                        self.screen.update()
                        time.sleep(0.2)
                        self.ship.showturtle()
                        self.screen.update()
                        time.sleep(0.2)
                    if self.lives == 0:
                        self.draw_game_over()
                        game_on = False

            # detect hit fire <-> fire
            if self.ship_fire:
                for fire in self.invader_fires:
                    if abs(self.ship_fire.ycor() - fire.ycor()) < 15 and abs(self.ship_fire.xcor() - fire.xcor()) < 5:
                        fire.hideturtle()
                        self.invader_fires.remove(fire)
                        self.score += 7
                        self.draw_frame_with_score_and_lives()
                        self.ship_fire.hideturtle()
                        self.ship_fire = None
                        break

            self.screen.update()


app = SpaceInvaders()
app.screen.mainloop()
