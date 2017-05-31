class PermutationHelper(object):
    """Helper class for working with permutations.

    Attributes:
        items (tuple): The pool of permuted items in its reference ordering.
        nitems (int): The number of permuted items.
    """

    def __init__(self, items):
        """Initialize the PermutationHelper.

        Args:
            items: The pool of permuted items in its reference ordering.
        """
        self.items = tuple(items)
        self.nitems = len(self.items)
        if self.nitems is not len(set(self.items)):
            raise ValueError("Permuted items must be distinct.")

    def make_element_permuter(self, permutation):
        """Makes a permutation function for individual items.
        
        Args:
            permutation: A permutation of `self.items`.

        Returns:
            function: The permuter.
        """
        assert sorted(permutation) == sorted(self.items)
        return lambda item: (item if item not in self.items
                            else permutation[self.items.index(item)])

    def make_permuter(self, permutation):
        """Makes a permutation function for iterables.

        Args:
            permutation: A permutation of `self.items`.

        Returns:
            function: The permuter.
        """
        permuter = self.make_element_permuter(permutation)
        return lambda iterable: tuple(map(permuter, iterable))

    def get_inverse(self, permutation):
        """Get the inverse of a permutation.

        Args:
            permutation: A permutation of `self.items`.

        Returns:
            tuple: The permutation.
        """
        assert sorted(permutation) == sorted(self.items)
        perm = tuple(permutation)
        return tuple(self.items[perm.index(item)] for item in self.items)
