from key_generator import Key_Generator
from encryptor import Encryptor
from decryptor import Decryptor

if __name__ == '__main__':
    el_gamal_Generator = Key_Generator(3967526699, 3967526698, 2, secret_key = 596305913)
    pub_key = el_gamal_Generator.get_key()
    print(f"public key: {pub_key}")
    print(f"h: {pub_key[3]}")
    message = 12345
    print(f"message: {message}")
    el_gamal_Encryptor = Encryptor(pub_key, message)
    cipher = el_gamal_Encryptor.encrypt()
    print(cipher)
    print(el_gamal_Generator.secret_key)
    secret_key = el_gamal_Generator.secret_key
    el_gamal_Decryptor = Decryptor(pub_key, secret_key, cipher)
    print(el_gamal_Decryptor.decrypt())