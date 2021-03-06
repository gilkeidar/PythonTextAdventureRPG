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
	monstersFormat = typeFormat == "monsters"
	

	if directionsFormat:
		# form of element is [locationId, direction]
		arrayToLoop = currentLocation.surroundingLocations
	elif itemsFormat:
		# form of element is: object
		arrayToLoop = currentLocation.itemsArray
	elif monstersFormat:
		# form of element is: object
		arrayToLoop = currentLocation.monstersArray

	if(len(arrayToLoop) == 1):
		if directionsFormat:
			starterString += arrayToLoop[0][1] + "."
		elif itemsFormat:
			if not arrayToLoop[0].name.lower().split(" ")[0] == "the":
				starterString += "a "
			starterString += arrayToLoop[0].name + " here."
		elif monstersFormat:
			starterString += "is "
			if not arrayToLoop[0].name.lower().split(" ")[0] == "the":
				starterString += "a "
			starterString += arrayToLoop[0].name + " here."
				
	else:
		for i in range(0, len(arrayToLoop)):
			element = arrayToLoop[i]
			# if this location is the last one in the list
			if(i == len(arrayToLoop) - 1 and len(arrayToLoop) > 1):
				if directionsFormat:
					starterString += "and " + element[1] + "."
				elif itemsFormat or monstersFormat:
					if not arrayToLoop[-1].name.lower().split(" ")[0] == "the":
						starterString += "and a " + element.name + " here."
					else:
						starterString += "and " + element.name + " here."
			elif len(arrayToLoop) == 2:
				if directionsFormat:
					starterString += element[1] + " "
				elif itemsFormat or monstersFormat:
					starterString += element.name + " "
			else:
				if directionsFormat:
					starterString += element[1] + ", "
				elif itemsFormat or monstersFormat:
					if element == arrayToLoop[0]:
						if not arrayToLoop[0].name.lower().split(" ")[0] == "the":
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


def traversalText(pathType, direction, destinationName):
	if pathType == "Walking":
		return "You make your way " + direction + " to " + destinationName + "..."
	elif pathType == "Climbing":
		return "You climb " + direction + " to " + destinationName + "..."
	