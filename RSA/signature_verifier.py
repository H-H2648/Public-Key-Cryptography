from utils.helpers import modular_exponent

class Signature_Verifier:
    def __init__(self, message, public_key):
        self.public_modulus = public_key[0]
        self.public_exponent = public_key[1]
        self.message = message

                
    def verify_signature(self, signature):
        return (self.message == modular_exponent(signature, self.public_exponent, self.public_modulus))