#Names: Anan Aramthanapon and Jackson Fiala
# Date: 11/14/18 (Got an extension)


#Description: UNO Game for 2-4 local players. We built a text game first, then converted it onto a GUI using the tkinter library, adding interactive cards and other widgets. 

#Sources:
#https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBwibXFtPtflztSNPGuIB_d
#http://effbot.org/tkinterbook/
#https://stackoverflow.com/questions/12364981/how-to-delete-tkinter-widgets-from-a-window
#https://service.mattel.com/instruction_sheets/42001pr.pdf
#https://www.tutorialspoint.com/python/tk_cursors.htm
#https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python
#https://stackoverflow.com/questions/30685308/how-do-i-change-the-text-size-in-a-label-widget-python-tkinter

#Images used
#https://commons.wikimedia.org/wiki/File:UNO_cards_deck.svg
#https://iconsplace.com/white-icons/arrow-icon-18/


# Honor Pledge
#On our honor, we have neither given nor received unauthorized aid. Anan Aramthanapon, Jackson Fiala


# Explanation:
# We did not add code accounting for if both the draw pile and the discard pile (except the top) runs out, as in a real game,
# this situation would not happen as players would be trying to get rid of their cards instead of keeping them in their hands.
# Also, there is nothing in the rulebook that explains what to do in this situation.


# We did not add an UNO button as we made it so that the player's turn ends immediately once a card is played.
# In addition to this, if an UNO button were to pop up, it is highly unlikely that the player will NOT click it, defeating its purpose.

# Instead of starting the game as described in the rulebook, we decided to start the game by adding cards to the discard pile
# until a normal number card is on top, as that is how both of us have played UNO.
# For the same reason, we decided to make the winner the first to run out of cards instead of going by the point system
# described in the rulebook

#Finally, we decided against putting our classes in other files because they rely to heavily on GUI code present in other aspects of the program


import random #To shuffle the lists
from tkinter import * #For GUI



#Classes
#________________________________________________________________________________________________________________________________________________

class Card: #Card Class
	def __init__(self, color, rank): # Take in color, rank, and image to make each card

		 # Stores the color of the card as an integer, 0 = red, 1 = yellow, 2 = green, 3 = blue
		self.color = color

		# Stores the number/type of card. 10 = skip, 11 = reverse, 12 = +2, 13 = wild, 14 = +4
		self.rank = rank 

		self.img = PhotoImage(file=str(rank)+" "+str(color)+".png") # Uses the color and rank of the card to make a PhotoImage file from the corresponding .png file of the same name
		self.but = Button(playarea,image=self.img, command = self.clickCard, cursor = "plus") # Makes a button using the image of that card

	def clickCard(self): # Activates when card is clicked
		if self.rank == discard.cards[0].rank or self.color == discard.cards[0].color or self.color == 4: # If card is playable:
			useCard(self) # Play that card
			endClear() # End turn after playing a card

class Deck:
	def __init__(self, present): # Make deck
		self.cards = [] # Make an empty deck
		self.present = present # If present == 1, make a full deck. If present == 0, make an empty deck

		if self.present == 1:

			for i in range(4): # For each color except "wild color"
				self.cards.append(Card(i, 0)) # Make 1 zero card

				for x in range(2): # Make 2 copies of the following cards
					for z in range(0,13): # Numbered cards from 1 to 9, and special cards from 10 to 12
						self.cards.append(Card(i, z))

			for q in range(4): # Make 4 wild and draw 4 cards
				for d in range(13,15):
					self.cards.append(Card(4, d))

			random.shuffle(self.cards) # Shuffle the deck

	def deal(self, position): # Removes and returns the value of the card in position of the deck
		try:
			return self.cards.pop(position)
		except IndexError: # If the draw pile is empty
			refreshDraw() # Refresh the draw pile using the discard pile
			return self.cards.pop(position) # Then return it

	def addtotop(self, card): # Add card to front of deck
		self.cards = [card] + self.cards


