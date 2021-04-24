

import numpy as np
def combfilter(b,a,factor):

    coef_len = len(b)

    new_len = coef_len + ( factor * ( coef_len - 1 ) )

    combf_a = np.zeros(new_len)
    combf_b = np.zeros(new_len)

    combf_a[::factor+1] = a
    combf_b[::factor+1] = b

    return combf_b,combf_a