from abc import ABC, abstractmethod
class Item():
	def __init__(self,itemId, name, description):
		self.itemId = itemId
		self.name = name
		self.description = description
		super().__init__()