#All of our GUI main frames
#________________________________________________________________________________________________________________________________________________



window = Tk() # Makes main tkinter window


# Setting up the main frames in the game
infobar = Frame(window, width = 1000, height = 50) # Makes infobar at the top
infobar.pack_propagate(0) # Stop bar from shrinking
infobar.pack()


leftbox = Frame(window, width = 64, height = 300, bg = "black") # box for left arrow
leftbox.pack_propagate(0)
leftbox.pack(side=LEFT)


playarea = Frame(window, width = 620, height = 300, bg = "black") # Makes playarea with the cards
playarea.pack_propagate(0)
playarea.pack(side=LEFT)

rightbox = Frame(window, width = 64, height = 300, bg = "black") # box for right arrow
rightbox.pack_propagate(0)
rightbox.pack(side=LEFT)


butbox = Frame(window, width = 128, height = 300, bg = "black") # box for misc. buttons
butbox.pack_propagate(0)
butbox.pack(side=LEFT)

discardbox = Frame(window, width = 124, height = 300, bg = "black") # box for top of discard pile
discardbox.pack_propagate(0)
discardbox.pack(side=LEFT)

winbox = Frame(window, width = 1000, height = 350) # box when a player wins. Gets packed at the end




#Non-GUI variables
#________________________________________________________________________________________________________________________________________________

playernames = [] #this list will be used to call on the players names
playerhands = [] #this list will be used to call on each player's hand
drawpile = Deck(1) # Make a full deck
discard = Deck(0) # Create an initially empty discard pile
direction = 1 # Direction of the game, can be reversed with a reverse card
turncounter = 0 # corresponds to the index of the player whose turn it is
pagenum = 0 # determines which page of hards in the player's hand gets displayed
colorlist = ["red","yellow","green","blue"] # used to convert color from numbers to strings




# Functions activated by button clicks
#_______________________________________________________________________________________________________________________________________________


 # Activates when Draw Card button is pressed
def drawCard():
	playerhands[turncounter].cards.append(drawpile.deal(0)) # Adds card to end of player's hand
	drawbut.pack_forget() # Remove draw button so they can't draw more than one card in a turn
	refreshCards() # Refresh their hand so they can access the new card they have just drawn
	endbut.pack() # Add the end turn button

# Activates when End Turn button is pressed
def endPress(): 
	global turncounter 
	endClear() # Clear the board for the next player
	turncounter = (turncounter + direction)%len(playernames) # Advance to the next turn
	showNext() # Show the Next Turn button

 # When Next Turn is pressed
def nextPress():
	nextbut.pack_forget() # Remove the Next Turn button
	nextTurn() # Setup the next turn for the next player

 # When left arrow is pressed
def leftPress():
	global pagenum
	pagenum -= 1 # Change the cards displayed in the player's hand to the left by 1
	refreshCards() # Make the new "hand page" show up

 # When right arrow is pressed
def rightPress():
	global pagenum
	pagenum += 1
	refreshCards()

# When the red color picker button is clicked
def rClick(): 
	discard.cards[0].color = 0
	clearWheel() # Remove the color wheel from the screen

 # ^^^ Yellow
def yClick():
	discard.cards[0].color = 1
	clearWheel()

# ^^^ Green
def gClick(): 
	discard.cards[0].color = 2
	clearWheel()

 # ^^^ Blue
def bClick():
	discard.cards[0].color = 3
	clearWheel()

 # Remove the color wheel from the screen
def clearWheel():
	colorinstructions.pack_forget() # Remove the instructions label
	for x in colorwheel: # Remove every color picker button
		x.pack_forget()
	showNext() # Show the next turn button




