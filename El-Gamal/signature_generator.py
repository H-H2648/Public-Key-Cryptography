from utils.helpers import gcd_multiplicative_inverse
from random import randint

class Signature_Generator:
    ### ASSUMES public modulus is prime
    def __init__(self, public_key, secret_key, message):
        self.public_modulus = public_key[0]
        self.generator = public_key[2]
        self.secret_exponent = secret_key
        self.message = message

                
    def generate_signature(self):
        ss = 0
        while ss == 0:
            random_int = randint(1, self.public_modulus - 1)
            if gcd_multiplicative_inverse(random_int, self.public_modulus - 1)[0] > 1:
                random_int = randint(1, self.public_modulus - 1)
            rr = pow(self.generator, random_int, self.public_modulus)
            ss = ((self.message - self.secret_exponent*rr)* pow(random_int, -1, self.public_modulus - 1)) % (self.public_modulus - 1)
        return [rr, ss]