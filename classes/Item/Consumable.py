from abc import ABC, abstractmethod
from .Item import Item

class Consumable(Item):
	def __init__(self, itemId, name, description, use, statEffect): # maybe add skill effect later
		super().__init__(itemId, name, description)
		self.use = use
		self.statEffect = statEffect

	@abstractmethod
	def useMethod(self):
		pass
