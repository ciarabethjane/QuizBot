#Final Version
#https://repl.it/join/uuttvvxi-ciaraelizabethe

#importing pygame and all important classes
import pygame
from botClasses import *


#initializes pygame modules
pygame.init()

#initializes the display surface
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
DISPLAY_SIZE = [DISPLAY_WIDTH, DISPLAY_HEIGHT]
display = pygame.display.set_mode(DISPLAY_SIZE)

#loading in the image (a robot I drew myself using procreate, and placed on a background clipart image to make it look like it was hosting a gameshow), and assigning resolution and position
botResolution = [800,600]
bot_x = 0
bot_y = 0
botPosition = [bot_x, bot_y]
botImg = pygame.image.load("ciarabethbot.png")
botImgScaled = pygame.transform.scale(botImg, botResolution)

#creates a clock to control speed of the game in the game loop. The image is first displayed outside of the loop so that the user can see the bot before they name it :)
clock = pygame.time.Clock()
black = [0,0,0]
pygame,display.blit(botImgScaled, botPosition)
pygame.display.update()

#the initial steps of the game happen outside of the loop. The user inputs their userName and they give the robot a name, and then they respond as to whether they want to play or not
run_game = True
userName = input("Enter player name: ")
botName = input("Name your bot: ")

#an instance of the GuessingBot class is created using the userName and botName the user provided. The default scoring method is that each guess increments either the Bot's score or the User's score by one
guessBot = GuessingBot(1,botName,userName,0,0)
askToPlay = guessBot.initial_greeting(userName)
print(askToPlay)
playAlong = guessBot.respond_to_gameplay(askToPlay)
#This is where the game loop begins.
if playAlong == True:
  while run_game == True:
    display.fill(black)
    pygame,display.blit(botImgScaled, botPosition)
    pygame.display.update()
    guessBot.clue()
    userGuess = guessBot.guess(input("Enter your guess:"))
    guessBot.add_score()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run_game = False


#Test cases the bot definitely passes:
#If the user indicates they don't want to play, the game closes
#If the user guesses all words on the first attempt, the game plays through all of the words and then closes
#If the user only makes incorrect guesses for the entire game, the game plays through all of the words, then closes. 
#The bot only increments its own score if it has run out of clues for the word
#When user inputs "new" as their guess, it triggers feature one and switches to the other dictionary. It starts at the first clue for the first word for the new dictionary. The game doesn't move to the next word or clue after the word "new" is entered as a guess, so the user doesn't lose out on a guess or a word because they want to change the dictionary
#When the user inputs "score" as their guess it triggers feature two and allows the user to select from a menu, which allows them to either change the amount of points a correct guess is worth or change if there's a penalty score awarded to the robot when the user makes an incorrect guess. The game doesn't move to the next word or clue after the word "score" is entered as a guess, so the user doesn't lose out on a guess or a word because they want to change the scoring criteria