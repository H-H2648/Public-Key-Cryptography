class Decryptor:
    def __init__(self, public_key, secret_key, cipher):
        self.public_modulus = public_key[0]
        self.size = public_key[1]
        self.generator = public_key[2]
        self.some_value = public_key[3]
        self.secret_key = secret_key
        self.cipher = cipher
    
    def decrypt(self):
        return (self.cipher[1]*pow(self.cipher[0], -self.secret_key, self.public_modulus)) % self.public_modulus