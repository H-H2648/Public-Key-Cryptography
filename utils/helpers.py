import math
import random
import numpy as np

#assumes num < modulus (otherwise it should be num % modulus)
#returns (gcd of num and modulus, multiplicative inverse of num % modulus)
def gcd_multiplicative_inverse(num, modulus):
    before_linear_coefficients = np.array([1, 0])
    before_val = modulus
    now_linear_coefficients = np.array([0, 1])
    now_val = num
    while (now_val > 0):
        quotient = before_val //now_val
        before_linear_coefficients, now_linear_coefficients = now_linear_coefficients, before_linear_coefficients - quotient*now_linear_coefficients
        before_val, now_val = now_val, before_val - quotient*now_val
    # if (now_val != 1):
    #     raise("SOMETHING WENT WRONG")
    #before_val represents gcd
    return before_val, before_linear_coefficients[1] % modulus


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
    return random.randint(0, 2**(bit_size)-1)

def power2Odd(val):
    power_2_count = 0
    while val % 2 == 0:
        val /= 2
        power_2_count +=1
    return power_2_count, val

#Used only within a for loop to see if it should continue or not
#if True, we can skip (it might be a prime)
#if False.. end loop because it is not a prime
def is_prime_helper(composite_check, power_2_count, val):
    for _ in range(power_2_count - 1):
        composite_check = modular_exponent(composite_check, 2, val)
        if composite_check == val - 1:
            return True
    return False


#Miller Test
#Should be good enough under the Genereal Riemann Hypothesis
def is_prime(val):
    if val == 2:
        return True
    if val % 2 == 0:
        return False
    power_2_count, biggest_odd_factor_sub1 = power2Odd(val-1)
    for trial in range(2, min(val-2, int(2*math.log(val)**2)) + 1):
        composite_check =  modular_exponent(trial, biggest_odd_factor_sub1, val)
        if (composite_check == 1) or (composite_check == val - 1):
            continue
        if is_prime_helper(composite_check, power_2_count, val):
            continue
        else:
            return False
    return True


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
    val = random.randint(1, num-1)
    while not(is_coprime(num, val)):
        val = random.randint(1, num-1)
    return val
    
    #not implemented yet
    #intention: generate random value coprime to self.phi_public_modulus
    pass

#assumes gcd(a, n) = 1
def jacobi_compute_helper(a, n, prod_so_far):
    while True:
        if a % 2 == 0:
            prod_so_far *= (-1)**((n**2 - 1)/8)
            a /= 2
            a = int(a)
            prod_so_far = int(prod_so_far)
        elif a > n:
            a = a %  n 
        elif a == 1:
            return prod_so_far
        elif a == 2:
            return int(prod_so_far * (-1)**((n**2 - 1)/8))
        else:
            prod_so_far *= (-1)**(((a-1)/2)*((n-1)/2))
            prod_so_far = int(prod_so_far)
            a, n = n, a
    
def jacobi_compute(a, n):
    gcd, _ = gcd_multiplicative_inverse(a, n)
    if gcd > 1:
        return 0
    return jacobi_compute_helper(a, n, 1)

def is_B_smooth(N, B_prime_lst):
    # B_prime_lst = []
    # for pos_prime in range(2, B + 1):
    #     if is_prime(pos_prime):
    #         B_prime_lst.append(pos_prime)
    index = 0
    factor_lst = []
    for _ in range(len(B_prime_lst)):
        factor_lst.append(0)
    while index < len(B_prime_lst):
        prime = B_prime_lst[index]
        if (N % prime) == 0:
            factor_lst[index] +=1
            N = N//prime
        else:
            index +=1
    if N > 1:
        return False, None
    else:
        return True, factor_lst



#assumes numbers are binary
#find linearly dependent rows
def dependent_rows(array):
    array_copy = np.copy(array)
    #assumes index < len(array[0]) (the number of columns)
    #when index is called, it assumes column 0, 1, ..., index - 1 has already been upper triangulized
    def upper_triangulize_helper(array, array_order, index):
        column = array[:, index]
        #where there is 1 in the column
        pos_1s = np.where(column[index:] > 0)[0]
        if len(pos_1s) == 0:
            return 
        else:
            #the first occurence of 1 in the column
            pos_1 = pos_1s[0] + index
            array[[index, pos_1]] = array[[pos_1, index]]
            array_order[[index, pos_1]] = array_order[[pos_1, index]]
            for row in range(index + 1, len(array)):
                if array[row][index] == 1:
                    array[row] = (array[row] + array[index]) % 2
                    array_order[row] = (array_order[row] + array_order[index]) % 2

    array_order = np.identity(len(array))
    for index in range(len(array[0])):
        upper_triangulize_helper(array_copy, array_order, index)

    return np.where(array_order[-1] == 1)[0]
    


        





