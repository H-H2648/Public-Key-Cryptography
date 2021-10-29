import math

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
                    return ii + jj*sqrt_size

#2, 0, 
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
            x_index, m_index, n_index = transform(x_index, m_index, n_index)
            ##apply transform twice
            x_2index, m_2index, n_2index = transform(x_2index, m_2index, n_2index)
            x_2index, m_2index, n_2index = transform(x_2index, m_2index, n_2index)
            print(x_index, m_index, n_index )
            print(x_2index, m_2index, n_2index)
            if x_index == x_2index:
                if m_index == m_2index and group_element != 1:
                    print("probably wrong")
                return ((m_index - m_2index)*pow(n_2index - n_index, -1, self.size)) % self.size


