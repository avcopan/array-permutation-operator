def sloppy_shuffles(iterable, composition=None, yield_signature=False):
    """Returns sloppy generalized riffle-shuffle permutations of an iterable.
    
    If (p, q, r, ...) is an integer composition of the length n of the iterable,
    this will cut the iterable into packets of size p, q, r, ... and interleave
    them in all n! / (p! * q! * r! * ...) unique ways.  These interleavings will
    be 'sloppy' in the sense that the order of the items within each packet is
    not preserved.  Uses Algorithm L from '`The Art of Computer Programming`_:
    Volume 4A Pre-Fascicle 2B: Draft of Section 7.1.1.2 - Generating All
    Permutations'.

    Args:
        iterable: The collection of items to be shuffled.
        composition: The shuffle composition.  Must be an integer composition of
            the length of the iterable.
        yield_signature: Yield the permutation signature, along with the 
            permuted items?

    Yields:
        tuple: The permuted items.  If `yield_signature` is `True`, this yields
            the permuted items and their signature.

    .. _The Art of Computer Programming:
        http://www.cs.utsa.edu/~wagner/knuth/
    """
    itms = list(iterable)
    n = len(itms)
    comp = composition if composition is not None else (1,) * n
    if sum(comp) is not n:
        raise ValueError("Invalid 'composition' argument.")

    # The algorithm operates on the list `idxs` which is the result of mapping
    # each item in `itms` into its packet index.  That is, if the composition
    # is (3, 1, 2) then `idxs` will be [0, 0, 0, 1, 2, 2].  We then use Knuth's
    # Algorithm L to enumerate the lexicographically sorted permutations of
    # `idxs` and apply the same transpositions to `items` in parallel.  For each
    # transposition, we flip the sign of `sgn`, the signature, which is
    # originally set to 1.

    idxs = sum((size * [idx] for idx, size in enumerate(comp)), [])
    sgn = 1
    p0 = 0
    while p0 >= 0:
        yield tuple(itms) if not yield_signature else (tuple(itms), sgn)
        p0 = next((p for p in reversed(range(n - 1))
                   if idxs[p] < idxs[p + 1]), -1)
        p1 = next((p for p in reversed(range(n)) if idxs[p0] < idxs[p]), 0)
        idxs[p0], idxs[p1] = idxs[p1], idxs[p0]
        sgn *= -1
        idxs[p0 + 1:] = idxs[p0 + 1:][::-1]
        sgn *= (-1) ** ((n - p0 - 1) // 2)

        # Apply the same permutations to `itms`.
        itms[p0], itms[p1] = itms[p1], itms[p0]
        itms[p0 + 1:] = itms[p0 + 1:][::-1]


