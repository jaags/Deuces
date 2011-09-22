import random
import os

class Card:
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value
	
	def print_card(self):
		if self.value == 8: print "J",
		elif self.value == 9: print "Q",
		elif self.value == 10: print "K",
		elif self.value == 11: print "A",
		elif self.value == 12: print "2",
		else: print (self.value+3),
		
		if self.suit == 0: print "C",
		elif self.suit == 1: print "D",
		elif self.suit == 2: print "H",
		else: print "S",	

class Deck:
	cards = []
	
	"""
		This init methode shuffles a deck of 52 cards.
		The seed_values[] are ints 0-51, in order.
		seed_values[random] is chosen, and parsed into a card
		via modulo 4 and modulo 13 (gurantees 52 unique cards),
		and then appended to cards[], building the deck,
		until all 52 elements of seed_value have been used.
	"""
	
	def __init__ (self):
		seed_values = [0]
		#generate seed_values[]
		i = 1
		while i < 52:
			seed_values.append(i);
			i = i+1
			
		#generate shuffled 52-card deck -> cards[]
		while (len(seed_values) > 0):
			j = random.randint(0, len(seed_values)-1)	# random seed_values[] index
			jsuit = seed_values[j] % 4		# modulo 4, determinessuit
			jval = seed_values[j] % 13		# modulo 13 determines value
			card = Card(jsuit, jval)		# create a card with above suit/value pair			
			self.cards.append(card)			# add to deck
			del seed_values[j]				# delete the seed value from seed_values[]
		

class Player:
	def __init__ (self, name):
		self.name = name
		self.hand = []
		self.size = 0
		self.chubbs = False
		self.passed = False
		self.pos = 0
		self.done = False
	
	def print_hand(self):
		keys_list = ['Q', "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"]
		print "Current Player: ", self.name
		print "| ",
		for x in self.hand:
			x.print_card()
			print " | ",
		x = 0
		print "\n|  ",
		while x < self.size:
			print keys_list[x],
			print "  |  ",
			x += 1
		print "\n"

class Combo:
	PASS = -1
	NULL = 0
	SINGLE = 1
	DOUBLE = 2
	TRIPLE = 3
	STRAIGHT = 4
	FLUSH = 5
	FULLHOUSE = 6
	THREEDUBS = 7
	TWOTRIPS = 8
	FOURS = 9
	SFLUSH = 10
	
	def __init__(self, cards):
		self.cards = cards
		self.size = len(self.cards)
		self.valid = True
		self.type = Combo.PASS
		self.value = -1
		self.suit = -1
		
		# player doesn't enter 0 cards, is not passing
		if (len (self.cards) > 0):
			self.type = Combo.NULL
			self.value = self.cards[len(cards)-1].value
			self.suit = self.cards[len(cards)-1].suit
			
			if (len (self.cards) == 1):
				self.type = Combo.SINGLE
				
			elif (len (self.cards) == 2):			# check if two cards are a pair
				if (self.cards[0].value == self.cards[1].value):
					self.type = Combo.DOUBLE 
					
			elif (len (self.cards) == 3):			# check if three cards are trips
				if (self.cards[0].value == self.cards[1].value and 
					self.cards[0].value == self.cards[2].value):
					self.type = Combo.TRIPLE
					
			elif (len (self.cards) == 5):			# check if valid 5 card hand
				straight = True
				flush = True
				fullhouse = False
				fours = False
			
				i = 0
				for x in self.cards:
					if self.cards[0].value != (x.value - i):
						straight = False
						break
					i = i+1
					
				for x in self.cards:
					if self.cards[0].suit != x.suit:
						flush = False
						break
						

				if (self.cards[0].value == self.cards[1].value and 
					self.cards[0].value == self.cards[2].value and
					self.cards[3].value == self.cards[4].value):
					fullhouse = True
				if (self.cards[0].value == self.cards[1].value and
					self.cards[2].value == self.cards[3].value and 
					self.cards[2].value == self.cards[4].value):
					fullhouse == True
				if (self.cards[0].value == self.cards[1].value and 
					self.cards[0].value == self.cards[2].value and
					self.cards[0].value == self.cards[3].value):
					fours = True
				if (self.cards[1].value == self.cards[2].value and 
					self.cards[1].value == self.cards[3].value and
					self.cards[1].value == self.cards[4].value):
					fours = True
						
				if (fullhouse == True): self.type = Combo.FULLHOUSE
				elif (fours == True):	self.type = Combo.FOURS
				elif (straight == True and flush == True): self.type = Combo.SFLUSH
				elif (straight == True): self.type = Combo.STRAIGHT
				elif (flush == True):	self.type = Combo.FLUSH
				
			elif (len (self.cards) == 6):
				print "whooo"
				if (self.cards[0] == self.cards[1] and
					self.cards[2] == self.cards[3] and
					self.cards[4] == self.cards[5] and
					self.cards[0].value == (self.cards[2].value)-1 and
					self.cards[0].value == (self.cards[4].value)-2):

					self.type = Combo.THREEDUBS
					print "gas"
				if (self.cards[0] == self.cards[1] and
					self.cards[0] == self.cards[2] and
					self.cards[3] == self.cards[4] and
					self.cards[3] == self.cards[5] and
					self.cards[0].value == (self.cards[3].value)-1):
					
					self.type = Combo.TWOTRIPS
					print "sarto"
			if (self.type == Combo.NULL): self.valid = False
	
	def print_combo(self):
		print "| ",
		for x in self.cards:
			x.print_card()
			print " | ",
		print "\t", self.type
		print "\n"
	

