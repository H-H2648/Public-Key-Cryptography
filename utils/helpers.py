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