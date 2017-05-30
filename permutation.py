class PermutationHelper(object):
    """Helper class for working with permutations.

    Attributes:
        items (tuple): The pool of permutable items in its reference ordering.
        nitems (int): The number of permutable items.
    """

    def __init__(self, items):
        """Initialize the PermutationHelper.

        Args:
            items: The pool of permutable items in its reference ordering.
        """
        self.items = tuple(items)
        self.nitems = len(self.items)

    def permuter(self, permutation):
        """Makes a permutation function for individual items.
        
        Args:
            permutation: A permutation of `self.items`.

        Returns:
            function: The permuter.
        """
        return lambda itm: (itm if itm not in self.items
                            else permutation[self.items.index(itm)])

    def get_signature(self, permutation):
        """Get a permutation's signature.
        
        Args:
            permutation: A permutation of `self.items`.

        Returns:
            int: The signature.
        """
        sgn = +1
        perm = list(permutation)
        assert(len(perm) == self.nitems and set(perm) == self.nitems)
        for index, item in enumerate(self.items):
            perm_index = perm.index(item)
            sgn *= -1 if index is not perm_index else +1
            perm[index], perm[perm_index] = perm[perm_index], perm[index]
