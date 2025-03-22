"""
Here generating some data for base tesing.
"""

# data range
num_user_range = (0, 0)
r_range = (0, 0)
mu_range = (0, 0)
c_range = (0, 0)
fmax_range = (0, 0)

# static data for comparing the results from article
static_num_users = 5
static_rs = [1, 2, 8, 10, 15] * 8
static_mus = [1, 1.5, 2, 3, 5]
static_cs = [20000, 20000, 31680, 31680, 2640]  # needed cycles per one bit
static_fmax = 8 * 10**3  # GHz
