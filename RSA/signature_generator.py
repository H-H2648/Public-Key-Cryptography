from utils.helpers import modular_exponent

class Signature_Generator:
    def __init__(self, public_key, secret_key, message):
        self.public_modulus = public_key[0]
        self.secret_exponent = secret_key[2]
        self.message = message

                
    def generate_signature(self):
        return modular_exponent(self.message, self.secret_exponent, self.public_modulus)