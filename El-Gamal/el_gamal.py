from key_generator import Key_Generator
from encryptor import Encryptor
from decryptor import Decryptor
from signature_generator import Signature_Generator
from signature_verifier import Signature_Verifier

if __name__ == '__main__':
    # el_gamal_Generator = Key_Generator(3967526699, 3967526698, 2, secret_key = 596305913)
    # pub_key = el_gamal_Generator.get_key()
    # print(f"public key: {pub_key}")
    # print(f"h: {pub_key[3]}")
    # message = 37917
    el_gamal_Generator = Key_Generator(6, 3, 2)
    pub_key = el_gamal_Generator.get_key()
    print(f"public key: {pub_key}")
    print(f"h: {pub_key[3]}")
    message = 4
    el_gamal_Encryptor = Encryptor(pub_key, message)
    El_gamal_signature_generator = Signature_Generator(pub_key, el_gamal_Generator.secret_key, message)
    cipher = el_gamal_Encryptor.encrypt()
    print(f"cipher: {cipher}")
    print(f"secret key: {el_gamal_Generator.secret_key}")
    signature = El_gamal_signature_generator.generate_signature_DSA()
    print(f"signature: {signature}")
    secret_key = el_gamal_Generator.secret_key
    el_gamal_Decryptor = Decryptor(pub_key, secret_key, cipher)
    el_gamal_signature_verifier = Signature_Verifier(el_gamal_Decryptor.decrypt(), pub_key)
    print(f"signature verification: {el_gamal_signature_verifier.verify_signature_DSA(signature)}")