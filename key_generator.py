import numpy as np  

class Key_Generator:
    def __init__(self, bit_size, prime_1=None, prime_2=None, public_exponent = None):
        self.bit_size  = bit_size
        if not(prime_1 is None):
            self.prime_1 = prime_1
        if not(prime_2 is None):
            self.prime_2 = prime_2
        if not(public_exponent is None):
            self.public_exponent = public_exponent
    
    def generate_random_prime(self):
        #not implemented yet
        pass

    def generate_random_coprime(self, num):
        #not implemented yet
        #intention: generate random value coprime to self.phi_public_modulus
        pass

    
    #assumes num < modulus (otherwise it should be num % modulus)
    def multiplicative_inverse(self, num, modulus):
        before_linear_coefficients = np.array([1, 0])
        before_val = modulus
        now_linear_coefficients = np.array([0, 1])
        now_val = num
        while (now_val > 1):
            quotient = before_val //now_val
            before_linear_coefficients, now_linear_coefficients = now_linear_coefficients, before_linear_coefficients - quotient*now_linear_coefficients
            before_val, now_val = now_val, before_val - quotient*now_val
        if (now_val != 1):
            raise("SOMETHING WENT WRONG")
        return now_linear_coefficients[1] % modulus



    def get_key(self):
        if not(hasattr(self, 'prime_1')):
            self.prime_1 = self.generate_random_prime()
        if not(hasattr(self, 'prime_2')):
            self.prime_2 = self.generate_random_prime()
        #in case we get the same prime, generate again
        while (self.prime_1 == self.prime_2):
            self.prime_2 = self.generate_random_prime()
        self.public_modulus = self.prime_1*self.prime_2
        self.phi_public_modulus = (self.prime_1 - 1)*(self.prime_2 - 1)
        if not(hasattr(self, 'public_exponent')):
            self.public_exponent = self.generate_random_coprime(self.phi_public_modulus)
        self.secret_exponent = self.multiplicative_inverse(self.public_exponent, self.phi_public_modulus)
        self.public_key = [self.public_modulus, self.public_exponent]
        self.secret_key = [self.prime_1, self.prime_2, self.secret_exponent]
        print(self.public_key)
        print(self.secret_key)
        return self.public_key
