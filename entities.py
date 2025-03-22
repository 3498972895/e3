class Buyer:
    def __init__(self, r, mu, c):
        """
        :param r: Data volume (bits)
        :param mu: Payment sensitivity
        :param c: Computational density (cycles/bit)
        """
        self.r = r
        self.mu = mu
        self.c = c
        self.f = 0.0  # Allocated CPU resource (Hz), dynamically allocated by Seller
        self.w = 0.0  # Money for bidding
        self.utility = 0.0  # Utility value


class Seller:
    def __init__(self, fmax):
        """
        :param fmax:The maximum number of requests that can be served per time unit.
        """
        self.fmax = fmax
        self.unit_price = 0
