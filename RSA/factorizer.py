from utils.helpers import modular_exponent, gcd_multiplicative_inverse, is_prime, is_B_smooth, dependent_rows
import random
import math
import numpy as np

class Factorizer:
    def __init__(self):
        pass

    #Assumes num is composite and is larger than 3 (can check if N is prime with isPrime)
    #B is some B such that for p - 1 = p_1^{e_1}...p_k^{e_k}, B > p_i^{e_i} for all i (where p | N)
    #This factorizer can fail for small B (when B fails the above constraint)
    #This factorizer can fail for a given choice of B when this propertyholds for all such p | N
    #if this returns -1, it means it did not find the factorizer.
    def pollard_factorize(self, num, B):
        factor_finder = 2
        for ii in range(2, B + 1):
            factor_finder = modular_exponent(factor_finder, ii, num)
    
        factor = gcd_multiplicative_inverse(factor_finder - 1, num)[0]
        if 1 < factor and factor < num:
            return factor
        else:
            return -1

    def random_square_factorize(self, num, B):
        if num == 2:
            return -1
        if num % 2 == 0:
            return -1
        if num < 2:
            return -1
        #factor_basis_B: the set of primes less than B
        factor_basis_B = []
        for ii in range(2, B+1):
            if is_prime(ii):
                factor_basis_B.append(ii)
        matrix_of_exponents = np.zeros((len(factor_basis_B) + 1, len(factor_basis_B)))
        num_rows = len(factor_basis_B) + 1
        random_x_lst = []
        ##RELATION GENERATION STAGE
        for index in range(num_rows):
            val_is_B_smooth = False
            while not(val_is_B_smooth):
                random_x = random.randint(math.ceil(math.sqrt(num)), num - 1)
                random_x_squared = pow(random_x, 2, num)
                val_is_B_smooth, exponents = is_B_smooth(random_x_squared, factor_basis_B)
                if val_is_B_smooth:
                    matrix_of_exponents[index] = exponents
                    random_x_lst.append(random_x)
                
        ##LINEAR ALGEBRA STAGE
        matrix_of_exponents_modulo_2 = np.remainder(matrix_of_exponents, 2)
        linearly_dependent_rows = dependent_rows(matrix_of_exponents_modulo_2)
        sum_of_dependent_exponents = np.zeros(len(factor_basis_B))
        for row in linearly_dependent_rows:
            sum_of_dependent_exponents += matrix_of_exponents[row]
        desired_exponents = sum_of_dependent_exponents // 2
        X = 1
        for row in linearly_dependent_rows:
            X *= random_x_lst[row]
        Y = 1
        for index in range(len(factor_basis_B)):
            Y*= factor_basis_B[index]**(desired_exponents[index])
        possible_factor, _ = gcd_multiplicative_inverse(X-Y, num)
        if 1 < possible_factor and possible_factor < num:
            return int(possible_factor)
        else:
            return -1
            



        
        
