#Import all classes from the filemanager.py friendly
from filemanager import *

#Create an instance of the BotFileManager class
dictionaryOfWords = BotFileManager("botfilemanager.txt")

class Bot:
  #This is the questions and clues bank
  #I altered code from https://www.geeksforgeeks.org/python-split-given-dictionary-in-half/ to create the two dictionaries to cater for the first feature. It splits the contents of the file imported by BotFileManager to create two dictionaries that the player can choose from
  allWords = dictionaryOfWords.all_words()
  __words1 = dict(list(allWords.items())[:len(allWords)//2])
  __words2 = dict(list(allWords.items())[len(allWords)//2:])
  
  #The bot is set up to use __words1 as the default dicitonary when the game starts
  chosenWords = __words1

  #This is a list of answers the bot will accept as meaning yes
  __affirmatives = ("yes", "y","Y","Yes","YES","","YeS","YEs","yES","yEs","yeS")

  #This is a list of answers the bot will accept as meaning no
  __deny = ("No","no","nO","n","N")

  #this is the __init__ method. It holds the bot's name, the dictionaries available to the bot for use during gameplay, the dictionary the bot is currently using for playing the game (which is held in a private variable), the list of answers that indicate the user is saying yes, the list of answers that indicate that the user is saying no, the index of the current key in the dictionary for the word that the user is trying to guess, a list of the keys of the dictionary being used to play the game, a list of clues for the current key in the dictionary, the index for the current clue that the bot is providing, and the boolean variable that indicates whether there are more words in the dictionary to play with.
  def __init__(self, playerName, name):
    self.playerName = playerName
    self.nickname = name
    self.words1 = self.__words1
    print(self.__words1)
    self.words2 = self.__words2
    print(self.__words2)
    self.chosenWords = self.words1
    if self.chosenWords == self.words1:
      dictionaryOfWords.lineCounter = 0
    if self.chosenWords == self.words2:
      dictionaryOfWords.lineCounter = 7
    self.affirmatives = self.__affirmatives
    self.deny = self.__deny
    self.currentKeyNo = 0
    self.listOfCorrectGuesses = list(self.chosenWords.keys())
    self.listOfAllValues = self.chosenWords.values()
    self.listOfClues = list(self.chosenWords[self.listOfCorrectGuesses[self.currentKeyNo]])
    self.clueNo = 0
    self.currentCorrectAnswer = self.listOfCorrectGuesses[self.currentKeyNo]
    self.greeting = "Hello! My name is %s, I like to play!"
    print(self.greeting % self.nickname)
    self.goodbye = "Thank you for playing with me! Come back soon!"
    self.hasMoreWords = False

  #this method draws the bot's outline to the console screen. I used the ASCII art of baby yoda from https://asky.lol/237 because I adore baby yoda
  def draw(self):
    botImage = "\n <´(• ﻌ •)`> \n"
    print(botImage)

  #this is the getter method for the bot's name. It retrieves the bot's name. It returns the bot's name, as is conventional for a getter method
  def get_BotName(self):
    return self.nickname
  
  #this is the setter method for the bot's name. It does not return a value as is conventional for a setter method. It sets the bot's nickname to whatever nickname is passed as the newNickname parameter to the method
  def set_BotName(self,newNickname):
    self.nickname = newNickname

  #This is the method that greets the user and briefs them on the rules of the game. It also asks the user if they would like to continue playing the game. It returns the "response" variable
  def initial_greeting(self,playerName):
    greeting = "hello"
    instructions = ", Welcome to my guessing game! \n In this game, I will give you a clue as to what the word is and you will enter your guess using your keyboard.\n If you guess correctly. I will move on to the next word.\n If you guess incorrectly 5 times, I will move on to the next word.\n I will continue until I have run out of words for you to guess.\n I automatically increment our scores by 1, if you'd like to change that, enter the word score as your guess and you'll be able to adjust this setting \n I have 2 dictionaries that you can guess words from. If you'd like to guess from the other dictionary, enter the word new as your guess and I'll swap to the other dictionary \n"
    print(greeting, playerName, instructions)
    self.draw()
    response = input("Type y if you would like to play! " )
    return response
  
  #this is the method that checks to see if the user would like to play the bot's guessing game.It compares the value passed as the "response" parameter to two lists that are stored in private variables: __affirmatives and __deny. If the response matches a value in the affirmatives list, the bot understands the user wants to play, if the response matches a value in the deny list, the bot understands the user doesn't want to play. If the response doesn't match a value in either of the lists, the bot indicates that it doesn't understand the user's response.
  def respond_to_gameplay(self,response):
    if response in self.__affirmatives:
      gameContinue = True
      print("Hurray! Let's Play!")
    elif response in self.__deny:
      self.draw()
      print("You don't want to play? That's ok, maybe we can play later!")
      quit()
    else:
      self.draw()
      print("uh-oh, I don't think I recognise that answer!")
    return gameContinue
    
  #This is the method that is used to return a clue to the user. It uses a counter called clueNo to loop through the list of clues. With each clue, it also prints a message to the user to guess again. When 5 clues have been given, it increments the index of the list of keys to the dictionary, so that the bot will move on to the next word to be guessed in the game.
  def clue(self):
    clues = self.listOfClues
    clueNumberNotification = "Here's clue number %d!"
    clueNoForUser = self.clueNo + 1
    if self.clueNo < 5:
      self.draw()
      print(clueNumberNotification % clueNoForUser)
      print(clues[self.clueNo])
      self.clueNo = self.clueNo + 1
    if self.clueNo == 5:
      self.clueNo = 0

#Thus method checks if the guess that the user has made is correct. It isn't case sensitive  
  def guess(self, word):
    isCorrect = False
    correctAnswerFormat = (self.listOfCorrectGuesses[self.currentKeyNo]).upper().split("['")
    correctAnswer = correctAnswerFormat[1]
    answer = word.upper()
    if answer == correctAnswer:
      isCorrect = True
    if answer != correctAnswer:
      isCorrect = False
    
    
    return isCorrect
  
  #This method is used for moving to the next clue for the word in the dictionary. It compares the index of the current clue to the total number of clues and if the value of the index is less than the value of the total number of clues, it increments the index of the current clue by 1 to move to the next clue.
  def next_clue(self):
    clueNo = self.clueNo
    if self.totalClueIndex < self.totalNoOfClues - 1:
      self.clueNo = clueNo + 1
      self.totalClueIndex = self.totalClueIndex + 1
   
  #This method moves on to the next word in the dictionary. It checks that the current index number of the keys is less than the total number of keys. It then adds one to the index to move to the next word in the list. It creates a list of clues from the values associated with the specific key in the dictionary. It returns the boolean value that's held by "hasMoreWords" to indicate whether or not there are still words left to guess.
  def next_word(self):
    if self.currentKeyNo == len(self.listOfCorrectGuesses)-1:
      self.hasMoreWords = False
      print(self.get_goodbye())
      exit()
    elif self.currentKeyNo < len(self.listOfCorrectGuesses)-1 :
      self.currentKeyNo = self.currentKeyNo + 1
      self.currentCorrectAnswer = self.listOfCorrectGuesses[self.currentKeyNo]
      self.listOfCluesFormat = list(self.chosenWords[self.listOfCorrectGuesses[self.currentKeyNo]])
      self.listOfClues = self.listOfCluesFormat
      self.clueNo = 0
      self.hasMoreWords = True
    
    return self.hasMoreWords

  #This method is implemented when the user wants to switch dictionaries. It swaps the whichever dictionary isn't currently in use, and updates all of the index numbers for clues and words so that the user is starting at the beginning of their new dictionary
  def wordSwap(self):
    if self.chosenWords == self.__words1:
      self.chosenWords = self.__words2
      self.clueNo = 0
      self.currentKeyNo = 0
      print("You have chosen to switch to dictionary 2!")
      print("new word!")
      self.listOfCorrectGuesses = list(self.chosenWords.keys())
      self.listOfAllValues = self.chosenWords.values()
      self.listOfClues = list(self.chosenWords[self.listOfCorrectGuesses[self.currentKeyNo]])
      self.clueNo = 0
      self.currentCorrectAnswer = self.listOfCorrectGuesses[self.currentKeyNo]
    elif self.chosenWords == self.__words2:
      self.chosenWords = self.__words1
      self.clueNo = 0
      self.currentKeyNo = 0
      print("You have chosen to switch to dictionary 1!")
      print("new word!")
      self.listOfCorrectGuesses = list(self.chosenWords.keys())
      self.listOfAllValues = self.chosenWords.values()
      self.listOfClues = list(self.chosenWords[self.listOfCorrectGuesses[self.currentKeyNo]])
      self.clueNo = 0
      self.currentCorrectAnswer = self.listOfCorrectGuesses[self.currentKeyNo]


#This is the getter method for the closing greeting It retrieves the bot's goodbye message, and returns it, as is conventional for a getter method
  def get_goodbye(self):
    goodbye = self.goodbye
    return goodbye

#This is the setter method for the closing greeting It doesn't return any value, as is conventional for a setter method. It sets the bot's closing greeting to whatever goodbye message is passed as the goodbyeMessage parameter to the method
  def set_goodbye(self, goodbyeMessage):
    self.goodbye = goodbyeMessage



#Creation of the GuessingBot class, which inherits the Bot Parent class     
class GuessingBot(Bot):   
 
  #Inherits the __init__ method from Bot class. This means that the GuessingBot class __init__() method essentially calls the Bot class __init__() method and then it adds the variables of scoreInc, botscore, userscore and clueTracker
  def __init__(self, scoreInc, name, playerName, botscore, userscore):
    super().__init__(playerName, name)
    self.scoreInc = scoreInc
    self.botscore = botscore
    self.userscore = userscore
    self.clueTracker = 0
    self.score_Criteria = 1
    

  #Creates a visual representation for the GuessingBot class. In this case, it's supposed to look like a duck.  
  def draw(self):
    botImage = "\n (•)> \n"
    print(botImage)
  
  #Inherits the initial_greeting() method from the Bot class
  def initial_greeting(self, player_name):
    response = super().initial_greeting(player_name)
    return  response

#inherits the respond_to_gameplay() method from the bot class  
  def respond_to_gameplay(self, response):
    return super().respond_to_gameplay(response)
  
  #Overrides the clue() method from the Bot class to add a prompt for the user to take a guess.
  def clue(self):
    super().clue()
    print("Take a guess!")

  #This is the method that allows the user to change the scoring system of the game. If the user wants to switch the value of a correct guess, they select 1, and then enter the amount they want each correct guess to be worth as a whole number. If the user wants to switch whether the robot gains a point for every incorrect guess the user makes, or if the robot only gains a point after there's no more clues left for a word, they select 2 and the program changes to do the opposite of what it's currently doing. It prints a statement to the user informing them of how the scoring criteria has been changed.
  def score_change(self):
    userMenu = input("If you'd like to change the amount of points a correct answer is worth, enter 1 \n If you'd like to change the scoring criteria to change whether I gain a point for every incorrect guess you make or not, enter 2: ")
    if userMenu == "1":
      self.scoreInc = int(input("Enter the amount you want each correct guess to be worth as a whole number: "))
      print("You have changed the scoring system")
    if userMenu == "2":
      if self.score_Criteria == 1:
        self.score_Criteria = 2
        print("You have turned on penalties for incorrect guesses.")
      elif self.score_Criteria == 2:
        self.score_Criteria = 1
        print("You have turned off penalties for incorrect guesses.")
 


  #inherits the guess() method from the Bot class and returns true or false depending on whether the user's guess is right. If the user guesses correctly, it calls the next_word() method. It uses self.clueNo to keep track of the clues. Once the user has been given 5 clues, it moves to the next word. This method is also responsible for monitoring if the user enters the keywords "score" or "new". If either of the keywords are entered, it calls the appropriate method, and then decreases the index numbers of the clue and current key so that the user doesn't lose a guess or have to move to the next word because they wanted to switch the dicitonary or the scoring criteria. It also ensures the botscore isn't increased when the user changes the scoring criteria or the dictionary
  def guess(self, word):
    self.userGuess = super().guess(word)
    if word == "new":
      super().wordSwap()
      self.botscore = self.botscore - self.scoreInc
    if word == "score":
      self.score_change()
      self.clueNo = self.clueNo - 1
      self.currentKeyNo = self.currentKeyNo - 1
      self.botscore = self.botscore - self.scoreInc
    if word != "new" and word != "score":
      if self.userGuess == True:
        print("Congratulations! You guessed it!")
        self.next_word()
      if self.userGuess == False and self.clueNo == 0:
        print("I've run out of clues for this word")
        self.next_word()
      
    return self.userGuess
  
  #inherits the next_clue() method from the Bot class
  def next_clue(self):
    super().next_clue()

    
  
  #inherits the next_word() method from the Bot class. Because the parent class' next_word() method is used to check if there are words left in the dictionary, I added additional code here to take advantage of the inherited code. This method uses the inherited method to check if there are words left in the dictionary. If there are, it moves to the next word in the dictionary. It alerts the user that it has moved to the next word by printing "It's time for a new word"
  def next_word(self):
    anotherWord = super().next_word()
    if anotherWord == True:
      self.clueNo = 0
      print("It's time for a new word!")

    
      
  #creates a score tallying system. The default setting is that the user has to make 5 incorrect guesses before the bot's score is incremented but if the user changes the score criteria, it increments the bot's score by the scoreInc variable for each incorrect guess the user makes.If the guess the user makes is correct, the user's score is incremented by the amount indicated by the scoring system in the scoreInc variable. The user can also change the value in the scoreInc method by entering the word "score" as their guess, and using the menu presented to them there.
  def add_score(self):
    if self.score_Criteria == 1:
      if self.userGuess == False and self.clueNo == 0:
        self.botscore = self.botscore + self.scoreInc
      if self.userGuess == True:
        self.userscore = self.userscore + self.scoreInc
      print("score: bot =", self.botscore," user =", self.userscore)
    if self.score_Criteria == 2:
      if self.userGuess == False:
        self.botscore = self.botscore + self.scoreInc
      if self.userGuess == True:
        self.userscore = self.userscore + self.scoreInc
      print("score: bot =", self.botscore," user =", self.userscore)
  
  #A getter method to get the closing greeting
  def get_closing_greeting(self):
    return self.goodbye
  
  
  #A setter method to set the closing greeting 
  def set_closing_greeting(self, goodbye):
    self.goodbye = goodbye
    
