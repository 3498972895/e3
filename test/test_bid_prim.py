from .data import static_num_users, static_rs, static_mus, static_cs, static_fmax
from ..entities import Seller, Buyer
from ..algorithms import BidPrim


"""
examing using static data same with article.
I found my result bidprim algorithm is not same with article
Because the source code the author provided uses a MINIMIZE FUCTION FROM a SCIPY library
the article w = [122.4, 139.7, 275.0, 255.2, 79.23]
My w = [15.298366456915105,
        17.459903533822715,
        34.36392209384021,
        31.886747368823258,
        9.900684403990523]
with same ratio
"""
buyers = [
    Buyer(static_rs[i], static_mus[i], static_cs[i]) for i in range(static_num_users)
]
seller = Seller(static_fmax)
bid_prim = BidPrim(buyers, seller)
bid_prim.run()
bid_prim.output()