class Game:
	stack = Combo([])
	last_player = Player("")
	gamestart = True
	gameover = False
	donecount = 0
	player_m = []
	
	def update_stack (self, combo, player):
		self.stack = combo
		self.last_player = player
		
	def print_stack(self):
		if (self.stack.size > 0):
			print "Current Combo to beat:"
			print "| ",
			for x in self.stack.cards:
				x.print_card()
				print " | ",
			print "\nPlayed by: ", self.last_player.name, "\n"
		else: print "Empty Stack\n"
		
	def game_started (self):
		self.gamestart = False
	
	def game_over (self):
		self.gameover = True
		
	def player_done (self):
		self.donecount += 1


Deuces = Game()

def main():
	BigThoo = Deck()
	Deuces.player_m = get_players() #Master List of Players
	
	deal_that_shat(BigThoo.cards, Deuces.player_m)
	
	for x in Deuces.player_m:
		x.hand = merge_sort (x.hand)
	
	while Deuces.gameover == False:
		player = []
		for x in Deuces.player_m:
			player.append (x)
		print len (Deuces.player_m)
		starter = pre_trick (player)
		trick(player, starter)
		if (Deuces.donecount == 3): Deuces.game_over()

def get_players ():
	os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
	print """
	Hello, and Welcome to Deuces 0.1 Pre-Alpha
	
	Rules:
	No Bombing Singles
	Pass means you're out till next round
	C -> D -> H -> S
	And finally, always pay respect to The Quang
	
	MAKE SURE TO MAXIMISE YOUR TERMINAL WINDOW
	OTHERWISE GYPPERY WILL ABOUND
	
	
	----------EXAMPLE------------
	Current Combo to beat:

	|  3 C  |  4 D  |  5 S  |  6 C  |  7 C  |
	Played by: Harriet Chubbman

	Current Player: Eleanor Choosevelt
	|  3 D  |  4 C  |  4 H  |  5 H  |  6 D  |  6 S  |  7 S  |
	|   Q   |   W   |   E   |   R   |   T   |   Y   |   U   |
	
	Enter Selection: qwrtu <--Here, the player chooses these letters to play a higher straight (ignore caps)
	
	
	
	Start by entering Player Names
	
	"""
	
	player = []
	x = 1
	while x <= 4:
		print "Player ", x, " Enter name: ",
		name = raw_input ("")
		player.append (Player(name))
		x += 1
		
	return player
	
def pre_trick (player):
	Deuces.update_stack(Combo([]), Player (""))
	starter = 0
	x = 0
	while x < len (player):
		if player[x].chubbs == True:
			starter = x
			player[x].chubbs = False
		if player[x].size == 0:
			del player[x]
			x -= 1
		x += 1
	return starter

