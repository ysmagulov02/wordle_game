import random
import pygame

# colors in RGB
GREY = (100, 100, 100)
GREEN = (90, 160, 40)
YELLOW = (220, 205, 60)
WHITE = (255, 255, 255)
RED = (200, 30, 30)

# in pixels
WIDTH, HEIGHT = 600, 700
MARGIN = 10
TOP_MARGIN = 100
BOTTOM_MARGIN = 100
LEFT_RIGHT_MARGIN = 100

# basic wordle game mechanics
MAX_NUM_GUESSES = 6
WORD_NUM_LETTERS = 5

INPUT = ""
GUESSES = []
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UNGUESSED = ALPHABET
GAME_OVER = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

# 4 margins in between the 5 squares
SQUARE_SIZE = (WIDTH - 4 * MARGIN - 2 * LEFT_RIGHT_MARGIN) // 5

# font settings
FONT = pygame.font.SysFont("free sans bold", SQUARE_SIZE)
FONT_SMALL = pygame.font.SysFont("free sans bold", SQUARE_SIZE // 2)
BIG_FONT = pygame.font.SysFont("free sans bold", 100, bold = True)

# GAME MESSAGES
you_win = BIG_FONT.render("You win!",       True, GREEN, WHITE)
you_lose = BIG_FONT.render("You lose!",     True, RED, WHITE)

# loads vocabulary for the game from a txt file into an array
def load_vocab(filename):
    file = open(filename)
    vocabulary = file.readlines()
    file.close()
    return [word[:5].upper() for word in vocabulary]

VOCABULARY = load_vocab("vocabulary.txt")
SECRET_WORD = random.choice(VOCABULARY)
# print(SECRET_WORD)

# takes a list of words
def determine_unguessed_letters(guesses):
    guessed_letters = "".join(guesses)
    unguessed_letters = ""
    for letter in ALPHABET:
        if letter not in guessed_letters:
            unguessed_letters = unguessed_letters + letter

    return unguessed_letters

# takes a string and an (int) index
def determine_color(guess, j): # j is the letter of the word
    letter = guess[j]
    if letter == SECRET_WORD[j]:
        return GREEN
    elif letter in SECRET_WORD:
        n_target = SECRET_WORD.count(letter)
        n_correct = 0
        n_occurance = 0
        for i in range(WORD_NUM_LETTERS):
            if guess[i] == letter:
                if i <= j:
                    n_occurance += 1
                if letter == SECRET_WORD[i]:
                    n_correct += 1
        if n_target - n_correct - n_occurance >= 0:
            return YELLOW

    # else return grey
    return GREY

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# animation loop
animating = True
while animating:

    # background
    screen.fill("white")
    determine_unguessed_letters(GUESSES)

    # draw unguessed letters
    letters = FONT_SMALL.render(UNGUESSED, False, GREY)
    surface = letters.get_rect(center = (WIDTH // 2, TOP_MARGIN // 2)) # centering the letter inside the square
    screen.blit(letters, surface)

    # drawing squares and guesses onto the screen
    y = TOP_MARGIN
    for i in range(MAX_NUM_GUESSES):
        x = LEFT_RIGHT_MARGIN
        for j in range (WORD_NUM_LETTERS):

            # squares
            square = pygame.Rect(x,  y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GREY, square, width = 2, border_radius = 3)

            # letters/words that have already been guessed
            if i < len(GUESSES): # 17:44 first vid
                color = determine_color(GUESSES[i], j)
                pygame.draw.rect(screen, color, square, border_radius = 3) # no width parameter so it's entirely filled
                letter = FONT.render(GUESSES[i][j], False, WHITE)
                surface = letter.get_rect(center = (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)) # centering the letter inside the square
                screen.blit(letter, surface)
            
            # user text input (next guess)
            if i == len(GUESSES) and j < len(INPUT): # looping through all boxes 
                letter = FONT.render(INPUT[j], False, GREY)
                surface = letter.get_rect(center = (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)) # centering the letter inside the square
                screen.blit(letter, surface)

            x += SQUARE_SIZE + MARGIN
        y += SQUARE_SIZE + MARGIN

    # show the correct answer after game over
    if len(GUESSES) == 6 and GUESSES[5] != SECRET_WORD:
        GAME_OVER = True
        letters = FONT.render(SECRET_WORD, False, GREY)
        surface = letters.get_rect(center = (WIDTH// 2, HEIGHT - BOTTOM_MARGIN // 2 - MARGIN)) # centering the letter inside the square
        screen.blit(letters, surface)
        
        # lose message
        screen.blit(you_lose, (130, 200))
        play_again = BIG_FONT.render("Play again?", True, RED , WHITE)
        screen.blit(play_again, (80, 300))

    # win message
    else:
        if GAME_OVER == True:
            screen.blit(you_win, (140, 200))
            play_again = BIG_FONT.render("Play again?", True, GREEN, WHITE)
            screen.blit(play_again, (80, 300))
        

    # update the screen
    pygame.display.flip()

    # track user interaction 
    for event in pygame.event.get():

        # closing the window stops the animation 
        if event.type == pygame.QUIT:
            animating = False

        # user presses key
        elif event.type == pygame.KEYDOWN:

            # escape key to quit the animation
            if event.key == pygame.K_ESCAPE:
                animating = False

            # backspace to remove letters from user input
            if event.key == pygame.K_BACKSPACE:
                if len(INPUT) > 0:
                    INPUT = INPUT[:len(INPUT) - 1]

            # return key to sumbit a guess
            elif event.key == pygame.K_RETURN:
                if len(INPUT) == 5 and INPUT in VOCABULARY:
                    GUESSES.append(INPUT)
                    UNGUESSED = determine_unguessed_letters(GUESSES)
                    GAME_OVER = True if INPUT == SECRET_WORD else False
                    INPUT = ""
                    
            # space bar to restart the game
            elif event.key == pygame.K_SPACE:
                GAME_OVER = False
                SECRET_WORD = random.choice(VOCABULARY)
                # print(SECRET_WORD)
                GUESSES = []
                UNGUESSED = ALPHABET
                INPUT = ""
            
            # regular text input
            elif len(INPUT) < 5 and not GAME_OVER:
                INPUT = INPUT + event.unicode.upper()
    