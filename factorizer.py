from utils.helpers import modular_exponent, gcd_multiplicative_inverse

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
        # print(factor_finder-1)
        # print(num)
        # print( gcd_multiplicative_inverse(factor_finder - 1, num))
        factor = gcd_multiplicative_inverse(factor_finder - 1, num)[0]
        if 1 < factor and factor < num:
            return factor
        else:
            return -1
        
