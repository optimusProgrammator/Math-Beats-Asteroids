from posix import times
import pygame
import math
import random
import time
import csv
from pygame import mixer

# Initialize the game
pygame.init()

# Screen dimensions
width = 1430
height = 840

#Time
start_time = None
elapsed = 0
saved_times = []

# Create the screen
screen = pygame.display.set_mode((width, height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont("Josefin Sans", 48)
time_font = pygame.font.SysFont("Josefin Sans", 35)

tips_font = pygame.font.SysFont("Josefin Sans", 35)
tips_header = pygame.font.SysFont("Josefin Sans", 80)

small_font = pygame.font.SysFont("Josefin Sans", 32)
victory = pygame.font.SysFont("Josefin Sans", 200)
over = pygame.font.SysFont("Josefin Sans", 200)



# Background
background = pygame.image.load('space_background.jpg')

# Title and Icon
pygame.display.set_caption("Math Beats Asteroids")

# Load and scale the heart image
heart_image = pygame.image.load('love-always-wins.png')
heart_image = pygame.transform.scale(heart_image, (50, 50))  # Adjust size as needed

saved_times_mode_1 = []
saved_times_mode_2 = []
saved_times_mode_3 = []
saved_times_mode_4 = []
saved_times_mode_5 = []

# Player (Stationary Ship)
player_image = pygame.image.load('spaceship (2).png')
playerX = width // 2 - 25  # Center the player
playerY = height - 100

music_muted = False
effects_muted = False
effects_volume = 1.0

# Question Variables
current_question = ""
correct_answer = 0
user_input = ""  # Stores the user's answer as a string

def start_stopwatch():
    global start_time
    start_time = time.time()

def update():
    global elapsed, start_time
    if start_time is not None:
        elapsed = time.time() - start_time

def save_time(mode, elapsed_time):

    if mode == 1:
        saved_times_mode_1.append(elapsed_time)
    elif mode == 2:
        saved_times_mode_2.append(elapsed_time)
    elif mode == 3:
        saved_times_mode_3.append(elapsed_time)
    elif mode == 4:
        saved_times_mode_4.append(elapsed_time)
    elif mode == 5:
        saved_times_mode_5.append(elapsed_time)

    save_time_to_csv(mode, elapsed)

def reset_stopwatch():
    global start_time, elapsed_time
    start_time = None
    elapsed_time = 0

def show_time(elapsed_time):
    font = pygame.font.Font('freesansbold.ttf', 24)
    time_text = f"Time: {elapsed_time:.2f} s"
    time_surface = font.render(time_text, True, (255, 255, 255))
    screen.blit(time_surface, (1000, 200))  # Adjust the position as needed

def save_time_to_csv(mode, elapsed):
    """
    Save the elapsed time for a specific mode to a CSV file.
    """
    with open("times.csv", mode="a", newline="") as file:  # Open in append mode
        writer = csv.writer(file)
        writer.writerow([mode, elapsed])


import csv

def load_times_from_csv():
    """
    Load saved times from a CSV file into global variables.
    The CSV is assumed to have two columns: 'mode' (as number) and 'time'.
    """
    global saved_times_mode_1, saved_times_mode_2, saved_times_mode_3, saved_times_mode_4, saved_times_mode_5

    # Initialize the lists for each mode
    saved_times_mode_1 = []
    saved_times_mode_2 = []
    saved_times_mode_3 = []
    saved_times_mode_4 = []
    saved_times_mode_5 = []

    # Open the CSV file and read the data
    try:
        with open('times.csv', mode='r') as file:
            reader = csv.reader(file)

            # Loop through each row in the CSV file
            for row in reader:
                print(f"Read row: {row}")  # Debug: Print each row to ensure data is being read
                mode = int(row[0])  # Mode number
                time = row[1]  # Time value as string

                # Ensure the time is properly converted to float, handling possible errors
                try:
                    time = float(time)
                except ValueError:
                    print(f"Skipping invalid time value: {time}")
                    continue

                # Append the time to the correct list based on the mode number
                if mode == 1:  # Addition
                    saved_times_mode_1.append(time)
                elif mode == 2:  # Subtraction (if you plan to use 2 for Subtraction)
                    saved_times_mode_2.append(time)
                elif mode == 3:  # Multiplication
                    saved_times_mode_3.append(time)
                elif mode == 4:  # Division
                    saved_times_mode_4.append(time)
                elif mode == 5:  # Order of Operations
                    saved_times_mode_5.append(time)

        # Print the contents of the lists to debug
        print(f"Addition times: {saved_times_mode_1}")
        print(f"Subtraction times: {saved_times_mode_2}")
        print(f"Multiplication times: {saved_times_mode_3}")
        print(f"Division times: {saved_times_mode_4}")
        print(f"Order of Operations times: {saved_times_mode_5}")

    except FileNotFoundError:
        print("CSV file not found, ensure 'saved_times.csv' exists.")

def show_saved_times_for_mode(mode):
    load_times_from_csv()
    """
    Display saved times for a specific mode.

    Args:
        mode (int): The game mode (1-5).
    """
    font = pygame.font.Font(None, 32)
    x, y = 50, 200  # Adjust position as needed

    if mode == 1:
        show_saved_times(saved_times_mode_1, x, y, font)
    elif mode == 2:
        show_saved_times(saved_times_mode_2, x, y, font)
    elif mode == 3:
        show_saved_times(saved_times_mode_3, x, y, font)
    elif mode == 4:
        show_saved_times(saved_times_mode_4, x, y, font)
    elif mode == 5:
        show_saved_times(saved_times_mode_5, x, y, font)

def generate_question():
    """Generate a random addition question."""
    global current_question, correct_answer, score, asteroid_speed
    if score >= 0 and score <= 10:
        asteroid_speed = 1
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        correct_answer = num1 + num2
        current_question = f"{num1} + {num2} = ?"
    if score >= 11 and score <= 20:
        num1 = random.randint(11, 20)
        num2 = random.randint(11, 20)
        asteroid_speed = 0.7
        correct_answer = num1 + num2
        current_question = f"{num1} + {num2} = ?"
    if score >= 21 and score <= 30:
        num1 = random.randint(21, 50)
        num2 = random.randint(21, 50)
        correct_answer = num1 + num2
        asteroid_speed = 0.5
        current_question = f"{num1} + {num2} = ?"
    if score == 31:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        num3 = random.randint(1, 20)
        num4 = random.randint(1, 20)
        asteroid_speed = 0.3
        correct_answer = num1 + num2 + num3 + num4
        current_question = f"{num1} + {num2} + {num3} + {num4}= ?"

def generate_question_2():
    """Generate a random subtraction question."""
    global current_question, correct_answer, score, asteroid_speed
    if score >= 0 and score <= 10:
        asteroid_speed = 1
        num1_2 = random.randint(10, 20)
        num2_2 = random.randint(0, 9)
        correct_answer = num1_2 - num2_2
        current_question = f"{num1_2} - {num2_2} = ?"
    if score >= 11 and score <= 20:
        num1_2 = random.randint(20, 30)
        num2_2 = random.randint(0, 10)
        asteroid_speed = 0.7
        correct_answer = num1_2 - num2_2
        current_question = f"{num1_2} - {num2_2} = ?"
    if score >= 21 and score <= 30:
        num1 = random.randint(30, 50)
        num2 = random.randint(0, 29)
        correct_answer = num1 - num2
        asteroid_speed = 0.5
        current_question = f"{num1} - {num2} = ?"
    if score == 31:
        num1 = random.randint(40, 50)
        num2 = random.randint(11, 20)
        num3 = random.randint(6, 10)
        num4 = random.randint(1, 5)
        asteroid_speed = 0.3
        correct_answer = num1 - num2 - num3 - num4
        current_question = f"{num1} - {num2} - {num3} - {num4} = ?"

def generate_question_3():
    """Generate a random multiplication question."""
    global current_question, correct_answer, score, asteroid_speed
    if score >= 0 and score <= 10:
        asteroid_speed = 1
        num1_2 = random.randint(1, 10)
        num2_2 = random.randint(1, 10)
        correct_answer = num1_2 * num2_2
        current_question = f"{num1_2} X {num2_2} = ?"
    if score >= 11 and score <= 20:
        num1_2 = random.randint(11, 20)
        num2_2 = random.randint(0, 10)
        asteroid_speed = 0.7
        correct_answer = num1_2 * num2_2
        current_question = f"{num1_2} X {num2_2} = ?"
    if score >= 21 and score <= 30:
        num1 = random.randint(21, 50)
        num2 = random.randint(0, 10)
        correct_answer = num1 * num2
        asteroid_speed = 0.5
        current_question = f"{num1} X {num2} = ?"
    if score == 31:
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10)
        num3 = random.randint(0, 10)
        num4 = random.randint(0, 10)
        asteroid_speed = 0.3
        correct_answer = num1 * num2 * num3 * num4
        current_question = f"{num1} X {num2} X {num3} X {num4}= ?"

def generate_question_4():
    """Generate a random division question."""
    global current_question, correct_answer, score, asteroid_speed

    # Ensure valid asteroid speed and question generation based on score range
    if 0 <= score <= 10:
        asteroid_speed = 1.0
        while True:
            num1_4 = random.randint(1, 30)
            num2_4 = random.randint(1, 10)  # Avoid zero
            if num1_4 % num2_4 == 0:
                correct_answer = num1_4 / num2_4
                current_question = f"{num1_4} / {num2_4} = ?"
                break


    elif 11 <= score <= 20:
        asteroid_speed = 0.9
        while True:  # Ensure divisibility
            num1_4 = random.randint(31, 50)
            num2_4 = random.randint(1, 10)  # Avoid zero
            if num1_4 % num2_4 == 0:
                correct_answer = num1_4 / num2_4
                current_question = f"{num1_4} / {num2_4} = ?"
                break

    elif 21 <= score <= 30:
        asteroid_speed = 0.7
        while True:  # Ensure divisibility
            num1 = random.randint(51, 100)
            num2 = random.randint(11, 20)  # Avoid zero
            if num1 % num2 == 0:
                correct_answer = num1 / num2
                current_question = f"{num1} / {num2} = ?"
                break

    elif score >= 31:
        asteroid_speed = 0.5
        while True:  # Ensure all divisions are valid and exact
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            num3 = random.randint(1, 10)
            num4 = random.randint(1, 10)
            if num1 % num2 == 0 and (num1 / num2) % num3 == 0 and ((num1 / num2) / num3) % num4 == 0:
                one = num1 / num2
                two = one / num3
                correct_answer = two / num4
                current_question = f"( ( ({num1} / {num2} ) / {num3}) / {num4}) = ?"
                break

def generate_question_5():
    """Generate a random PEMDAS question."""
    global current_question, correct_answer, score, asteroid_speed
    if score >= 0 and score <= 10:
        asteroid_speed = 0.4
        num15 = random.randint(10, 14)
        num25 = random.randint(1, 10)
        num35 = random.randint(1, 5)
        num45 = random.randint(1, 10)
        correct_answer = ((num15 * num25) + num35) - num45
        current_question = f" (({num15} X {num25}) + {num35}) - {num45} = ?"
    if score >= 11 and score <= 20:
        asteroid_speed = 0.4
        num15 = random.randint(1, 5)
        num25 = random.randint(1, 5)
        num35 = random.randint(1, 2)
        num45 = random.randint(1, 2)
        correct_answer = ((num15 + num25) ** num35) - num45
        current_question = f"(({num15} + {num25}) ^ {num35}) - {num45} = ?"
    if score >= 21 and score <= 30:
        asteroid_speed = 0.4
        while True:  # Ensure divisibility
            num15 = random.randint(50, 100)
            num25 = random.randint(1, 9)
            num35 = random.randint(1, 3)
            num45 = random.randint(1, 20)  # Avoid zero
            if num15 % num25 == 0:
                correct_answer = (num15 / num25) - num35 + num45
                current_question = f"({num15} / {num25}) - {num35} + {num45} = ?"
                break
    if score == 31:
        asteroid_speed = 0.1
        while True:
            num1 = random.randint(11, 20)
            num2 = random.randint(1, 10)  # Avoid zero
            num3 = random.randint(1, 10)  # Avoid zero
            num4 = random.randint(11, 30)  # Avoid zero
            num5 = random.randint(1, 10)  # Avoid zero if necessary

            product = num1 * num2
            if product % num3 == 0:  # Ensure no division by zero or invalid division
                correct_answer = ((num1 * num2) / num3) + num4 - num5
                current_question = f"(({num1} X {num2}) / {num3}) + {num4} - {num5} = ?"
                break

#I WANTED TO ADD A STOPWATCH

# Bullet
bulletImg = pygame.image.load('rah.png')
bulletX = 0
bulletY = playerY
bulletY_change = 10
bullet_state = "ready"

# Asteroid
asteroid_image = pygame.image.load('rock.png')
asteroidX = playerX
asteroidY = -64
asteroid_speed = 0.9

feedback_message = None  # Stores the message ("CORRECT!" or "WRONG!")
feedback_color = None    # Stores the color (e.g., GREEN or RED)
feedback_start_time = 0  # Tracks when the message was displayed

alert_message = None
alert_color = None
alert_start_time = 0

#arrow
arrow = pygame.image.load('arrow.png')
arrow = pygame.transform.scale(arrow, (60, 60))

# Pause button and menu
pause_image = pygame.image.load('pause.png')
pause_rect = pause_image.get_rect(topright=(width - 1350, 20))

# Game variables
lives_count = 7
score = 0

def reset_game():
    global playerX, playerY, bulletX, bulletY, bullet_state, asteroidX, asteroidY, lives_count, score
    playerX = width // 2 - 25
    playerY = height - 100
    bulletX = 0
    bulletY = playerY
    bullet_state = "ready"
    asteroidX = playerX
    asteroidY = -64
    lives_count = 7
    score = 0

def player(x, y):
    screen.blit(player_image, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Asteroid
def asteroid(x, y):
    screen.blit(asteroid_image, (x, y))

def isCollision(asteroidX, asteroidY, bulletX, bulletY):
    distance = math.sqrt(math.pow(asteroidX + 32 - bulletX - 16, 2) + math.pow(asteroidY - bulletY, 2))
    return distance < 27

def show_lives(lives):
    """Display remaining lives as hearts."""
    for i in range(lives):
        screen.blit(heart_image, (10 + (i * 60), 100))  # Space hearts horizontally



def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 160))

