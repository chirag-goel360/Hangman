import math
import pygame
from random_word import RandomWords
import random

pygame.init()
HEIGHT, WIDTH = 500, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")
RADIUS = 20
SPACING = 15
letters = []
startingx = round((WIDTH - (RADIUS * 2 + SPACING) * 13) / 2)
startingy = 400
A = 65
for i in range(26):
    x = startingx + SPACING * 2 + ((RADIUS * 2 + SPACING) * (i % 13))
    y = startingy + ((i // 13) * (SPACING + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

images = []
for i in range(7):
    hangmanImage = pygame.image.load("hangman" + str(i) + ".png")
    images.append(hangmanImage)
hangman_status = 0
r = RandomWords()
words = r.get_random_words(hasDictionaryDef = "true", includePartOfSpeech = "noun,verb", minCorpusCount = 1,maxCorpusCount = 10, minDictionaryCount = 1, maxDictionaryCount = 10, minLength = 5, maxLength = 8, limit = 15)
wordToGuess = random.choice(words)
wordToGuess = wordToGuess.upper()
guessed = []
WHITE = (255,255,255)
BLACK = (0,0,0)

def draw():
    window.fill(WHITE)
    text = TITLE_FONT.render("HANGMAN GAME", 1, BLACK)
    window.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    show_word = ""
    for letter in wordToGuess:
        if letter in guessed:
            show_word += letter + " "
        else:
            show_word += "_ "
    text = WORD_FONT.render(show_word, 1, BLACK)
    window.blit(text, (400, 200))

    for letter in letters:
        x, y, l, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(l, 1, BLACK)
            window.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    window.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def display_final_message(message):
    pygame.time.delay(2000)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

def main():
    global hangman_status
    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, l, visible = letter
                    if visible:
                        distance = math.sqrt((x - mx)**2 + (y - my)**2)
                        if distance < RADIUS:
                            letter[3] = False
                            guessed.append(l)
                            if l not in wordToGuess:
                                hangman_status += 1
        
        draw()
        victory = True
        for letter in wordToGuess:
            if letter not in guessed:
                victory = False
                break
        
        if victory:
            display_final_message("YOU WON!")
            break
        if hangman_status == 6:
            display_final_message("YOU LOST!")
            break

main()
pygame.quit()