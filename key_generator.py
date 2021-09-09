import numpy as np  
import scipy

from utils.helpers import generate_random_prime, generate_random_coprime

class Key_Generator:
    def __init__(self, bit_size, prime_1=None, prime_2=None, public_exponent = None):
        self.bit_size  = bit_size
        if not(prime_1 is None):
            self.prime_1 = prime_1
        if not(prime_2 is None):
            self.prime_2 = prime_2
        if not(public_exponent is None):
            self.public_exponent = public_exponent


    




    def get_key(self):
        if not(hasattr(self, 'prime_1')):
            self.prime_1 = generate_random_prime()
        if not(hasattr(self, 'prime_2')):
            self.prime_2 = generate_random_prime()
        #in case we get the same prime, generate again
        while (self.prime_1 == self.prime_2):
            self.prime_2 = generate_random_prime()
        self.public_modulus = self.prime_1*self.prime_2
        self.phi_public_modulus = (self.prime_1 - 1)*(self.prime_2 - 1)
        if not(hasattr(self, 'public_exponent')):
            self.public_exponent = generate_random_coprime(self.phi_public_modulus)
        self.secret_exponent = multiplicative_inverse(self.public_exponent, self.phi_public_modulus)
        self.public_key = [self.public_modulus, self.public_exponent]
        self.secret_key = [self.prime_1, self.prime_2, self.secret_exponent]
        return self.public_key