def correct():
    global feedback_message, feedback_color, feedback_start_time
    feedback_message = "CORRECT!"
    feedback_color = GREEN
    feedback_start_time = pygame.time.get_ticks()  # Get the current time in milliseconds

def wrong():
    global feedback_message, feedback_color, feedback_start_time
    feedback_message = "WRONG!"
    feedback_color = RED
    feedback_start_time = pygame.time.get_ticks()

def alert():
    global alert_message, alert_color, alert_start_time
    alert_message = "ALERT! ONE LIFE DOWN!"
    alert_color = RED
    alert_start_time = pygame.time.get_ticks()  # Get the current time in milliseconds

def show_question():
    question_text = font.render(current_question, True, WHITE)
    input_text = font.render(user_input, True, WHITE)
    question = font.render("QUESTION: ", True, WHITE)

    # Blit question and input on the screen
    screen.blit(question_text, (1000, 90))
    screen.blit(question, (1000, 40))
    screen.blit(input_text, (1000, 130))  # User's current input

def you_won():
    won_text = victory.render("YOU WIN!!", True, GREEN)
    congrats = font.render("CONGRATULATIONS", True, GREEN)

    screen.blit(won_text, (370, 420))
    screen.blit(congrats, (540, 380))

# Toggle music function
def toggle_music():
    global music_muted
    if music_muted:
        mixer.music.set_volume(1)  # Unmute
        music_muted = False
    else:
        mixer.music.set_volume(0)  # Mute
        music_muted = True


