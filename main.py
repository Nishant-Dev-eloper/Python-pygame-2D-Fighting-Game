import pygame
from pygame import mixer
from easy import Fighter as EasyFighter
from medium import Fighter as MediumFighter
from hard import Fighter as HardFighter
from two_players import Fighter as TwoPlayers

import sys

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fatal distruction")

# set framerate
clock = pygame.time.Clock()
FPS = 80

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("start_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("magic.wav")
magic_fx.set_volume(0.75)

# load background image
bg_image = pygame.image.load("background.jpg").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load("warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("wizard.png").convert_alpha()

# load victory and defeat images for Two Players
victory_two_players_img = pygame.image.load("player_1_wins.png").convert_alpha()
defeat_two_players_img = pygame.image.load("player_2_wins.png").convert_alpha()

# load victory and defeat images for other modes
victory_img = pygame.image.load("victory.png").convert_alpha()
defeat_img = pygame.image.load("defeat.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# define font
count_font = pygame.font.Font("turok.ttf", 80)
score_font = pygame.font.Font("turok.ttf", 30)

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

if len(sys.argv) > 1:
    difficulty = sys.argv[1]
else:
    difficulty = "medium"  # Default to medium if no difficulty is provided in command-line arguments

# Convert the difficulty string to lowercase for consistency
difficulty = difficulty.lower()

if difficulty == "easy":
    FighterClass = EasyFighter
elif difficulty == "hard":
    FighterClass = HardFighter
elif difficulty == "two_players":  # Use "two_players" instead of "Two Players"
    FighterClass = TwoPlayers
else:
    FighterClass = MediumFighter

# create two instances of fighters
fighter_1 = FighterClass(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = FighterClass(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# game loop
run = True
while run:
    clock.tick(FPS)

    # draw background
    draw_bg()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            round_over = True
            round_over_time = pygame.time.get_ticks()
            if difficulty == "two_players":
                winner_img = defeat_two_players_img
                score[1] += 1  # Player 2 wins, so increase player 2's score
            else:
                winner_img = defeat_img
                score[1] += 1  # Player 2 wins, so increase player 2's score
        elif fighter_2.alive == False:
            round_over = True
            round_over_time = pygame.time.get_ticks()
            if difficulty == "two_players":
                winner_img = victory_two_players_img
                score[0] += 1  # Player 1 wins, so increase player 1's score
            else:
                winner_img = victory_img
                score[0] += 1  # Player 1 wins, so increase player 1's score
    else:
        # display victory or defeat image at the center
        img_rect = winner_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(winner_img, img_rect)

        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = FighterClass(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = FighterClass(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()
