class Algorithm:
    def __init__(self, buyers, seller, max_iter=1000, tol=1e-6):
        self.buyers = buyers
        self.seller = seller
        self.max_iter = max_iter
        self.tol = tol
        self.p_records = []
        self.el_records = []
        self.w_records = []
        self.utility_records = []

    def compute_buyer_utility(self, r, c, mu, f, w):
        """Calculate buyer utility function (Equation 2 from paper)"""
        return -(r * c / f + mu * w)

    def run(self):
        pass


"""
Proposing two ways to iterate  the BIDPRIM ALGORITHMS:
    1) initialize unit_p with const num 1
    2) allocate fmax evenly frist then calculating the p
"""


class BidPrim(Algorithm):

    def __init__(self, buyers, seller):
        super().__init__(buyers, seller)

    def run(self):
        # 1. Initialize the unit_price p using const 1
        # p = 1
        # or  Initialize the unit_price p using allocate fmax evenly first
        p = sum(
            [
                (fmax - e) * r * c / (mu * fmax * e * e)
                for j in range(len(self.buyers))
                for r, c, mu, fmax, e in [
                    (
                        self.buyers[j].r,
                        self.buyers[j].c,
                        self.buyers[j].mu,
                        self.seller.fmax,
                        self.seller.fmax / len(self.buyers),
                    )
                ]
            ]
        ) / len(self.buyers)

        # 2. iteratating
        for i in range(self.max_iter):

            # buyer's resouce allocation amount according to lemma3
            el = [
                (-r * c + ((r * c) ** 2 + 4 * mu * fmax**2 * r * c * p) ** 0.5)
                / (2 * mu * fmax * p)
                for buyer in self.buyers
                for r, c, mu, fmax in [(buyer.r, buyer.c, buyer.mu, self.seller.fmax)]
            ]

            # update p according to lemma4
            p_new = sum(p * e for e in el) / self.seller.fmax

            # recording each round data (price p, resource allocation el, paying w, utility)
            self.p_records.append(p_new)
            self.el_records.append(el)
            self.w_records.append([e * p_new for e in el])
            self.utility_records.append(
                [
                    self.compute_buyer_utility(
                        self.buyers[j].r,
                        self.buyers[j].c,
                        self.buyers[j].mu,
                        self.el_records[i][j],
                        self.w_records[i][j],
                    )
                    for j in range(len(self.buyers))
                ]
            )

            # check if price difference is small enough, stop iteration
            if abs(p_new - p) < self.tol:
                # write ending records into buyers
                for k in range(len(self.buyers)):
                    self.buyers[k].f = self.el_records[i][k]
                    self.buyers[k].w = self.w_records[i][k]
                    self.buyers[k].utility = self.utility_records[i][k]
                break

            # else continue iteration
            p = p_new

    def output(self):
        print(self.p_records[-1])
        print(sum(self.w_records[-1]) / self.seller.fmax)


class UniPrim(Algorithm):
    def __init__(self, buyers, seller):
        super().__init__(buyers, seller)

    def run(self):

        # 1. calculate the p according to theorm2
        p = (
            (
                sum(
                    [
                        (r * c / mu) ** 0.5 / fmax * fmax
                        for buyer in self.buyers
                        for r, c, mu, fmax in [
                            (buyer.r, buyer.c, buyer.mu, self.seller.fmax)
                        ]
                    ]
                )
            )
            ** 2
        ) / (self.seller.fmax * self.seller.fmax)

        # 2. calculate the wi* for each buyer
        self.w_records = [
            (r * c * p / mu) ** 0.5
            for buyer in self.buyers
            for r, c, mu in [(buyer.r, buyer.c, buyer.mu)]
        ]

        # 3. write records to buyer and seller
        for i, buyer in enumerate(self.buyers):
            buyer.w = self.w_records[i]
        self.seller.unit_price = p

    def output(self):
        print(sum(self.w_records) / self.seller.fmax)
        print(self.seller.unit_price)