# Settings page
def settings():
    global music_muted, effects_muted, effects_volume  # Access global variables
    settings_running = True

    # Initial volume levels
    music_volume = mixer.music.get_volume()
    wompwomp = mixer.Sound("youtube_ln1S4uWghz0_audio.mp3")
    yayyay = mixer.Sound("victory.mp3")
    laser_sound = mixer.Sound("laser.wav")
    explosionSound = mixer.Sound("explosion.wav")

    # Set initial effects volume based on global effects_volume
    wompwomp.set_volume(effects_volume)
    yayyay.set_volume(effects_volume)
    laser_sound.set_volume(effects_volume)
    explosionSound.set_volume(effects_volume)

    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)

    while settings_running:
        screen.blit(background, (0, 0))

        # Title
        title_text = font_large.render("Settings", True, (255, 255, 255))
        screen.blit(title_text, (400, 50))

        # Music Volume Section
        music_title = font_medium.render("Music Volume", True, (200, 200, 200))
        screen.blit(music_title, (150, 150))
        pygame.draw.rect(screen, (50, 50, 50), (150, 200, 300, 10))  # Slider track
        pygame.draw.circle(screen, (0, 255, 0), (150 + int(music_volume * 300), 205), 10)  # Slider knob
        music_vol_text = font_small.render(f"{int(music_volume * 100)}%", True, (255, 255, 255))
        screen.blit(music_vol_text, (470, 190))

        # Effects Volume Section
        effects_title = font_medium.render("Effects Volume", True, (200, 200, 200))
        screen.blit(effects_title, (150, 250))
        pygame.draw.rect(screen, (50, 50, 50), (150, 300, 300, 10))  # Slider track
        pygame.draw.circle(screen, (0, 255, 0), (150 + int(effects_volume * 300), 305), 10)  # Slider knob
        effects_vol_text = font_small.render(f"{int(effects_volume * 100)}%", True, (255, 255, 255))
        screen.blit(effects_vol_text, (470, 290))

        # Sound Effects Section
        effects_section_title = font_medium.render("Sound Effects", True, (200, 200, 200))
        screen.blit(effects_section_title, (150, 380))
        wompwomp_button = pygame.Rect(150, 440, 200, 50)
        yayyay_button = pygame.Rect(400, 440, 200, 50)
        pygame.draw.rect(screen, (0, 150, 255), wompwomp_button, border_radius=10)
        pygame.draw.rect(screen, (0, 150, 255), yayyay_button, border_radius=10)
        wompwomp_text = font_small.render("Play WompWomp", True, (255, 255, 255))
        yayyay_text = font_small.render("Play YayYay", True, (255, 255, 255))
        screen.blit(wompwomp_text, (wompwomp_button.x + 15, wompwomp_button.y + 10))
        screen.blit(yayyay_text, (yayyay_button.x + 30, yayyay_button.y + 10))

        # Back Button
        back_button = pygame.Rect(150, 540, 200, 50)
        pygame.draw.rect(screen, (255, 200, 0), back_button, border_radius=10)
        back_text = font_small.render("Back to Menu", True, (0, 0, 0))
        screen.blit(back_text, (back_button.x + 20, back_button.y + 10))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Adjust Music Volume Slider
                    if pygame.Rect(150, 200, 300, 20).collidepoint(event.pos):
                        music_volume = (event.pos[0] - 150) / 300
                        music_volume = max(0, min(1, music_volume))
                        mixer.music.set_volume(music_volume)

                    # Adjust Effects Volume Slider
                    elif pygame.Rect(150, 300, 300, 20).collidepoint(event.pos):
                        effects_volume = (event.pos[0] - 150) / 300
                        effects_volume = max(0, min(1, effects_volume))
                        wompwomp.set_volume(effects_volume)
                        yayyay.set_volume(effects_volume)
                        laser_sound.set_volume(effects_volume)
                        explosionSound.set_volume(effects_volume)

                    # Sound Effects Buttons
                    elif wompwomp_button.collidepoint(event.pos):
                        wompwomp.play()
                    elif yayyay_button.collidepoint(event.pos):
                        yayyay.play()

                    # Back Button
                    elif back_button.collidepoint(event.pos):
                        settings_running = False
                        tips()

            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                # Dragging Music Volume Slider
                if pygame.Rect(150, 200, 300, 20).collidepoint(event.pos):
                    music_volume = (event.pos[0] - 150) / 300
                    music_volume = max(0, min(1, music_volume))
                    mixer.music.set_volume(music_volume)

                # Dragging Effects Volume Slider
                elif pygame.Rect(150, 300, 300, 20).collidepoint(event.pos):
                    effects_volume = (event.pos[0] - 150) / 300
                    effects_volume = max(0, min(1, effects_volume))
                    wompwomp.set_volume(effects_volume)
                    yayyay.set_volume(effects_volume)
                    laser_sound.set_volume(effects_volume)
                    explosionSound.set_volume(effects_volume)

        pygame.display.update()