# Runs when a card that can be played is clicked on
def useCard(card): 
	global direction, turncounter
	cardindex = playerhands[turncounter].cards.index(card) # Searches for the card in the player's hand

	endClear() # Clear the playboard
	discard.addtotop(playerhands[turncounter].deal(cardindex)) # Add that card to the discard pile from the player's hand

	if len(playerhands[turncounter].cards) == 0: # If the player now has no cards in their hand
		win() # run the win function

	# Everything here is mod the number of players in the game so that the turn indicator will loop around

	# Skip card played
	if card.rank == 10: #rank of a skip card
		turncounter = (turncounter+(2*direction))%len(playernames) # add 2 to the turncounter (skip a player)
		showNext() # Shows next button so the next player can start their turn

	# Reverse card played
	elif card.rank == 11: 
		if len(playernames)>2:
			direction = direction * (-1) # reverse the direction of the turns
			turncounter = (turncounter + direction)%len(playernames)
		else:
			direction = direction *(-1)
			turncounter = turncounter #player goes again if only 2 player and reveresed
		showNext()

	 # Draw 2 played
	elif card.rank == 12:
		for i in range(2):
			playerhands[(turncounter+direction)%len(playernames)].cards.append(drawpile.deal(0)) # Next player draws 2 cards
		turncounter = (turncounter+(2*direction))%len(playernames) # Skip that player
		showNext()

	# Plain Wild played
	elif card.rank == 13: 
		turncounter = (turncounter + direction)%len(playernames)
		colorPicker() # Gets player to pick the color of their wild card

	 # Draw 4 played
	elif card.rank == 14:
		for i in range(4):
			playerhands[(turncounter+direction)%len(playernames)].cards.append(drawpile.deal(0)) # Next player draws 4 cards
		turncounter = (turncounter+(2*direction))%len(playernames) # Skip that player
		colorPicker() # Gets player to pick the color of their wild draw4 card

	# Regular number cards
	else: 
		turncounter = (turncounter + direction)%len(playernames) # Add 1 to turncounter
		showNext()


#after clicking okay to a selected amount of users
def Confirm(): 
	global listofentries, numberofplayers #make these two vars global

	spacerlabel2.pack_forget() #remove spacers
	spacerlabel3.pack_forget()
	numberokaybutton.pack_forget() #delete all number of users pieces
	playerselection.pack_forget()
	Numberlabel.pack_forget() 

	numberofplayers = [playerselection.get(i) for i in playerselection.curselection()] #the number of users is equal to the number from the listbox
	numberofplayers = int(numberofplayers[0]) #convert from string to int


	listofentries = [] #make a list for the different text entry boxes
	
	Namelabel.pack(side=TOP)
	for i in range(numberofplayers): #create one text entry for each user
		listofentries.append(0)
		listofentries[i] = Entry(playarea)
		listofentries[i].pack()

	confirmnamesbutton.pack() #enter button

 # if names are confirmed, adds the names to a list
def EnterName():
	for i in range(numberofplayers): # repeat for as many users there are
		playernames.append(listofentries[i].get()) # add to the list playernames each entered name
		listofentries[i].pack_forget() # delete text entry

	confirmnamesbutton.pack_forget() # delete other aspects
	Namelabel.pack_forget() # remove everything from the screen
	spacerlabel3.pack_forget()

	beginGame() #start the game




# Other functions
#_______________________________________________________________________________________________________________________________________________

# Makes a hand of 7 cards for each player in the game
def makeHands(): 

	for i in range(len(playernames)): # Make an empty deck for each player in the game
		playerhands.append(Deck(0))

	for i in range(7): # For each player, deal 7 cards into their deck
		for x in playerhands:
			x.addtotop(drawpile.deal(0))

# Makes the discard pile at the beginning of the game
def makeDiscard(): 
	while True: # Start the game off by adding a card to the discard pile
		discard.addtotop(drawpile.deal(0)) # Keep adding cards
		if discard.cards[0].rank <= 9: # Until a regular number card is on top, burning cards in the process
			break

