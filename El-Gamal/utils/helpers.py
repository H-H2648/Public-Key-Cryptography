import numpy as np
import math

#assumes num < modulus (otherwise it should be num % modulus)
#returns (gcd of num and modulus, multiplicative inverse of num % modulus)
def gcd_multiplicative_inverse(num, modulus):
    if num < 0:
        num = num + modulus
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

def power2Odd(val):
    power_2_count = 0
    while val % 2 == 0:
        val /= 2
        power_2_count +=1
    return int(power_2_count), int(val)

#Used only within a for loop to see if it should continue or not
#if True, we can skip (it might be a prime)
#if False.. end loop because it is not a prime
def is_prime_helper(composite_check, power_2_count, val):
    for _ in range(power_2_count - 1):
        composite_check = pow(composite_check, 2, val)
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
        composite_check =  pow(trial, biggest_odd_factor_sub1, val)
        if (composite_check == 1) or (composite_check == val - 1):
            continue
        if is_prime_helper(composite_check, power_2_count, val):
            continue
        else:
            return False
    return True

def prime_factorization(n):
    prime_dict = {}
    if is_prime(n):
        prime_dict[n] = 1
    else:
        for ii in range(2, n+1):
            if is_prime(ii):
                if (n % ii) == 0:
                    exponent = 0
                    while (n % ii) == 0:
                        n /= ii
                        exponent +=1
                    prime_dict[ii] = exponent
    return prime_dict

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


#upper triangulizes with respect to modulo p
#
def upper_triangulize(array, modulo):
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