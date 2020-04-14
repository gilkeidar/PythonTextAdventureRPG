from .Character import Character

# Player Stats 
# Classic 4:
# 	STR --> player's physical strength (Damage!)
# 	DEX --> player's dexterity e.g. ability, skill
# 	CON --> player's constitution (Defense!)
# 	INT --> player's intelligence
#
# As I outlined when I originally chose these,
# 	STR --> increases damage
# 	DEX --> increases accuracy
# 	CON --> increases armor class (lowers damage received) and HP
# 	INT --> faster level-up
# 	Level -> Whenever a user levels up, all stats are increased
# 			 or player gets "Stat Points" that can be added to
# 			 any or multiple stats.

class Player(Character):
	def __init__(self, name, hp, level):
		super().__init__(name)
		self.hp = hp; # health of player
		self.fullHP = hp;
		self.level = level;
		self.attack = 1;
		self.defense = 1;
		self.inventory = []; # inventory array
		# self.equipment = [None, None]; # equipment array
		# self.armor = None
		# self.weapon = None
		self.equipment = {"armor": None, "weapon": None}

		# Change to equipment dictionary

