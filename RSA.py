from key_generator import Key_Generator
from encryptor import Encryptor
from decryptor import Decryptor

from utils.helpers import is_prime

if __name__ == '__main__':
    # for ii in range(2, 200):
    #     print(f'{ii}, {is_prime(ii)}')
    RSA_Generator = Key_Generator(8)
    pub_key = RSA_Generator.get_key()
    print(pub_key)
    RSA_Encryptor = Encryptor(pub_key, 123)
    cipher = RSA_Encryptor.encrypt()
    print(cipher)
    print(RSA_Generator.secret_key)
    secret_exponent = RSA_Generator.secret_key[2]
    RSA_Decryptor = Decryptor(cipher, pub_key[0], secret_exponent)
    print(RSA_Decryptor.decrypt())