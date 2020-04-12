from .Character import Character

class Monster(Character):
	def __init__(self, name, description, hp, attack, defense, level, drops):
		super().__init__(name)
		self.hp = hp
		self.description = description
		self.attack = attack
		self.defense = defense
		# self.stats = stats
		self.level = level
		self.drops = drops