# If for some reason (extremely bad players), the draw pile runs out, refresh the draw pile by shuffling every card in the discard pile (except for the top card) back into the draw pile
def refreshDraw(): 

	discardlength = len(discard.cards)

	for i in range(discardlength-1): # Move every card except the top card, starting with the bottom card, of the discard pile to the draw pile
		drawpile.addtotop(discard.deal(-1))

	random.shuffle(drawpile.cards) # Shuffle the new draw pile


# Refreshes the infobar at the top when the next player goes
def refreshinfobar(): 

	# Clear the infobar
	for i in range(len(playernames)): 
		infolist[i].pack_forget()

		# Changes the text of each of the infobar labels
		if i == turncounter: # If it is the player's turn
			infolist[i].config(text = playernames[i] + ". It's your turn!")
		else: # If not, show how many cards they have
			infolist[i].config(text = playernames[i] + ". Cards in hand:" + str(len(playerhands[i].cards)))

	infolist[4].pack_forget() # Remove the draw pile display
	infolist[4].config(text = "Cards left in draw pile: " + str(len(drawpile.cards))) # refresh the draw pile display

	for i in range(len(playernames)): # Add the number of cards other players are holding
		infolist[i].pack(fill = Y, side=LEFT) # Add each player's infobox back in

	infolist[4].pack(fill = Y) # Add draw pile display back in

#if a player uses all cards
def win():

	# remove everything on the screen
	infobar.pack_forget() 
	leftbox.pack_forget()
	playarea.pack_forget()
	rightbox.pack_forget()
	butbox.pack_forget()
	discardbox.pack_forget()

	# pack the winbox
	winbox.pack()
	winbox.pack_propagate(0) # Don't shrink the winbox
	winlabel.config(text = playernames[turncounter] + " wins!") # Display winning player's name in the winlabel
	winlabel.pack(fill=BOTH) # Add the winlabel to the winbox


# Refreshes the player's hand (when scrolling through pages of cards)
def refreshCards(): 

	for x in playerhands[turncounter].cards: # Remove every card in the player's hand from the screen
		x.but.pack_forget()

	leftbut.pack_forget() # Remove the left arrow
	rightbut.pack_forget() # Remove the right arrow

	if pagenum > 0: # If you are not on the first page of cards
		leftbut.pack(side=LEFT) # Add the left arrow so the player can scroll left

	if pagenum < len(playerhands[turncounter].cards)-5: # If you are not on the last page of cards
		rightbut.pack(side=LEFT) # Show the right arrow to allow player to scroll right

	for x in playerhands[turncounter].cards[pagenum:pagenum+5]:
		x.but.pack(side=LEFT) # Show 5 cards (or fewer) in the player's hand depending on which page you are on


# Updates the discard box
def refreshDiscard(): 
	discardlabel.pack(side = TOP) # Add a label the signify that this card on the right is the top of the discard pile

	if discard.cards[0].rank == 13 or discard.cards[0].rank == 14: # If the top card of the discard pile is a wild card
		wildlabel.config(text = "This wild card is \n" + colorlist[discard.cards[0].color], fg = colorlist[discard.cards[0].color])
		wildlabel.pack() # Add colored text to indicate color of the wild card

	topcard.config(image = discard.cards[0].img) # Update the image of the topcard (discard pile) label
	topcard.pack(side=RIGHT) # Put the top card back in

 #Refreshes the playboard
def refreshboard():
	refreshCards() # Shows their first page of cards
	refreshDiscard() # Updates top of discard pile
	drawbut.pack() # Adds the draw button in


#Transition between turns so people can cheat and see other's hands
def showNext():
	nextbut.config(text = playernames[turncounter] + ". Please click this button to begin your turn.") # Update the text to display the player's name
	nextbut.pack() # Display the next button


# Clears the board at the end of a player's turn
def endClear(): 
	global pagenum
	pagenum = 0 # Resets the pagenumber back to 0 for the next player (very left page of their hand)

	drawbut.pack_forget() # Remove everything from the board
	endbut.pack_forget()
	topcard.pack_forget()
	discardlabel.pack_forget()
	leftbut.pack_forget()
	rightbut.pack_forget()
	wildlabel.pack_forget()
	for x in playerhands[turncounter].cards:
		x.but.pack_forget()

