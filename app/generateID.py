import random
import string

class Generate:
    numbers =[0,1,2,3,4,5,6,7,8,9]
    lower_alphabets = list(string.ascii_lowercase)
    upper_alphabets = list(string.ascii_uppercase)
    all_char = numbers + lower_alphabets + upper_alphabets


    def __init__(self, length):
        self._length = length
        self._id = self.generateID()
        
        
    def generateID(self):
        ident = ""
        for i in range(self._length):
            num = random.randint(0,61)
            ident+=str(Generate.all_char[num])
        return ident
    @property
    def id(self):
        return self._id
