from .Character import Character

class NPC(Character):
	def __init__(self, name, role):
		super().__init__(name)
		self.role = role