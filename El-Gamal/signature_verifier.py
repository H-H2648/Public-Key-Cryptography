class Signature_Verifier:
    def __init__(self, message, public_key):
        self.public_modulus = public_key[0]
        self.generator = public_key[2]
        self.some_value = public_key[3]
        self.message = message

                
    def verify_signature(self, signature):
        return (pow(self.generator, self.message, self.public_modulus) == ((pow(self.some_value, signature[0], self.public_modulus)*pow(signature[0], signature[1], self.public_modulus))% self.public_modulus))