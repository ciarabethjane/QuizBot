class FileManager:
    #This method initialises the class object. The private variable self.__filename holds the name of the file that the class will manage, and the self.file_length variable is initialised as holding the value 0
    def __init__(self, filename):
        self.__filename = filename
        self.file_length = 0
    
    #I adapted code from this website : https://www.geeksforgeeks.org/count-number-of-lines-in-a-text-file-in-python/ to create a method to determine how many lines there are in total in the file. This method opens and reads the file. It iterates through the file using a for loop. Each line increments the lineCounter variable by one. After the end of the loop has been reached, the self.file_length attribute is updated to the value held within the lineCounter variable
    def get_total_no_of_lines(self):
      file = open(self.__filename, "r")
      lineCounter = 0
      for i in file: 
        if i: 
          lineCounter += 1
      self.file_length = lineCounter
      
      return self.file_length
    
    #this method returns the line from the file that corresponds to the number that's passes to the method as the parameter "num". It opens the file, and then checks if the value of num is equal to or greater than zero, and also if num is less than or equal to the total number of lines in the file. If both of these conditions are satisfied, the line is returned as a string. If one of those conditions isn't satisfied, the string "-1" is returned
    def get_line_number(self,num):
      line = ""
      file = open(self.__filename) 
      if num > -1 and num < self.file_length: 
          line = str(file.readlines()[num])
      if num < 0 or num > self.file_length:
        line = "-1"
      return line

    #This is a standard getter method that gets the filename. It returns the filename, and only takes self as a parameter, as is standard for a getter method
    def get_filename(self):
      return self.__filename
    
    #This is a standard setter method that sets the file name to the string that's passed as the parameter "newFileName". This method doesn't return anything, as is standard for setter methods
    def set_filename(self, newFileName):
      self.__filename = newFileName

    #This is the property for the getters and setters of the filename
    fileName = property(get_filename, set_filename)

    #This method opens the file, and uses the inbuilt method readlines() to return the entire contents of the file. I used type casting to ensure that the file content is returned as a string
    def read_file(self):
      file = open(self.__filename) 
      fileContents = str(file.readlines())
      return fileContents
    
    #I created this method to streamline the process of checking that a given range meets the correct format and is in range for the read_line_range method, and later in the child class, the dictionary_from_range method.
    def is_range_ok(self, ran):
      rangeOk = True
      startValue = ran[0]
      stopValue = ran[1]
      if len(ran) < 3 and startValue < stopValue and startValue > -1 or stopValue > -1 and startValue < self.file_length and stopValue < self.file_length:
        rangeOk = True
      else:
        rangeOk = False
      return rangeOk
    #This method returns the lines from a given line range provided that the list of start and stop values (ran) is in the correct format (only has 2 values, and the first value is less than the second value in the list) and is in range (neither value is negative, and both values are less than the total amount of lines available in the file). The counter value is initially assigned the value that's held in the startValue variable, and is incremented as each line within the range is read and added to the stringLines variable. Once the counter value is equal to the value held in the stopValue variable, it terminates the while loop. The stringLines variable returns the lines of the file that are within the given range. If the list of start and stop values isn't in the correct format or is out of range, the stringLines variable is used to return an empty string
    def read_line_range(self, ran):
      line = ""
      stringLines = ""
      startValue = ran[0]
      stopValue = ran[1]
      lines = ""
      counter = startValue
      rangeIsOk = self.is_range_ok(ran)
      if rangeIsOk == True:
        while counter < stopValue + 1:
          line = self.get_line_number(counter)
          lines = lines + line
          counter = counter + 1
        stringLines = lines
      if rangeIsOk == False:
        stringLines = ""
      
      return stringLines


