class Signature_Verifier:
    def __init__(self, message, public_key):
        self.public_modulus = public_key[0]
        self.size = public_key[1]
        self.generator = public_key[2]
        self.some_value = public_key[3]
        self.message = message

                
    def verify_signature(self, signature):
        return (pow(self.generator, self.message, self.public_modulus) == ((pow(self.some_value, signature[0], self.public_modulus)*pow(signature[0], signature[1], self.public_modulus))% self.public_modulus))

    def verify_signature_DSA(self, signature):
        w = pow(signature[1], -1, self.size)
        u1 = (self.message*w)% self.size
        u2 = (signature[0]*w)% self.size
        temp_v = ((pow(self.generator, u1, self.public_modulus)*pow(self.some_value, u2, self.public_modulus)) % self.modulus) % self.size
        return (signature[0] == temp_v)
