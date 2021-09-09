class Encryptor:
    def __init__(self, public_key, message):
        self.public_modulus = public_key[0]
        self.public_exponent = public_key[1]
        self.message = message
    
    def modular_exponent(num, mod, power):
        exponent_2 = 0
        power_2 = 1
        power_num = 1
        while power_2 <= power:
            power_2 *=2
            exponent_2 +=1
        
        