import random


#assumes the group is the multiplicative group modulo G
#for the sake of completion, size must be specified (but since we assume we work with mod G, the size is implicit (phi(G)))
#generator must be specified
class Key_Generator:
    def __init__(self, modulo, size, generator, secret_key = None):
        self.modulo = modulo
        self.size = size
        self.generator = generator
        if not(secret_key is None):
            self.secret_key = secret_key
        
    def get_key(self):
        if not(hasattr(self, 'secret_key')):
            self.secret_key = random.randint(1, self.size - 1)
        self.some_value = pow(self.generator, self.secret_key, self.modulo)
        self.public_key = [self.modulo, self.size, self.generator, self.some_value]
        return self.public_key

        