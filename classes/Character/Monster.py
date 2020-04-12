from .Character import Character

class Monster(Character):
	def __init__(self, monsterId, name, description, hp, attack, defense):
		super().__init__(name)
		self.monsterId = monsterId
		self.hp = hp
		self.description = description
		self.attack = attack
		self.defense = defense
		# self.stats = stats
		# self.level = level
		# self.drops = drops