def trick(player, starter):
	j = starter
	while len (player) > 1:
		while j < len (player) and len (player) > 1:
			os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
			if (Deuces.gamestart == False):
				print """



							PASS THE COMPUTER TO			
															
					 		THE NEXT PLAYER					
															
							THEN HIT ENTER TO CONTINUE		
															
							NO PEEKING!						
				"""
			else: 
				print "\n\n\n\n"
				
				
				print player[j].name, " is Chubbs, and will commence play by hitting Enter"
				print "\n\n\n\n\n\n\n\n"
			whatever = raw_input("")
			played = False
			while played == False:
				played = play_some_shat (player[j])
				if (played == False): 
					print "Not a valid hand"
					continue
				if (played.type == Combo.PASS):
					print "Passed"
					del player[j]
					j -= 1
				elif player[j].size == 0:
					Deuces.player_done()
					print "Done"
					del player[j]
					j -= 1
			j += 1
		j = 0
	print player[0].name, " chubby"
	player[0].chubbs = True

def play_some_shat(player):
	os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
	
	print "\n\n\n\n"
	print "Player\t\tCards"
	print "--------------------------------------"
	for x in Deuces.player_m:
		if (x.size <= 6): psize = x.size
		else: psize = "hella"
		print x.name, "\t\t", psize
	
	Deuces.print_stack()
	player.print_hand()	
	
	choice = raw_input ("Enter Selection: ")
	indexes = parse_input (choice)
	
	cards = []
	for x in indexes:
		if (x < len (player.hand)): 
			cards.append(player.hand[x])
			player.hand[x].print_card()
			print ""
			
	combo = Combo(cards)
	
	print "Playing "
	combo.print_combo()
	
	if combo.type == Combo.PASS:
		if Deuces.stack.size == 0: return False
		else: return combo
	if (combo.type == Combo.NULL): return False
	if (combo_playable (combo) == False): return False
		
	Deuces.update_stack(combo, player)
	
	x = (len (indexes) - 1)
	while x >= 0:
		del player.hand[indexes[x]]
		player.size -= 1
		x -= 1
		
	return combo	

# Pre-Condition: Combo cannot have type = PASS
def combo_playable (combo):
	if (Deuces.stack.size == 0):
		if (Deuces.gamestart == True):
			if (combo.cards[0].value == 0 and combo.cards[0].suit == 0): 
				Deuces.game_started()
				return True
			else: return False
		else: return True
	elif (Deuces.stack.size != combo.size): 
		if (Deuces.stack.size == 1 or combo.type <= Combo.FULLHOUSE): return False
	
	if (Deuces.stack.type > combo.type): return False
	elif (Deuces.stack.type == combo.type):
		if (Deuces.stack.value > combo.value): return False
		elif (Deuces.stack.value == combo.value):
			if (Deuces.stack.suit > combo.suit): return False
	return True

def deal_that_shat(deck, players):
	while len(deck) > 0:	#loop through deck
		x = 0
		while x < 4:		#loop through players
			card = deck.pop()
			players[x].hand.append(card)
			players[x].size += 1
			if card.value == 0 and card.suit == 0: players[x].chubbs = True
			x = x+1

def parse_input(choice):
	index = []
	choices = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '/']
	cap_choices = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|']
	if len(choice) < 7:
		j = 0
		while j < len (choices):
			for x in choice:
				if x == choices[j] or x == cap_choices[j]: 
					index.append(j)
					break
			j += 1
		
			

	return index

def merge_sort(hand):
	if len(hand) < 2:
		return hand
		
	else:
		middle = len(hand) / 2
		left = merge_sort(hand[:middle])
		right = merge_sort(hand[middle:])
		return merge(left, right)

def merge(left, right):
	result = []
	i, j = 0, 0 
	while i < len(left) and j < len(right):
		if left[i].value < right[j].value:
			result.append(left[i])
			i += 1
		elif left[i].value == right[j].value:
			if left[i].suit < right[j].suit:
				result.append(left[i])
				i += 1
			else:
				result.append(right[j])
				j += 1
		else:
			result.append(right[j])
			j += 1
	result += left[i:]
	result += right[j:]
	return result


if __name__ == "__main__": main()
