from key_generator import Key_Generator

if __name__ == '__main__':
    Generator = Key_Generator(8, prime_1 = 233, prime_2 = 211, public_exponent = 20771)
    Generator.get_key()