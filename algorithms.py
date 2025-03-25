class Algorithm:
    def __init__(self, buyers, seller):
        self.buyers = buyers
        self.seller = seller
        self.w_records = []
        self.el_records = []
        self.buyer_utility_records = []
        self.p_records = []
        self.seller_utility_record = []

    def compute_buyer_utility(self, r, c, mu, f, w):
        """Calculate buyer utility function (Equation 2 from paper)"""
        return -(r * c / f + mu * w)

    def run(self):
        pass

    def output(self, algorithm_name):
        print(f"{algorithm_name}:")
        if isinstance(self.w_records[-1], list):
            print(f"buyer's cost {self.w_records[-1]}")
        else:
            print(f"buyer's cost {self.w_records}")

        if isinstance(self.el_records[-1], list):
            print(f"buyer's resource allocation {self.el_records[-1]}")
        else:
            print(f"buyer's resource allocation {self.el_records}")

        if isinstance(self.buyer_utility_records[-1], list):
            print(f"buyer's utility {self.buyer_utility_records[-1]}")
        else:
            print(f"buyer's utility {self.buyer_utility_records}")

        print(f"seller's unit_price {self.p_records[-1]}")
        print(f"seller's utility {self.seller_utility_record[-1]}")


class BidPrim(Algorithm):
    """
    Proposing two ways to iterate  the BIDPRIM ALGORITHMS:
        1) initialize unit_p with const num 1
        2) allocate fmax evenly frist then calculating the p
    """

    def __init__(self, buyers, seller, max_iter=1000, tol=1e-6):
        super().__init__(buyers, seller)
        self.max_iter = max_iter
        self.tol = tol

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

            # 2.1 update p according to lemma4
            p_new = sum(p * e for e in el) / self.seller.fmax

            """
            2.2 Recording each round data
            (price p, resource allocation el, paying w, buyer's utility, seller's utility)
            """
            self.p_records.append(p_new)
            self.el_records.append(el)
            self.w_records.append([e * p_new for e in el])
            self.buyer_utility_records.append(
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
            self.seller_utility_record.append(sum(self.w_records[-1]))

            # 2.3 check if price difference is small enough, stop iteration
            if abs(p_new - p) < self.tol:
                break
            # else continue iteration
            p = p_new


class UniPrim(Algorithm):
    """
    This algorithm only has a single round to find equilibrium.
    """

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

        # 3. calculate each buyer allocated resource
        self.el_records = [w / p for w in self.w_records]

        # 4. calculate each buyer utility
        self.buyer_utility_records = [
            self.compute_buyer_utility(r, c, mu, f, w)
            for i in range(len(self.buyers))
            for r, c, mu, f, w in [
                (
                    self.buyers[i].r,
                    self.buyers[i].c,
                    self.buyers[i].mu,
                    self.el_records[i],
                    self.w_records[i],
                )
            ]
        ]

        # 5. write records to buyer and seller
        self.p_records.append(p)

        # 5. calculate the seller utility
        self.seller_utility_record.append(sum(self.w_records))


class FaidPrim(Algorithm):
    def __init__(self, buyers, seller, fairness_factor):
        super().__init__(buyers, seller)
        self.fairness_factor = fairness_factor
        self.difference_price_set = []

    def run(self):
        # 1. calculte all buyer's ai for needs of Theorem3
        buyers_ai = [
            (r * c / mu) ** 0.5
            for buyer in self.buyers
            for r, c, mu in [(buyer.r, buyer.c, buyer.mu)]
        ]

        # 2. generate powerset of buyers
        from itertools import chain, combinations

        powerset = [
            list(item)
            for item in list(
                chain.from_iterable(
                    combinations(list(range(len(self.buyers))), r)
                    for r in range(len(self.buyers) + 1)
                )
            )
        ]

        # 3. getting two sets makes the smallest divisions between them
        divisions = 99999999999999999
        divisions_set = []
        for i in range(len(powerset)):
            p_index_a = i
            for j in range(len(powerset)):
                p_index_b = j
                if set(powerset[p_index_a]).isdisjoint(
                    set(powerset[p_index_b])
                ) and set(powerset[p_index_a]).union(set(powerset[p_index_b])) == set(
                    list(range(len(self.buyers)))
                ):
                    temp_division = abs(
                        sum(buyers_ai[b_index] for b_index in powerset[p_index_a])
                        - sum(buyers_ai[b_index] for b_index in powerset[p_index_b])
                    )
                    if temp_division < divisions:
                        divisions = temp_division
                        divisions_set = [i, j]

        # 4. calculate alpha and beta
        alpha = sum(buyers_ai[b_index] for b_index in powerset[divisions_set[0]])
        beta = sum(buyers_ai[b_index] for b_index in powerset[divisions_set[1]])

        # 5. calculate the pi according to formula 22)
        f = self.fairness_factor
        fmax = self.seller.fmax
        pi_a = ((alpha + beta * f**0.5) / fmax) ** 2
        pi_b = ((alpha + beta * f**0.5) / ((f**0.5) * fmax)) ** 2

        # union pi and their divisions_set
        pd = [(pi_a, divisions_set[0]), (pi_b, divisions_set[1])]

        # # 6. calculate each buyer cost wi* according to formula 19)
        self.w_records = [0] * len(self.buyers)
        for pi, devision in pd:
            for b_index in powerset[devision]:
                r = self.buyers[b_index].r
                c = self.buyers[b_index].c
                mu = self.buyers[b_index].mu
                self.w_records[b_index] = (r * c * pi / mu) ** 0.5

        # 7. calculate each buyer's allocated resource
        self.el_records = [0] * len(self.buyers)
        for pi, devision in pd:
            for b_index in powerset[devision]:
                self.el_records[b_index] = self.w_records[b_index] / pi

        # 8. record the difference price set
        self.difference_price_set = [
            f"price: {pi} group: {powerset[devision]}" for pi, devision in pd
        ]
        self.p_records = [pi_a, pi_b]
        # # 9. calculate each buyer's utility
        self.buyer_utility_records = [
            self.compute_buyer_utility(r, c, mu, f, w)
            for i in range(len(self.buyers))
            for r, c, mu, f, w in [
                (
                    self.buyers[i].r,
                    self.buyers[i].c,
                    self.buyers[i].mu,
                    self.el_records[i],
                    self.w_records[i],
                )
            ]
        ]
        #
        # # 10. calculate seller utility
        self.seller_utility_record.append(sum(self.w_records))

    def output(self, algorithm_name):
        super().output(algorithm_name)
        print(f"fairness factor {self.fairness_factor}")
        print(self.difference_price_set)