#When a wild card is played
def colorPicker():
	colorinstructions.pack(side=TOP) # Add the label explaining what to do
	for x in colorwheel: # Add the color picker buttons
		x.pack(side=TOP)

#Begins next players turn
def nextTurn(): # Runs after next button is pressed
	refreshinfobar() # Prepares the infobar and board for the player
	refreshboard()

#Takes in number of users
def Gamesetup():

	spacerlabel1.pack(side = TOP) # spacers to make the screen look nicer
	Numberlabel.pack() #ask how many users
	spacerlabel2.pack()

	playerselection.pack() # listbox to select # of users
	choices = ["2", "3", "4"] # choices for number of users (2-4 players)
	for i in range(len(choices)): # add all choices to listbox
		playerselection.insert(i, choices[i])

	spacerlabel3.pack()
	numberokaybutton.pack() #display okay button



#main functions for beginning a game
def beginGame(): # starts the game
	makeHands()
	makeDiscard()
	nextTurn()




# All of our GUI Widgets(buttons, labels, listboxes)
#_______________________________________________________________________________________________________________________________________________________________________________________________________________________

topcard = Label(discardbox) # displays image of top of discard pile
discardlabel = Label(discardbox, text = "Discard Pile:", bg = "black", fg = "white") # Shows that this card is the discard pile

winlabel = Label(winbox, font=("Courier", 60)) #winning message

#Buttons for turnplay
drawbut = Button(butbox, text = "Draw Card", command = drawCard)
endbut = Button(butbox, text = "End Turn", command = endPress)
nextbut = Button(playarea, text = "Next Player, please press this button to begin your turn.", command = nextPress)

leftimg = PhotoImage(file="leftarrow.png") #left arrow
leftbut = Button(leftbox, image = leftimg, command = leftPress)

rightimg = PhotoImage(file="rightarrow.png") #right arrow
rightbut = Button(rightbox, image = rightimg, command = rightPress)

#these are various spacers (same color as background) used throughout code to make GUI look nicer
spacerlabel1 = Label(playarea, bg = "black") 
spacerlabel2 = Label(playarea, bg = "black")
spacerlabel3 = Label(playarea, bg = "black")

# Shows information about each player at the top
infolist = [Label(infobar, bg = "blue"),Label(infobar, bg = "red"),Label(infobar, bg = "yellow"),Label(infobar, bg = "green"),Label(infobar)] 



#Buttons/Label that appear when a wild card is played, prompting the user to select a desired color
colorwheel = [Button(butbox, text = "Red", fg = "red", command = rClick),Button(butbox, text = "Yellow", fg = "orange", command = yClick),Button(butbox, text = "Green", fg = "green", command = gClick),Button(butbox, text = "Blue", fg = "blue", command = bClick)]
colorinstructions = Label(playarea, text = "Pick the color you would like your wild card to be.", bg = "black", fg = "white")
wildlabel = Label(discardbox, bg = "black") # displays color for next player for what colors can be played on a wild card


#Widgets for the intial Game setup: Number of users entry, names entry
playerselection = Listbox(playarea, selectmode = BROWSE, width =5, height=8) #this is the listbox for selecting the number of players
Numberlabel = Label(playarea, text = 'Welcome to Uno!!! Select Number of Users') #this provides instruction for entering number of players
numberokaybutton = Button(playarea, text = "Okay", command = Confirm) #this is the button to confirm number of players selection

confirmnamesbutton = Button(playarea, text = "Enter", command = EnterName) #this is the button to confirm the names typed in
Namelabel = Label(playarea, text = 'Enter Player Names') #this provides instruction for entering names




#What kicks off the game
#_____________________________________________________________________________________________________________________________________________________________________________________________________________________



Gamesetup() # Begin the setup!

window.title("UNO Game") # Title of the window
window.mainloop()










