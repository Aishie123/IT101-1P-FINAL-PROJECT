from tkinter import *
import random
import pyglet

# SNAKE GAME by Team CRAKZ :>

# Global Variables
SCORE_FONT_SIZE = 25
GAME_WIDTH = 400
GAME_HEIGHT = 400
SPEED = 80
SPACE_SIZE = 10
BODY_PARTS = 3
SNAKE_COLOR = "#8AC847"
FOOD_COLOR = "#EDD455"
BACKGROUND_COLOR = "#000000"


# CLASSES -----------------------------------------------------------------------------------------------------------

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        # Defining where the food should spawn randomly
        # Converting to pixels by multiplying by the space size
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 2) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 2) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        # It needs a starting corner and an ending corner.
        # That's why we provide x and y as the initial values and
        # x + SPACE_SIZE AND y + SPACE_SIZE as the ending corners.


# FUNCTIONS -----------------------------------------------------------------------------------------------------------

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Updating the snake coordinates
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    check_teleport(snake)

    # Checking if we caught the food, and if we did, we update the score
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()
    else:
        # We only delete the last part of the snake if we did not get the food
        # Deleting the squares of the snake that should not appear on screen
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # Checking if we hit something we should have not hit
    if check_collisions(snake):
        game_over()
    else:
        # Recalling the same function after the game speed value so we can loop
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

    elif new_direction == 'enter':
        pass


def start(start_game):
    if start_game == 'enter':
        main_game()


def counter(reset):
    if reset == 'enter':
        global score
        score = 0
        # configure
        label.config(text="Score: {}".format(score))
        title_screen()


def title_screen():
    canvas.delete(ALL)
    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.25, font=('Monster Friend 2 Back', 35),
                       text="SNAKE GAME", fill="white", tag="game-over")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.25, font=('Monster Friend 2 Center', 35),
                       text="SNAKE GAME", fill="red", tag="game-over")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.25, font=('Monster Friend 2 Fore', 35),
                       text="SNAKE GAME", fill="white", tag="game-over")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 1.75, font=('determination sans', 20),
                       text="Press 'Enter' to Start", fill="red", tag="game-start")

    window.bind('<Return>',
                lambda event: start('enter'))


def game_over():
    canvas.delete(ALL)
    window.update()
    window.bind('<Return>',
                lambda event: counter('enter'))
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.25, font=('determination sans', 60),
                       text="GAME OVER", fill="red", tag="game_over")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 1.75, font=('determination sans', 20),
                       text="Press 'Enter' to Try Again", fill="white", tag="game-start")


def check_collisions(snake):
    # Unpacking the head of the snake
    x, y = snake.coordinates[0]

    # Checking if we collide with any part of the snake, excluding the head
    for body_part in snake.coordinates[1:]:

        if x == body_part[0] and y == body_part[1]:
            return True

    # Returning false if no collisions were detected
    return False


def check_teleport(snake):
    x, y = snake.coordinates[0]

    if x < 0:
        # Setting the X coordinate to be the other end of the map
        x = GAME_WIDTH - SPACE_SIZE
        new_coord = (x, y)
        # Updating the snake X coordinates to teleport it to the other end of the map
        snake.coordinates[0] = new_coord
    if x >= GAME_WIDTH:
        # Setting the X coordinate to be the other end of the map
        x = -SPACE_SIZE
        new_coord = (x, y)
        # Updating the snake X coordinates to teleport it to the other end of the map
        snake.coordinates[0] = new_coord
    if y < 0:
        # Setting the Y coordinate to be the other end of the map
        y = GAME_HEIGHT - SPACE_SIZE
        new_coord = (x, y)
        # Updating the snake Y coordinates to teleport it to the other end of the map
        snake.coordinates[0] = new_coord
    if y >= GAME_HEIGHT:
        # Setting the Y coordinate to be the other end of the map
        y = -SPACE_SIZE
        new_coord = (x, y)
        # Updating the snake Y coordinates to teleport it to the other end of the map
        snake.coordinates[0] = new_coord


def main_game():
    canvas.delete(ALL)
    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind('<Return>',
                lambda event: change_direction('enter'))
    window.bind('<Left>',
                lambda event: change_direction('left'))
    window.bind('<Right>',
                lambda event: change_direction('right'))
    window.bind('<Up>',
                lambda event: change_direction('up'))
    window.bind('<Down>',
                lambda event: change_direction('down'))

    snake = Snake()
    food = Food()

    next_turn(snake, food)


# ------------------------------------------------------------------------------------------------------------------

# Window Configuration
window = Tk()
window.title("Snake")
window.resizable(False, False)

# Importing font files
pyglet.font.add_file('DTM-Sans.otf')
pyglet.font.add_file('MonsterFriend2Back.otf')
pyglet.font.add_file('MonsterFriend2Center.otf')
pyglet.font.add_file('MonsterFriend2Fore.otf')

# Initial Values
score = 0
direction = 'down'

# Creating the label that updates the score
label = Label(window, text="Score:{}".format(score), font=('determination sans', SCORE_FONT_SIZE))
label.pack()

# Creating the canvas where the snake will run
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Calling the function that shows the title screen
title_screen()

# Opening the game in the center of the screen
window.mainloop()