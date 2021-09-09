from key_generator import Key_Generator
from encryptor import Encryptor

if __name__ == '__main__':
    RSA_Generator = Key_Generator(8, prime_1 = 233, prime_2 = 211, public_exponent = 20771)
    pub_key = RSA_Generator.get_key()
    RSA_Encryptor = Encryptor(pub_key, 123)
    print(RSA_Encryptor.encrypt())