from opensimplex import OpenSimplex

seed = 123456789

a = OpenSimplex(seed)
b = OpenSimplex(seed + 2**64)

print("Same permutation:", a._perm == b._perm)
print("Same gradient indexes:", a._perm_grad_index3 == b._perm_grad_index3)
print("Stored seed A:", a.get_seed())
print("Stored seed B:", b.get_seed())t