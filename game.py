from tkinter import *
import random
import pyglet
import sys

# SNAKE GAME by Team CRAKZ :>

# Global Variables
SCORE_FONT_SIZE = 25
GAME_WIDTH = 400
GAME_HEIGHT = 400
SPEED = 80  # default speed
SPACE_SIZE = 10
BODY_PARTS = 3
SNAKE_COLOR = "#8AC847"
FOOD_COLOR = "#EDD455"
BACKGROUND_COLOR = "#000000"
RATIO = 1080 / 1920  # default screen ratio


# CLASSES -----------------------------------------------------------------------------------------------------------

class Snake:
    # initialization
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
    # initialization
    def __init__(self):
        # Defines where the food should spawn randomly
        # Converts to pixels by multiplying by the space size
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 2) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 2) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        # It needs a starting corner and an ending corner.
        # That's why x and y were provided as the initial values and
        # x + SPACE_SIZE AND y + SPACE_SIZE as the ending corners.


# FUNCTIONS -----------------------------------------------------------------------------------------------------------

def title_screen():

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    global RATIO

    if sys.platform == "win32":
        RATIO = 1  # for windows
    elif sys.platform == "darwin":
        RATIO = 1.375  # for macOS

    RATIO *= window.winfo_screenwidth() / 1920  # ratio of user's screen

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.20,
                       font=('Monster Friend 2 Back', int(RATIO * 28)),
                       text="SNAKE GAME", fill="white")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.20,
                       font=('Monster Friend 2 Center', int(RATIO * 28)),
                       text="SNAKE GAME", fill="red")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.20,
                       font=('Monster Friend 2 Fore', int(RATIO * 28)),
                       text="SNAKE GAME", fill="white")

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 1.80,
                       font=('determination sans', int(RATIO * 15)),
                       text="Press 'Enter' to Start", fill="red")

    window.bind('<Return>',
                lambda event: start('enter'))


def difficulty():
    # Display for the difficulty levels
    global RATIO

    window.update()
    canvas.delete(ALL)

    window.bind('<Left>',
                lambda event: diff_levels('easy'))
    window.bind('<Down>',
                lambda event: diff_levels('normal'))
    window.bind('<Right>',
                lambda event: diff_levels('hard'))

    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2.50,
                       font=('Determination Sans', int(RATIO * 30)),
                       text="SELECT DIFFICULTY", fill=FOOD_COLOR)
    canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() / 2),
                       font=('Determination Sans', int(RATIO * 15)),
                       text="Press the 'LEFT KEY' for Easy", fill="white")
    canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() / 2) + 25,
                       font=('Determination Sans', int(RATIO * 15)),
                       text="Press the 'DOWN KEY' for Normal", fill="white")
    canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() / 2) + 50,
                       font=('Determination Sans', int(RATIO * 15)),
                       text="Press the 'RIGHT KEY' for Hard", fill="white")

def main_game():

    canvas.delete(ALL)
    window.update()

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


def game_over():
    global RATIO

    canvas.delete(ALL)
    window.update()

    window.bind('<Return>',
                lambda event: counter('enter'))
    window.bind('<Escape>',
                lambda event: exit('esc'))

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() / 2) - 45,
                       font=('determination sans', int(RATIO * 50)),
                       text="GAME OVER", fill="red", tag="game_over")
    canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() / 2) + 10,
                       font=('determination sans', int(RATIO * 15)),
                       text="Press 'Enter' to Try Again", fill="white")
    canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() / 2) + 35,
                       font=('determination sans', int(RATIO * 15)),
                       text="Press 'Esc' to Exit Game", fill="white")


# EVENT HANDLER FUNCTIONS ------

def change_direction(new_direction):
    # Event handler function that sets the direction according to user input
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


def diff_levels(lvl):
    # Event handler function that sets the game speed according to user input
    global SPEED
    if lvl == 'easy':
        SPEED = 150
    elif lvl == 'normal':
        SPEED = 80
    elif lvl == 'hard':
        SPEED = 30
    main_game()


def counter(reset):
    # Event handler function that resets score and goes back to title screen
    if reset == 'enter':
        # if user wants to play again
        global score
        score = 0
        # configure
        label.config(text="Score: {}".format(score))
        title_screen()


def start(start_game):
    # Event handler function that starts game
    if start_game == 'enter':
        difficulty()


def exit(escape):
    # Event handler function that quits game
    if escape == 'esc':
        quit()


# ----------------------------

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

    # Updates the snake coordinates
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    check_teleport(snake)

    # Checks if snake caught the food, and if snake did, the program updates the score
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()
    else:
        # Deletes the last part of the snake if it did not get the food
        # Deletes the squares of the snake that should not appear on screen
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # Checks if snake hit something it should have not hit
    if check_collisions(snake):
        game_over()
    else:
        # Recalls the same function after the game speed (in milliseconds) to proceed to next turn
        window.after(SPEED, next_turn, snake, food)

# ----------------------------

def check_collisions(snake):
    # Gets the coordinates of the snake's head
    x, y = snake.coordinates[0]

    # Checks if snake collides with any part of its body, excluding the head
    for body_part in snake.coordinates[1:]:

        if x == body_part[0] and y == body_part[1]:
            return True

    # Returns false if no collisions were detected
    return False


def check_teleport(snake):
    # Gets the coordinates of the snake's head
    x, y = snake.coordinates[0]

    if x < 0:
        # Sets the X coordinate to be the other end of the map
        x = GAME_WIDTH - SPACE_SIZE

    if x >= GAME_WIDTH:
        # Sets the X coordinate to be the other end of the map
        x = -SPACE_SIZE

    if y < 0:
        # Sets the Y coordinate to be the other end of the map
        y = GAME_HEIGHT - SPACE_SIZE

    if y >= GAME_HEIGHT:
        # Sets the Y coordinate to be the other end of the map
        y = -SPACE_SIZE

    new_coord = (x, y)
    # Updates the snake Y coordinates to teleport it to the other end of the map
    snake.coordinates[0] = new_coord


# ------------------------------------------------------------------------------------------------------------------

# Window Configuration
window = Tk()
window.title("Snake")
window.resizable(False, False)

# Imports font files
pyglet.font.add_file('DTM-Sans.otf')
pyglet.font.add_file('MonsterFriend2Back.otf')
pyglet.font.add_file('MonsterFriend2Center.otf')
pyglet.font.add_file('MonsterFriend2Fore.otf')

# Initial Values
score = 0
direction = 'down'

# Creates the label that updates the score
label = Label(window, text="Score:{}".format(score), font=('determination sans', SCORE_FONT_SIZE))
label.pack()

# Creates the canvas where the snake will run
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Calls the function that shows the title screen
title_screen()

# Opens the game in the center of the screen
window.mainloop()
