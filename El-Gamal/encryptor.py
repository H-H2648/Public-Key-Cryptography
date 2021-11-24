import random

class Encryptor:
    def __init__(self, public_key, message):
        self.public_modulus = public_key[0]
        self.size = public_key[1]
        self.generator = public_key[2]
        self.some_value = public_key[3]
        self.message = message

                
    def encrypt(self):
        exponent = random.randint(1, self.size)
        print(f"r: {exponent}")
        cipher1 = pow(self.generator, exponent, self.public_modulus)
        cipher2 = (self.message*pow(self.some_value, exponent, self.public_modulus)) % self.public_modulus
        return [cipher1, cipher2]