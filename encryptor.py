from utils.helpers import modular_exponent

class Encryptor:
    def __init__(self, public_key, message):
        self.public_modulus = public_key[0]
        self.public_exponent = public_key[1]
        self.message = message

                
    def encrypt(self):
        return modular_exponent(self.message, self.public_exponent, self.public_modulus)
        
        