def show_game_over():
    game_over_text = over.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, text_rect)


def tips():
    menu_running = True
    header_for_tips = tips_header.render("TIPS", True, WHITE)
    tip1 = tips_font.render("Tip 1: Look at the question from the top-right of the screen!", True, WHITE)
    tip2 = tips_font.render("Tip 2: Use the num keys to input your answer.", True, WHITE)
    tip3 = tips_font.render("Tip 3: You can use the backspace if you want to erase your answer!", True, WHITE)
    tip4 = tips_font.render("Tip 4: Use the “return” or “enter” button your keyboard to submit your answer!", True, WHITE)
    tip5 = tips_font.render("Tip 5: If the answer is wrong, you'll get another chance "
                       "to answer until you get it right", True, WHITE)
    tip6 = tips_font.render("Tip 6: If the answer is right, you get a point and will move on to the next question!", True, WHITE)
    tip7 = tips_font.render("Tip 7: Score all 31 asteroids, or take down 31 asteroids, you win the game!", True, WHITE)
    tip8 = tips_font.render("Tip 8: Lose all 7 lives, game over!", True, WHITE)
    line = tips_font.render("___________________________________________________________________", True, WHITE)
    exit_tips_text = font.render("Exit", True, WHITE)
    times_text = font.render("Times", True, WHITE)
    settings_text = font.render("Settings", True, WHITE)


    header_for_tipsbox = header_for_tips.get_rect(topleft=(300, 100))
    tip1box = tip1.get_rect(topleft=(300, 200))
    tip2box = tip2.get_rect(topleft=(300, 250))
    tip3box = tip3.get_rect(topleft=(300, 300))
    tip4box = tip4.get_rect(topleft=(300, 350))
    tip5box = tip5.get_rect(topleft=(300, 400))
    tip6box = tip6.get_rect(topleft=(300, 450))
    tip7box = tip7.get_rect(topleft=(300, 500))
    tip8box = tip8.get_rect(topleft=(300, 550))
    linebox = line.get_rect(topleft=(300, 600))
    exit_tips_rect = exit_tips_text.get_rect(topleft=(100, 100))
    timesbox = times_text.get_rect(topleft=(100, 150))
    settings_box = settings_text.get_rect(topleft=(100, 200))


    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_tips_rect.collidepoint(event.pos):
                    menu_running = True
                    main_menu()
                elif timesbox.collidepoint(event.pos):
                    menu_running = False
                    times_view()
                elif settings_box.collidepoint(event.pos):
                    menu_running = False
                    settings()

        screen.blit(background, (0, 0))
        screen.blit(header_for_tips, header_for_tipsbox.topleft)
        screen.blit(tip1, tip1box.topleft)
        screen.blit(tip2, tip2box.topleft)
        screen.blit(tip3, tip3box.topleft)
        screen.blit(tip4, tip4box.topleft)
        screen.blit(tip5, tip5box.topleft)
        screen.blit(tip6, tip6box.topleft)
        screen.blit(tip7, tip7box.topleft)
        screen.blit(tip8, tip8box.topleft)
        screen.blit(line, linebox.topleft)
        screen.blit(times_text, timesbox.topleft)
        screen.blit(exit_tips_text, exit_tips_rect.topleft)
        screen.blit(settings_text, settings_box.topleft)
        screen.blit(arrow, (35,85))
        screen.blit(arrow, (35,135))
        screen.blit(arrow, (35, 185))


        pygame.display.update()


