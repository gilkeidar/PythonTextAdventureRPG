# e.g. an edge
class Path:
	def __init__(self, source, target, pathType, directionST, directionTS):
		# maybe add a path description later, e.g.
		#
		# "You walk through the Gleaming Bridge to Ancient Castle"
		self.source = source # source location object/id
		self.target = target
		self.pathType = pathType # normal path? Through a magic gate? Via well? Via flight? Via magic? (though that's not different from a magic gate, is it...)
		self.directionST = directionST
		self.directionTS = directionTS