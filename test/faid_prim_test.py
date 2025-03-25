from .data import static_num_users, static_rs, static_mus, static_cs, static_fmax
from ..entities import Seller, Buyer
from ..algorithms import FaidPrim

"""
data same with paper's NUMERICAL RESULTS section beginning.
"""
buyers = [
    Buyer(static_rs[i], static_mus[i], static_cs[i]) for i in range(static_num_users)
]
seller = Seller(static_fmax)
faid_prim = FaidPrim(buyers, seller, 3.5)
faid_prim.run()
faid_prim.output("FAID-PRIM")