def times_view():
    load_times_from_csv()
    """
    Show a page with the top 3 saved times for each mode.
    """
    print("Entering times view...")  # Debugging line

    run_times_page = True
    x, y = 50, 50  # Starting position for header

    while run_times_page:
        screen.fill(BLACK)  # Clear the screen
        screen.blit(background, (0, 0))  # Optional: Background image

        # Display title at the top of the page
        title = font.render("Top 3 Quickest Times", True, WHITE)
        screen.blit(title, (x, y))

        # Display headers and top times for each mode
        display_top_times(saved_times_mode_1, "Addition", x, y + 50)
        display_top_times(saved_times_mode_2, "Subtraction", x + 250, y + 50)
        display_top_times(saved_times_mode_3, "Multiplication", x + 500, y + 50)
        display_top_times(saved_times_mode_4, "Division", x + 750, y + 50)
        display_top_times(saved_times_mode_5, "Order of Operations", x + 1000, y + 50)

        # Add back button to return to the main menu
        back_button = pygame.Rect(50, 750, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = time_font.render("Back to Tips", True, WHITE)
        screen.blit(back_text, (60, 760))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    run_times_page = False
                    tips()

        pygame.display.update()  # Update the screen


def display_top_times(saved_times, mode_name, x, y):
    load_times_from_csv()
    """
    Helper function to display the top 3 saved times for each mode, along with the mode name.
    """
    # Sort the saved times in ascending order and get the top 3
    sorted_times = sorted(saved_times)[:3] if saved_times else []

    # Print sorted times for debugging
    print(f"Sorted times for {mode_name}: {sorted_times}")

    # Display the mode title
    mode_title = time_font.render(mode_name, True, WHITE)
    screen.blit(mode_title, (x, y))

    # Display the top 3 times or placeholders if empty
    y_offset = y + 40
    if sorted_times:
        for i, time in enumerate(sorted_times):
            time_text = time_font.render(f"{i + 1}. {time:.2f} seconds", True, WHITE)
            screen.blit(time_text, (x, y_offset))
            y_offset += 40  # Adjust space between each entry
    else:
        no_data_text = time_font.render("No times yet", True, WHITE)
        screen.blit(no_data_text, (x, y_offset))


def pause_menu():
    global lives_count, score, asteroidX, asteroidY
    menu_running = True

    # Menu options
    restart_text = font.render("Restart", True, WHITE)
    continue_text = font.render("Continue", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)
    tips_text = font.render("Tips", True, WHITE)

    # Rectangles for clickable options
    restart_rect = restart_text.get_rect(center=(width // 2, height // 2 - 100))
    continue_rect = continue_text.get_rect(center=(width // 2, height // 2))
    exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 100))
    tips_rect = tips_text.get_rect(center=(width // 2, height // 2 + 200))

    tips = [
        "Tip 1: Look at the question from the top-right of the screen!",
        "Tip 2: Use the num keys to input your answer.",
        "Tip 3: You can use the backspace if you want to erase your answer!",
        "Tip 4: Use the “return” or “enter” button your keyboard to submit your answer!",
        "Tip 5: If the answer is wrong, you will be given another chance to input your answer until you get it right",
        "Tip 6: If the answer is right, you get a point and will move on to the next question!",
        "Tip 7: Score all 31 asteroids, or take down 31 asteroids, you win the game!",
        "Tip 8: Lose all 7 lives, game over!"
    ]
    current_tip = 0

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    menu_running = False
                    game_loop_1()
                elif continue_rect.collidepoint(event.pos):
                    menu_running = False
                elif exit_rect.collidepoint(event.pos):
                    menu_running = True
                    main_menu()
                elif tips_rect.collidepoint(event.pos):
                    current_tip = (current_tip + 1) % len(tips)

        # Draw the pause menu
        screen.fill(BLACK)
        screen.blit(restart_text, restart_rect.topleft)
        screen.blit(continue_text, continue_rect.topleft)
        screen.blit(exit_text, exit_rect.topleft)
        screen.blit(tips_text, tips_rect.topleft)

        # Display the current tip
        tip_display = small_font.render(tips[current_tip], True, WHITE)
        tip_rect = tip_display.get_rect(center=(width // 2, height // 2 + 250))  # Adjust position if needed
        screen.blit(tip_display, tip_rect.topleft)

        pygame.display.update()

def pause_menu2():
    global lives_count, score, asteroidX, asteroidY
    menu_running = True

    # Menu options
    restart_text = font.render("Give it another go? (Click here)", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)

    # Rectangles for clickable options
    restart_rect = restart_text.get_rect(center=(width // 2, height // 2 - 100))
    exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 100))

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    reset_game()
                    menu_running = False
                    game_loop_1()
                elif exit_rect.collidepoint(event.pos):
                    menu_running = True
                    main_menu()

        # Draw the pause menu
        screen.fill(BLACK)
        screen.blit(restart_text, restart_rect.topleft)
        screen.blit(exit_text, exit_rect.topleft)

        # Display the current tip
        pygame.display.update()

def game_loop_1():
    reset_game()
    generate_question()  # Generate the first question

    pygame.mixer.music.pause()

    mixer.music.load("epische-melodie-fur-musik-oder-videos-8898.mp3")
    mixer.music.play(0)

    global bullet_state, bulletY, lives_count, asteroidX, asteroidY, user_input, score, elapsed
    global feedback_message, feedback_color, feedback_start_time, effects_volume  # For feedback display
    global alert_message, alert_color, alert_start_time

    feedback_message = None  # Initialize feedback message
    feedback_color = None  # Initialize feedback color
    feedback_start_time = 0  # Initialize feedback timer

    alert_message = "ALERT! ONE LIFE DOWN!"
    alert_color = RED
    alert_start_time = 0

    # Load sound effects
    laser_sound = mixer.Sound("laser.wav")
    explosionSound = mixer.Sound("explosion.wav")
    wrongeh = mixer.Sound("wrong.mp3")

    # Set sound effects volume based on the current settings
    laser_sound.set_volume(effects_volume)
    explosionSound.set_volume(effects_volume)
    wrongeh.set_volume(effects_volume)


    start_stopwatch()  # Start the stopwatch at the beginning of the game

    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Draw pause button
        screen.blit(pause_image, pause_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            # Handle user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # User presses Enter
                    if user_input.isdigit():
                        if int(user_input) == correct_answer:
                            correct()  # Trigger correct feedback
                            laser_sound.play()  # Play laser sound
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            score += 1
                            generate_question()
                        else:
                            wrong() # Trigger wrong feedback
                            wrongeh.play()

                        user_input = ""  # Reset input after feedback
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():  # Add numbers to input
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()

        # Update the stopwatch
        update()

        # Game mechanics
        player(playerX, playerY)

        asteroidY += asteroid_speed
        if asteroidY > 620:
            asteroidY = -64
            asteroidX = playerX
            explosionSound.play()
            alert()
            lives_count -= 1

        if bullet_state == "fire" and isCollision(asteroidX, asteroidY, bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            asteroidY = -64
            asteroidX = playerX

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        asteroid(asteroidX - 35, asteroidY)
        show_lives(lives_count)
        show_score()
        show_question()  # Display the question and input

        # Display the stopwatch on the screen
        show_time(elapsed)

        # Display feedback if it's active and within 2 seconds
        if feedback_message and pygame.time.get_ticks() - feedback_start_time < 900:  # 2 seconds
            feedback_txt = font.render(feedback_message, True, feedback_color)
            screen.blit(feedback_txt, (1000, 140))
        elif alert_message and pygame.time.get_ticks() - alert_start_time < 1000:  # 2 seconds
            alert_txt = font.render(alert_message, True, alert_color)
            screen.blit(alert_txt, (10, 240))
        else:
            feedback_message = None  # Clear feedback after 2 seconds

        # Check game over conditions
        if lives_count <= 0:
            show_game_over()
            pygame.mixer.music.pause()
            wompwomp = mixer.Sound("youtube_ln1S4uWghz0_audio.mp3")
            wompwomp.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            pause_menu2()

        if score == 32:  # Victory condition
            save_time(1, elapsed)
            you_won()
            pygame.mixer.music.pause()
            yayyay = mixer.Sound("victory.mp3")
            yayyay.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            main_menu()

        pygame.display.update()

def game_loop_2():
    reset_game()
    generate_question_2()  # Generate the first question

    pygame.mixer.music.pause()

    mixer.music.load("epische-melodie-fur-musik-oder-videos-8898.mp3")
    mixer.music.play(0)

    global bullet_state, bulletY, lives_count, asteroidX, asteroidY, user_input, score, elapsed
    global feedback_message, feedback_color, feedback_start_time, effects_volume  # For feedback display
    global alert_message, alert_color, alert_start_time

    feedback_message = None  # Initialize feedback message
    feedback_color = None  # Initialize feedback color
    feedback_start_time = 0  # Initialize feedback timer

    alert_message = "ALERT! ONE LIFE DOWN!"
    alert_color = RED
    alert_start_time = 0

    # Load sound effects
    laser_sound = mixer.Sound("laser.wav")
    explosionSound = mixer.Sound("explosion.wav")
    wrongeh = mixer.Sound("wrong.mp3")

    # Set sound effects volume based on the current settings
    laser_sound.set_volume(effects_volume)
    explosionSound.set_volume(effects_volume)
    wrongeh.set_volume(effects_volume)

    start_stopwatch()  # Start the stopwatch at the beginning of the game

    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Draw pause button
        screen.blit(pause_image, pause_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            # Handle user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # User presses Enter
                    if user_input.isdigit():
                        if int(user_input) == correct_answer:
                            correct()  # Trigger correct feedback
                            laser_sound.play()  # Play laser sound
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            score += 1
                            generate_question_2()
                        else:
                            wrong()
                            wrongeh.play()# Trigger wrong feedback

                        user_input = ""  # Reset input after feedback
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():  # Add numbers to input
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()

        # Update the stopwatch
        update()

        # Game mechanics
        player(playerX, playerY)

        asteroidY += asteroid_speed
        if asteroidY > 620:
            asteroidY = -64
            asteroidX = playerX
            explosionSound.play()
            alert()
            lives_count -= 1

        if bullet_state == "fire" and isCollision(asteroidX, asteroidY, bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            asteroidY = -64
            asteroidX = playerX

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        asteroid(asteroidX - 35, asteroidY)
        show_lives(lives_count)
        show_score()
        show_question()  # Display the question and input

        # Display the stopwatch on the screen
        show_time(elapsed)

        # Display feedback if it's active and within 2 seconds
        if feedback_message and pygame.time.get_ticks() - feedback_start_time < 900:  # 2 seconds
            feedback_txt = font.render(feedback_message, True, feedback_color)
            screen.blit(feedback_txt, (1000, 140))
        elif alert_message and pygame.time.get_ticks() - alert_start_time < 1000:  # 2 seconds
            alert_txt = font.render(alert_message, True, alert_color)
            screen.blit(alert_txt, (10, 240))
        else:
            feedback_message = None  # Clear feedback after 2 seconds

        # Check game over conditions
        if lives_count == 0:
            show_game_over()
            pygame.mixer.music.pause()
            wompwomp = mixer.Sound("youtube_ln1S4uWghz0_audio.mp3")
            wompwomp.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            pause_menu2()

        if score == 32:  # Victory condition
            save_time(2, elapsed)
            you_won()
            pygame.mixer.music.pause()
            yayyay = mixer.Sound("victory.mp3")
            yayyay.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            main_menu()

        pygame.display.update()

def game_loop_3():
    reset_game()
    generate_question_3()  # Generate the first question

    pygame.mixer.music.pause()

    mixer.music.load("epische-melodie-fur-musik-oder-videos-8898.mp3")
    mixer.music.play(0)

    global bullet_state, bulletY, lives_count, asteroidX, asteroidY, user_input, score, elapsed
    global feedback_message, feedback_color, feedback_start_time, effects_volume  # For feedback display
    global alert_message, alert_color, alert_start_time

    feedback_message = None  # Initialize feedback message
    feedback_color = None  # Initialize feedback color
    feedback_start_time = 0  # Initialize feedback timer

    alert_message = "ALERT! ONE LIFE DOWN!"
    alert_color = RED
    alert_start_time = 0

    # Load sound effects
    laser_sound = mixer.Sound("laser.wav")
    explosionSound = mixer.Sound("explosion.wav")
    wrongeh = mixer.Sound("wrong.mp3")

    # Set sound effects volume based on the current settings
    laser_sound.set_volume(effects_volume)
    explosionSound.set_volume(effects_volume)
    wrongeh.set_volume(effects_volume)

    start_stopwatch()  # Start the stopwatch at the beginning of the game

    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Draw pause button
        screen.blit(pause_image, pause_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            # Handle user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # User presses Enter
                    if user_input.isdigit():
                        if int(user_input) == correct_answer:
                            correct()  # Trigger correct feedback
                            laser_sound.play()  # Play laser sound
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            score += 1
                            generate_question_3()
                        else:
                            wrong()
                            wrongeh.play()# Trigger wrong feedback

                        user_input = ""  # Reset input after feedback
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():  # Add numbers to input
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()

        # Update the stopwatch
        update()

        # Game mechanics
        player(playerX, playerY)

        asteroidY += asteroid_speed
        if asteroidY > 620:
            asteroidY = -64
            asteroidX = playerX
            explosionSound.play()
            alert()
            lives_count -= 1

        if bullet_state == "fire" and isCollision(asteroidX, asteroidY, bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            asteroidY = -64
            asteroidX = playerX

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        asteroid(asteroidX - 35, asteroidY)
        show_lives(lives_count)
        show_score()
        show_question()  # Display the question and input

        # Display the stopwatch on the screen
        show_time(elapsed)

        # Display feedback if it's active and within 2 seconds
        if feedback_message and pygame.time.get_ticks() - feedback_start_time < 900:  # 2 seconds
            feedback_txt = font.render(feedback_message, True, feedback_color)
            screen.blit(feedback_txt, (1000, 140))
        elif alert_message and pygame.time.get_ticks() - alert_start_time < 1000:  # 2 seconds
            alert_txt = font.render(alert_message, True, alert_color)
            screen.blit(alert_txt, (10, 240))
        else:
            feedback_message = None  # Clear feedback after 2 seconds

        # Check game over conditions
        if lives_count == 0:
            show_game_over()
            pygame.mixer.music.pause()
            wompwomp = mixer.Sound("youtube_ln1S4uWghz0_audio.mp3")
            wompwomp.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            pause_menu2()

        if score == 32:  # Victory condition
            save_time(3, elapsed)
            you_won()
            pygame.mixer.music.pause()
            yayyay = mixer.Sound("victory.mp3")
            yayyay.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            main_menu()

        pygame.display.update()

def game_loop_4():
    reset_game()
    generate_question_4()  # Generate the first question

    pygame.mixer.music.pause()

    mixer.music.load("epische-melodie-fur-musik-oder-videos-8898.mp3")
    mixer.music.play(0)

    global bullet_state, bulletY, lives_count, asteroidX, asteroidY, user_input, score, elapsed
    global feedback_message, feedback_color, feedback_start_time, effects_volume  # For feedback display
    global alert_message, alert_color, alert_start_time

    feedback_message = None  # Initialize feedback message
    feedback_color = None  # Initialize feedback color
    feedback_start_time = 0  # Initialize feedback timer

    alert_message = "ALERT! ONE LIFE DOWN!"
    alert_color = RED
    alert_start_time = 0

    # Load sound effects
    laser_sound = mixer.Sound("laser.wav")
    explosionSound = mixer.Sound("explosion.wav")
    wrongeh = mixer.Sound("wrong.mp3")

    # Set sound effects volume based on the current settings
    laser_sound.set_volume(effects_volume)
    explosionSound.set_volume(effects_volume)
    wrongeh.set_volume(effects_volume)

    start_stopwatch()  # Start the stopwatch at the beginning of the game

    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Draw pause button
        screen.blit(pause_image, pause_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            # Handle user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # User presses Enter
                    if user_input.isdigit():
                        if int(user_input) == correct_answer:
                            correct()  # Trigger correct feedback
                            laser_sound.play()  # Play laser sound
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            score += 1
                            generate_question_4()
                        else:
                            wrong()
                            wrongeh.play()
                            # Trigger wrong feedback

                        user_input = ""  # Reset input after feedback
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():  # Add numbers to input
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()

        # Update the stopwatch
        update()

        # Game mechanics
        player(playerX, playerY)

        asteroidY += asteroid_speed
        if asteroidY > 620:
            asteroidY = -64
            asteroidX = playerX
            explosionSound.play()
            alert()
            lives_count -= 1

        if bullet_state == "fire" and isCollision(asteroidX, asteroidY, bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            asteroidY = -64
            asteroidX = playerX

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        asteroid(asteroidX - 35, asteroidY)
        show_lives(lives_count)
        show_score()
        show_question()  # Display the question and input

        # Display the stopwatch on the screen
        show_time(elapsed)

        # Display feedback if it's active and within 2 seconds
        if feedback_message and pygame.time.get_ticks() - feedback_start_time < 900:  # 2 seconds
            feedback_txt = font.render(feedback_message, True, feedback_color)
            screen.blit(feedback_txt, (1000, 140))
        elif alert_message and pygame.time.get_ticks() - alert_start_time < 1000:  # 2 seconds
            alert_txt = font.render(alert_message, True, alert_color)
            screen.blit(alert_txt, (10, 240))
        else:
            feedback_message = None  # Clear feedback after 2 seconds

        # Check game over conditions
        if lives_count == 0:
            show_game_over()
            pygame.mixer.music.pause()
            wompwomp = mixer.Sound("youtube_ln1S4uWghz0_audio.mp3")
            wompwomp.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            pause_menu2()

        if score == 32:  # Victory condition
            save_time(4, elapsed)
            you_won()
            pygame.mixer.music.pause()
            yayyay = mixer.Sound("victory.mp3")
            yayyay.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            main_menu()

        pygame.display.update()

def game_loop_5():
    reset_game()
    generate_question_5()  # Generate the first question

    pygame.mixer.music.pause()

    mixer.music.load("epische-melodie-fur-musik-oder-videos-8898.mp3")
    mixer.music.play(0)

    global bullet_state, bulletY, lives_count, asteroidX, asteroidY, user_input, score, elapsed
    global feedback_message, feedback_color, feedback_start_time, effects_volume  # For feedback display
    global alert_message, alert_color, alert_start_time

    feedback_message = None  # Initialize feedback message
    feedback_color = None  # Initialize feedback color
    feedback_start_time = 0  # Initialize feedback timer

    alert_message = "ALERT! ONE LIFE DOWN!"
    alert_color = RED
    alert_start_time = 0

    # Load sound effects
    laser_sound = mixer.Sound("laser.wav")
    explosionSound = mixer.Sound("explosion.wav")
    wrongeh = mixer.Sound("wrong.mp3")

    # Set sound effects volume based on the current settings
    laser_sound.set_volume(effects_volume)
    explosionSound.set_volume(effects_volume)
    wrongeh.set_volume(effects_volume)

    start_stopwatch()  # Start the stopwatch at the beginning of the game

    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Draw pause button
        screen.blit(pause_image, pause_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            # Handle user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # User presses Enter
                    if user_input.isdigit():
                        if int(user_input) == correct_answer:
                            correct()  # Trigger correct feedback
                            laser_sound.play()  # Play laser sound
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            score += 1
                            generate_question_5()
                        else:
                            wrong()
                            wrongeh.play()# Trigger wrong feedback

                        user_input = ""  # Reset input after feedback
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():  # Add numbers to input
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()

        # Update the stopwatch
        update()

        # Game mechanics
        player(playerX, playerY)

        asteroidY += asteroid_speed
        if asteroidY > 620:
            asteroidY = -64
            asteroidX = playerX
            explosionSound.play()
            alert()
            lives_count -= 1

        if bullet_state == "fire" and isCollision(asteroidX, asteroidY, bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            asteroidY = -64
            asteroidX = playerX

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

        asteroid(asteroidX - 35, asteroidY)
        show_lives(lives_count)
        show_score()
        show_question()  # Display the question and input

        # Display the stopwatch on the screen
        show_time(elapsed)

        # Display feedback if it's active and within 2 seconds
        if feedback_message and pygame.time.get_ticks() - feedback_start_time < 900:  # 2 seconds
            feedback_txt = font.render(feedback_message, True, feedback_color)
            screen.blit(feedback_txt, (1000, 140))
        elif alert_message and pygame.time.get_ticks() - alert_start_time < 1000:  # 2 seconds
            alert_txt = font.render(alert_message, True, alert_color)
            screen.blit(alert_txt, (10, 240))
        else:
            feedback_message = None  # Clear feedback after 2 seconds

        # Check game over conditions
        if lives_count == 0:
            show_game_over()
            pygame.mixer.music.pause()
            wompwomp = mixer.Sound("youtube_ln1S4uWghz0_audio.mp3")
            wompwomp.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            pause_menu2()

        if score == 32:  # Victory condition
            save_time(5, elapsed)
            you_won()
            pygame.mixer.music.pause()
            yayyay = mixer.Sound("victory.mp3")
            yayyay.play()
            pygame.display.update()
            pygame.time.delay(5000)
            run_game = False
            main_menu()

        pygame.display.update()



def main_menu():

    global music_muted

    menu_running = True
    music_muted = False  # Initially, music is not muted

    load_times_from_csv()
    title_logo = pygame.image.load('Math-removebg-preview.png')
    title_logo = pygame.transform.scale(title_logo, (700, 700))
    logo_rect = title_logo.get_rect(center=(400, 400))  # Adjust logo position to center
    screen.blit(background, (0, 0))
    screen.blit(title_logo, logo_rect.topleft)

    mixer.music.load("twisterion-b1-221376.wav")
    mixer.music.play(-1)

    # Main Menu options
    add_mode_text = font.render("ADDITION", True, WHITE)
    sub_mode_text = font.render("SUBTRACTION", True, WHITE)
    mult_mode_text = font.render("MULTIPLICATION", True, WHITE)
    div_mode_text = font.render("DIVISION", True, WHITE)
    pemdas_mode_text = font.render("ORDER OF OPERATIONS", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    tips_text = font.render("TIPS & EXTRAS", True, WHITE)

    add_mode_rect = add_mode_text.get_rect(center=(1000, 150))
    sub_mode_rect = sub_mode_text.get_rect(center=(1000, 250))
    mult_mode_rect = mult_mode_text.get_rect(center=(1000, 350))
    div_mode_rect = div_mode_text.get_rect(center=(1000, 450))
    pemdas_mode_rect = pemdas_mode_text.get_rect(center=(1000, 550))
    quit_rect = quit_text.get_rect(center=(1000, 650))
    tip_rect = tips_text.get_rect(center=(405, 650))


    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if add_mode_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop_1()  # Proceed to the game
                if sub_mode_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop_2()  # Proceed to the game
                if mult_mode_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop_3()  # Proceed to the game
                if div_mode_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop_4()
                if pemdas_mode_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop_5()
                if tip_rect.collidepoint(event.pos):
                    menu_running = False
                    tips()
                    # Proceed to the game
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        # Blit the menu items on the screen
        screen.blit(add_mode_text, add_mode_rect.topleft)
        screen.blit(sub_mode_text, sub_mode_rect.topleft)
        screen.blit(mult_mode_text, mult_mode_rect.topleft)
        screen.blit(div_mode_text, div_mode_rect.topleft)
        screen.blit(pemdas_mode_text, pemdas_mode_rect.topleft)
        screen.blit(quit_text, quit_rect.topleft)
        screen.blit(tips_text, tip_rect.topleft)

        pygame.display.update()

def main():
    pygame.init()
    load_times_from_csv()  # Load saved times at startup
    main_menu()
    pygame.quit()

main()
