from key_generator import Key_Generator
from encryptor import Encryptor
from decryptor import Decryptor

if __name__ == '__main__':
    RSA_Generator = Key_Generator(8, prime_1 = 233, prime_2 = 211, public_exponent = 20771)
    pub_key = RSA_Generator.get_key()
    RSA_Encryptor = Encryptor(pub_key, 123)
    cipher = RSA_Encryptor.encrypt()
    secret_exponent = RSA_Generator.secret_key[2]
    RSA_Decryptor = Decryptor(cipher, pub_key[0], secret_exponent)
    print(RSA_Decryptor.decrypt())