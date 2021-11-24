from key_generator import Key_Generator
from encryptor import Encryptor
from decryptor import Decryptor
from signature_generator import Signature_Generator
from signature_verifier import Signature_Verifier

from utils.helpers import is_prime

if __name__ == '__main__':
    message = 37917
    RSA_Generator = Key_Generator(16, 233, 211, 20771)
    pub_key = RSA_Generator.get_key()
    print(f"public key: {pub_key}")
    RSA_Encryptor = Encryptor(pub_key, 37917)
    RSA_signature_generator = Signature_Generator(pub_key, RSA_Generator.secret_key, message)
    cipher = RSA_Encryptor.encrypt()
    signature = RSA_signature_generator.generate_signature()
    print(f"cipher: {cipher}")
    print(f"signature: {signature}")
    print(f"secret key: {RSA_Generator.secret_key}")
    secret_exponent = RSA_Generator.secret_key[2]
    RSA_Decryptor = Decryptor(cipher, pub_key[0], secret_exponent)
    print(f"decripted message: {RSA_Decryptor.decrypt()}")
    RSA_signature_verifier = Signature_Verifier(RSA_Decryptor.decrypt(), pub_key)
    print(f"signature verification: {RSA_signature_verifier.verify_signature(signature)}")