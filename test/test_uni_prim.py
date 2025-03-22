from .data import static_num_users, static_rs, static_mus, static_cs, static_fmax
from ..entities import Seller, Buyer
from ..algorithms import UniPrim

buyers = [
    Buyer(static_rs[i], static_mus[i], static_cs[i]) for i in range(static_num_users)
]
seller = Seller(static_fmax)
uni_prim = UniPrim(buyers, seller)
uni_prim.run()
uni_prim.output()
