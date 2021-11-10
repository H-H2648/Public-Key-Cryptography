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
def solve_linear_algebra(coefficients, output, modulo):
    #assumes index < len(array[0]) (the number of columns)
    #when index is called, it assumes column 0, 1, ..., index - 1 has already been upper triangulized
    def upper_triangulize_helper(array, output, index):
        column = array[:, index]
        coprime_ind = -1
        for ii in range(index, len(column)):
            if (column[ii] > 0 and gcd_multiplicative_inverse(column[ii], modulo)[0] == 1):
                coprime_ind = ii
                break
        if coprime_ind == -1:
            return -1


        else:
            array[[index, coprime_ind]] = array[[coprime_ind, index]]
            output[[index, coprime_ind]] = output[[coprime_ind, index]]
            # print(array.astype(int))
            # print(output.astype(int))
            #so we have 1 on the main diagonal
            const = int(array[index][index])
            array[index] = np.remainder(array[index]*pow(const, -1, modulo),  modulo)
            output[index] = np.remainder(output[index]*pow(const, -1, modulo),  modulo)
            # print(array.astype(int))
            # print(output.astype(int))
            for row in range(index + 1, len(array)):
                if array[row][index] > 0:
                    const = array[row][index]
                    array[row] = (array[row] - const*array[index]) % modulo
                    output[row] = (output[row] - const*output[index]) % modulo
                    # print(array.astype(int))
                    # print(output.astype(int))


    for index in range(len(coefficients[0])):
        #fails when there is no coprime to modulus in the column (should rarely happen)
        if upper_triangulize_helper(coefficients, output, index) == -1:
            return -1

    #linearly dependent
    for index in range(len(coefficients[0])):
        if coefficients[index][index] == 0:
            return -1

    solution = np.zeros(len(coefficients[0]))
    for index in range(len(coefficients[0])-1, -1, -1):
        solution[index] = output[index]
        for temp_index in range(len(coefficients[0])-1, index, -1):
            solution[index] = ((solution[index] - solution[temp_index]*coefficients[index][temp_index]) % modulo)
    return solution.astype(int)


