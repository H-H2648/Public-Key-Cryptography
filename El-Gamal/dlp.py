import math
import random
import numpy as np
from utils.helpers import gcd_multiplicative_inverse, is_prime, prime_factorization, is_B_smooth, solve_linear_algebra, latex_print, latex_print_array

class DLP:
    def __init__(self, modulus, size, generator):
        self.modulus = modulus
        self.size = size
        self.generator = generator
    
    #looks for x such that (generator)^x = group_element
    def shanks_DLP(self, group_element):
        sqrt_size = int(math.sqrt(self.size))
        inverse_power_sqrt = pow(self.generator, -sqrt_size, self.modulus)
        #we wish to find generator^ii = group_element*inverse_power_sqrt^jj
        ii_lst = []
        jj_lst = []
        power_g = 1
        for ii in range(sqrt_size):
            ii_lst.append(power_g)
            power_g = (power_g * self.generator) % self.modulus
        power_h_gm = group_element
        for jj in range(sqrt_size + 1):
            jj_lst.append(power_h_gm)
            power_h_gm = (power_h_gm * inverse_power_sqrt) % self.modulus
        for ii in range(sqrt_size):
            for jj in range(sqrt_size + 1):
                if ii_lst[ii] == jj_lst[jj]:
                    print(f"equality found: {(ii, jj)}")
                    return ii + jj*sqrt_size

    def pollard_DLP(self, group_element):


        def transform(x, m, n):
            if x < self.modulus/3:
                return (group_element * x) % self.modulus, m, (n+1) % self.size
            if self.modulus/3 <= x and x < self.modulus/3*2:
                return (x * x) % self.modulus, (2*m) % self.size , (2*n) % self.size
            else:
                return (self.generator*x) % self.modulus, (m + 1) % self.size, n

        x_index, m_index, n_index = 1, 0, 0
        x_2index, m_2index, n_2index = 1, 0, 0
        while True:
            if (x_index == group_element) and (n_index == 0):
                return m_index
            if (x_2index == group_element) and (n_2index == 0):
                return m_2index
            x_index, m_index, n_index = transform(x_index, m_index, n_index)
            ##apply transform twice
            x_2index, m_2index, n_2index = transform(x_2index, m_2index, n_2index)
            x_2index, m_2index, n_2index = transform(x_2index, m_2index, n_2index)
            if x_index == x_2index:
                if gcd_multiplicative_inverse(n_2index-n_index, self.size)[0] > 1:
                    m_index, n_index = random.randint(0, self.size-1), random.randint(0, self.size-1)
                    x_index = (pow(self.generator, m_index, self.modulus) * pow(group_element, n_index, self.modulus)) % self.modulus
                    x_2index, m_2index, n_2index = x_index, m_index, n_index
                else:

                    return ((m_index - m_2index)*pow(n_2index - n_index, -1, self.size)) % self.size

    #assumes self.modulus is relatively small and can be factored in reasonable amount of time
    def pohlig_hellman_DLP(self, group_element):
        prime_dict = prime_factorization(self.size)
        congruences = []
        for prime in prime_dict:
            power = prime_dict[prime]
            prime_power = pow(prime, power)
            leftover = self.size//prime_power
            temp_generator = pow(self.generator, leftover, self.modulus)
            temp_group_element = pow(group_element, leftover, self.modulus)
            temp_DLP = DLP(self.modulus, prime_power, temp_generator)
            # log = temp_DLP.pollard_DLP(temp_group_element)
            log = temp_DLP.prime_power_dlp(temp_group_element, prime)
            congruences.append((log, leftover, prime_power))
        #applying Chinese Remainder Theorem
        final_log = 0
        for log, leftover, prime_power in congruences:
            final_log += log*leftover*pow(leftover, -1, prime_power)
            final_log %= self.size
        return final_log
        




        

    #self.modulus must be some prime power
    def prime_power_dlp(self, group_element, prime):
        #self.size = p^e
        #so prime = self.size + 1=
        power = int(math.log(self.size)/math.log(prime))
        inv_prime_power_generator_array = [0]*power
        for jj in range(power):
            if jj == 0:
                inv_prime_power_generator = pow(self.generator, -1, self.modulus)
            else:
                inv_prime_power_generator = pow(inv_prime_power_generator, prime, self.modulus)
            inv_prime_power_generator_array[jj] = inv_prime_power_generator
        
        digits = [0]*power
        #gamma_arrays consists of gammas, where gamma_j = generator^(sum (i = j, ..., power - 1): d_jprime^j)
        #where logarithm (the desired output) = sum i = 0 to power - 1: d_jprime^j (d_j is the jth digit of the prime-base representation of the logarithm)
        bar_generator = pow(self.generator, pow(prime, power - 1, self.size), self.modulus)



        for jj in range(power):
            if jj == 0:
                gamma = group_element
            else:
                gamma = (gamma*pow(inv_prime_power_generator_array[jj-1], digits[jj-1], self.modulus)) % self.modulus
            bar_gamma = pow(gamma, pow(prime, power - 1 -jj, self.size), self.modulus)
            helper_dlp_machine = DLP(self.modulus, prime, bar_generator)
            digit = helper_dlp_machine.pollard_DLP(bar_gamma)
            digits[jj] = digit
        prime_base =1
        output = 0
        for digit in digits:
            output += prime_base*digit
            prime_base *= prime
        return output

    def index_calculus_DLP(self, group_element, B, square_free = False, primes = None):
        factor_basis_B = []
        for ii in range(2, B+1):
            if is_prime(ii):
                factor_basis_B.append(ii)
        matrix_of_exponents = np.zeros((len(factor_basis_B) + 10, len(factor_basis_B)))
        num_rows = len(factor_basis_B) + 10
        random_x_lst = []
        random_x_powered_lst = []
        ##RELATION GENERATING STAGE
        for index in range(num_rows):
            val_is_B_smooth = False
            while not(val_is_B_smooth):
                random_x = random.randint(1, self.size-1)
                random_x_powered = pow(self.generator, random_x, self.modulus)
                val_is_B_smooth, exponents = is_B_smooth(random_x_powered, factor_basis_B)
                if val_is_B_smooth:
                    matrix_of_exponents[index] = exponents
                    random_x_lst.append(random_x)
                    random_x_powered_lst.append(random_x_powered)
        random_x_array = np.array(random_x_lst)
        random_x_powered_array = np.array(random_x_powered_lst)
        latex_print_array(random_x_array)
        latex_print_array(random_x_powered_array)

        ##LINEAR ALGEBRA STAGE
        matrix_of_exponents_modulo = np.remainder(matrix_of_exponents, self.size)
        random_xs_modulo = np.remainder(random_x_array, self.size)
        solution_modulo = solve_linear_algebra(matrix_of_exponents_modulo, random_xs_modulo, self.size)

        ##DISCRETE LOGARITHM FINDING STAGE
        val_is_B_smooth = False
        while not(val_is_B_smooth):
            random_y = random.randint(1, self.size - 1)
            logarithm_finder = (group_element*pow(self.generator, random_y, self.modulus))%self.modulus
            val_is_B_smooth, exponents = is_B_smooth(logarithm_finder, factor_basis_B)
        log =  (np.dot(np.array(exponents), solution_modulo) - random_y) % self.size
        return int(log)



