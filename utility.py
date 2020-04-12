# Utility function file
import random

# Formats location list text (e.g. "You can go north, south, and east" and "There is a Longsword and a Ranger's Belt here.")
def textRoomFormatter(starterString, typeFormat, currentLocation):
	# type format can be:
	# directions, items, monsters
	# global currentLocation
	# directionsString = "You can go " <- starter string

	arrayToLoop = []

	directionsFormat = typeFormat == "directions"
	itemsFormat = typeFormat == "items"
	

	if directionsFormat:
		# form of element is [locationId, direction]
		arrayToLoop = currentLocation.surroundingLocations
	elif itemsFormat:
		# form of element is: object
		arrayToLoop = currentLocation.itemsArray

	if(len(arrayToLoop) == 1):
		if directionsFormat:
			starterString += arrayToLoop[0][1] + "."
		elif itemsFormat:
			if not arrayToLoop[0].name.split(" ")[0] == "The":
				starterString += "a "
			starterString += arrayToLoop[0].name + " here."
	else:
		for element in arrayToLoop:
			# if this location is the last one in the list
			if(element == arrayToLoop[-1] and len(arrayToLoop) > 1):
				if directionsFormat:
					starterString += "and " + element[1] + "."
				elif itemsFormat:
					if not arrayToLoop[-1].name.split(" ")[0] == "The":
						starterString += "and a " + element.name + " here."
					else:
						starterString += "and " + element.name + " here."
			elif len(arrayToLoop) == 2:
				if directionsFormat:
					starterString += element[1] + " "
				elif itemsFormat:
					starterString += element.name + " "
			else:
				if directionsFormat:
					starterString += element[1] + ", "
				elif itemsFormat:
					if element == arrayToLoop[0]:
						if not arrayToLoop[0].name.split(" ")[0] == "The":
							starterString += "a "
					starterString += element.name + ", "

	return starterString

# Prints a response when the player types an unrecognized command/string
def unrecognizedCommand(containsWords = True):
	responses = []
	# If player said unintelligble text
	if(containsWords):
		responses = ["For an aspiring adventurer, you sure know how to mumble.",
		"Sorry, what did you say?", "Did you say something?", "Sorry?", 
		"I'm afraid I didn't understand that.", "Try saying 'help' to see words I understand!"]
	# If player said nothing (or just spaces)
	else:
		responses = ["For an aspiring adventurer, you sure know how to mumble.",
		"Sorry, what did you say?", "Did you say something?", "Sorry?"]
	response = random.choice(responses)
	return response
