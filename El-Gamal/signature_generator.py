from utils.helpers import gcd_multiplicative_inverse
from random import randint

class Signature_Generator:
    ### ASSUMES public modulus is prime
    def __init__(self, public_key, secret_key, message):
        self.public_modulus = public_key[0]
        self.size = public_key[1]
        self.generator = public_key[2]
        self.secret_exponent = secret_key
        self.message = message

    ### requires a prime modulus 
    def generate_signature(self):
        ss = 0
        while ss == 0:
            random_int = randint(1, self.size)
            if gcd_multiplicative_inverse(random_int, self.size)[0] > 1:
                random_int = randint(1, self.size)
            rr = pow(self.generator, random_int, self.public_modulus)
            ss = ((self.message - self.secret_exponent*rr)* pow(random_int, -1, self.size)) % (self.size)
        return [rr, ss]

    def generate_signature_DSA(self):
        ss = 0
        while ss == 0:
            random_int = randint(1, self.size - 1)
            if gcd_multiplicative_inverse(random_int, self.size)[0] > 1:
                random_int = randint(1, self.size)
            rr = (pow(self.generator, random_int, self.public_modulus)) % self.size
            if rr == 0:
                pass
                #goes to the while ss = 0 loop with ss = 0
            else:
                ss = ((self.message + self.secret_exponent*rr)* pow(random_int, -1, self.size)) % self.size
        return [rr, ss]
        