from .Consumable import Consumable

class Potion(Consumable):

	def __init__(self, itemId, name, description, use, statEffect):
		super().__init__(itemId, name, description, use, statEffect)
	
	def useMethod(self):
		# Potion use method
		# print("Use method")
		return {"type": self.use, "effect" : self.statEffect, "destroyed" : True}
	# def hello(self):
		# print("Have a nice day!")