import re

class StringValidator:
    RE_ALPHANUMERIC = None

    validateString = ""
    _patterns = {}

    def __init__(self, validateString):
		self.validateString = validateString
    def isAlphaNumeric(self):
        if not self.__class__.RE_ALPHANUMERIC:
            self.__class__.RE_ALPHANUMERIC = re.compile("^[a-zA-Z0-9]+$")
        return self.checkStringAgainstRe(self.__class__.RE_ALPHANUMERIC)

    def checkStringAgainstRe(self, regexObject):
		if regexObject.search(self.validateString) == None:
			return False
		return True