#Child class: BotFileManager
class BotFileManager(FileManager):
  
  def __init__(self,filename):
    self.filename = super().__init__(filename)
    self.clueDictionary = {}
    self.lineCounter = 0

  #Used to output user friendly information   
  def __str__(self):
    botname = "botname"
    fileBeingRead = self.filename
    userInfo = "%s is the file being read for %s" %(fileBeingRead, botname)
    return userInfo


 #This method reads the entire of the file. It uses the parent class' get_total_no_of_lines method to determine how many total lines are in the file. 
  def all_words(self):
    noOfLines = super().get_total_no_of_lines()
    #I changed the lineCounter to be hard coded to always start at line 1 in the file, because the line that corresponds with index 0 in the text file isn't used in the gameplay
    self.lineCounter = self.lineCounter
    #Using the parent class' get_line_number method, with the inbuilt split method, each individual line of the file is retrieved and then split again into words. This enables the program to use linesAsWords[0] as a hard-coded value for the key, as well as linesAsWords[1:5] as the hard-coded values that should be embedded as a list of clues into the dictionary. It repeats this for each line using a while loop. Because of the hard-coded values, I would need to revisit this code if there were to be a level with less than or more than 5 clues.
    while self.lineCounter < noOfLines:
      lines = str(super().get_line_number(self.lineCounter).split("\n"))
      linesAsWords = lines.split(',')
      key = linesAsWords[0]
      values = linesAsWords[1:6]
      self.clueDictionary[key] = values
      self.lineCounter = self.lineCounter + 1
    #this method returns the file as a dictionary, with all of the words to be guessed as keys, and all of the lists of clues as values to the corresponding keys 
    return self.clueDictionary

  #This method uses the read_line_range method from the parent class to read the lines of the text file that correspond to the range that's passed as the parameter "ran". It splits the lines using the "\n" character to detemine each "level", and then splits it further by words as seperated by ",". It only runs correctly if the all_words method is called first. It uses the parent method is_range_ok() to check that the range provided is in the correct format and meets all the necessary conditions to be considered as being in range.
  def dictionary_from_range(self, ran):
    isRangeOk = super().is_range_ok(ran)
    if isRangeOk == True:
      requestedDictSegment = {}
      lines = super().read_line_range(ran)
      levels = str(lines.split("\n"))
      words = levels.split(",")
      totalWordCounter = 0
      wordCounter = 0
      levelNo = 0
      keyWord = ""
      dictvalues = []
      stopValue = ran[1] + 1
      while totalWordCounter < len(words):
        while wordCounter < 6:
          while levelNo < stopValue:
          # if the value in the wordCounter variable == 0, then the program identifies that this word is the correct solution to this level, making it the key. It increments the totalWordCounter and wordCounter variables by 1
            if wordCounter == 0:
              keyWord = words[totalWordCounter]
              totalWordCounter = totalWordCounter + 1
              wordCounter = wordCounter + 1
          #if the value of the wordCounter variable is greater than 0 but less than 6, then we know that the word is one of the clues, so it's added to the list of values for the clues and the total wordCounter and wordCounter variables are incremented by 1
            elif 0 < wordCounter and wordCounter < 6:
              print(totalWordCounter)
              dictvalues.append(words[totalWordCounter])
              totalWordCounter = totalWordCounter + 1
              wordCounter = wordCounter + 1
            #if the wordCounter == 6, then the keyWord and its corresponding values is added to the dictionary that this method will return. The dictvalues that was holding the clues for this level is reassigned as an empty list, the wordCounter is reset to 0 and the levelNo variable is incremented by 1. Similar to the all_words method,  I would also need to revisit this method if there were to be a level with less than or more than 5 clues.
              if wordCounter == 6:
                requestedDictSegment [keyWord] = dictvalues 
                dictvalues = []
                wordCounter = 0
                levelNo = levelNo + 1
          #if the levelNo is equal to the stop value, the wordCounter is assigned a value of 7 to terminate the loops
          if levelNo == stopValue:
            wordCounter = 7
            totalWordCounter = len(words) + 2
    else:
      requestedDictSegment = -1
        
    return requestedDictSegment


  #If the number passed as a parameter to this method is less than the total number of lines in the file (which is calculated using the parent class' get_total_no_of_lines method), the parent class' get_line_number method is used to retrieve the line in the file that corresponds to the value passed as no. The line is then split into individual words (as indicated to the program using ","). The first word in the line is assigned as the key, while the other words are assigned as values to the list that will be used as the value in the dictionary. This key and value is added to the dictionary dictLine. If the parameter no is not less than or equal to the number of lines in the file, the value of -1 is assigned to dictLine. dictLine is returned.
  def line_as_dictionary(self,no):
    if no < super().get_total_no_of_lines():
      dictLine = {}
      line = super().get_line_number(no)
      wordsInLine = line.split(",")
      keyLine = ""
      valuesList = []
      keyLine = wordsInLine[0]
      valuesList = wordsInLine[1:5]
      dictLine [keyLine] = valuesList
    else:
      dictLine = -1
    return dictLine
    
    



  