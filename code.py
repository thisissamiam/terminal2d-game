from opensimplex import OpenSimplex

seeds = [0, 1, 123456789, 999999999999999]

for seed in seeds:
    a = OpenSimplex(seed)
    b = OpenSimplex(seed + 2**64)

    print(
        seed,
        (a._perm == b._perm).all(),
        (a._perm_grad_index3 == b._perm_grad_index3).all()
    )