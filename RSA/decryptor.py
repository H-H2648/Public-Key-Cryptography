from utils.helpers import modular_exponent

class Decryptor:
    def __init__(self, cipher, public_modulus, secret_exponent):
        self.cipher = cipher
        self.public_modulus = public_modulus
        self.secret_exponent = secret_exponent
    
    def decrypt(self):
        return modular_exponent(self.cipher, self.secret_exponent, self.public_modulus)