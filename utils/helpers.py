#assumes num < mod
#exponentiation by squaring..
def modular_exponent(num, power, mod):
    if power == 0:
        return 1
    else:
        power_2_lst = [1]
        power_num_lst = [num]
        while power_2_lst[-1] < power:
            power_2_lst.append(power_2_lst[-1]*2)
            power_num_lst.append((power_num_lst[-1] * power_num_lst[-1]) % mod )
        exp = 1
        #x^{2^{a_n} + ... + 2^{a_0}} = x^{2^{a_n}}*...*x^{2^{a_0}}
        #we keep track of all x^{2^k}s in power_num_lst
        while power > 0:
            if power_2_lst[-1] <= power:
                power -= power_2_lst[-1]
                exp *= power_num_lst[-1]
                exp %= mod
            power_2_lst = power_2_lst[:-1]
            power_num_lst = power_num_lst[:-1]
        return exp

def generate_random_number_bit(bit_size):
    return scipy.stats.randint(0, 2**(bit_size)-1)

def is_prime(val):
    #not implemented yet
    pass

def generate_random_prime(bit_size):
    possible_prime = generate_random_number_bit(bit_size)
    while not(is_prime(possible_prime)):
        possible_prime = generate_random_number_bit(bit_size)
    prime = possible_prime
    return prime

def is_coprime(num, val):
    if val == 1:
        return True
    while val > 1:
        num, val = val, num % val
    if val == 1:
        return True
    if val == 0:
        return False
        


def generate_random_coprime(num):
    val = scipy.stats.randomint(1, num-1)
    while not(is_coprime(num, val)):
        val = scipy.stats.randomint(1, num-1)
    return val
    
    #not implemented yet
    #intention: generate random value coprime to self.phi_public_modulus
    pass


#assumes num < modulus (otherwise it should be num % modulus)
def multiplicative_inverse(num, modulus):
    before_linear_coefficients = np.array([1, 0])
    before_val = modulus
    now_linear_coefficients = np.array([0, 1])
    now_val = num
    while (now_val > 1):
        quotient = before_val //now_val
        before_linear_coefficients, now_linear_coefficients = now_linear_coefficients, before_linear_coefficients - quotient*now_linear_coefficients
        before_val, now_val = now_val, before_val - quotient*now_val
    if (now_val != 1):
        raise("SOMETHING WENT WRONG")
    return now_linear_coefficients[1] % modulus

