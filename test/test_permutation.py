import pytest as pt
from permutils.helper import PermutationHelper


def test__init_exception():
    with pt.raises(ValueError):
        PermutationHelper(('a', 'b', 'c', 'a'))


def test__inverse_permuter_items():
    import itertools as it

    for nitems in range(2, 7):
        items = tuple(range(nitems))
        ph = PermutationHelper(items)
        for perm in it.permutations(items):
            inv_perm = ph.get_inverse(perm)
            inv_permuter = ph.make_permuter(inv_perm)
            assert inv_permuter(perm) == items
