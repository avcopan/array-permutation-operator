import itertools as it

class BlockPermutations(object):
  """
  Unique permutations, treating subsets ("blocks") of the items as equivalent.

  This is done by mapping equivalent items into a single element, applying all
  unique permutations to that, and applying the same changes to the original
  set.  Uses Algorithm L from Knuth '`The Art of Computer Programming`_: Volume
  4A Pre-Fascicle 2B: Draft of Section 7.1.1.2 - Generating All Permutations'.

  Attributes:
    items: The set of items to be permuted, e.g. ('a','b','c','d').
    nitems: The number of items.
    composition: An integer composition of `nitems`, indicating which subsets of
      items should be treated as equivalent.  In the above example, (2,2) would
      indicate that ('a','b') and ('c','d') should be treated as equivalent.

  .. _The Art of Computer Programming:
     http://www.cs.utsa.edu/~wagner/knuth/
  """

  def __init__(self, items, composition):
    self.items       = tuple(items)
    self.nitems      = len(items)
    self.composition = tuple(composition)
    if not sum(self.composition) == self.nitems:
      raise Exception("{:s} is not an integer composition of {:d}".format(
                      str(self.composition), self.nitems))

  def iter_signed_permutations(self):
    """
    Iterate over signed permutations.

    Omit permutations of equivalent items by mapping the list of items into a
    list of equivalence class indices. For example, if self.items equals
    ('a', 'b', 'c', 'd') and self.composition equals (2, 2), then the
    equivalence class indices would be [0, 0, 1, 1].

    Yields:
      tuple: A pair, in which the second element is a `tuple` containing the
        permuted items and the first element is the permutation signature, an
        `int` with value `+1` or `-1`.
    """
    items   = list(self.items)
    indices = sum((size * [index] for index, size in
                  enumerate(self.composition)), [])
    sgn = 1
    p0 = 0
    while p0 >= 0:
      yield sgn, tuple(items)
      p0 = next((p for p in reversed(range(self.nitems-1))
                if indices[p ] < indices[p+1]), -1)
      p1 = next((p for p in reversed(range(self.nitems))
                if indices[p0] < indices[p  ]),  0)
      indices[p0], indices[p1] = indices[p1], indices[p0]
      items  [p0], items  [p1] = items  [p1], items  [p0]
      sgn *= -1
      indices[p0+1:] = indices[p0+1:][::-1]
      items  [p0+1:] = items  [p0+1:][::-1]
      sgn *= (-1) ** ( (self.nitems-p0-1)//2 )


class AppliedPermutations(object):
  """
  Permutations applied to a larger set containing the permuted items.

  Attributes:
    permutation_object: A permutation object.  Must have `items` as an attribute
      and implement the method `iter_signed_permutations()`
    items: The set of permuted items.  Obtained from permutation_object.
    operand_set: The set items to which the permutations are applied.
      Must contain `items`, which is its default value.
  """

  def __init__(self, permutation_object, operand_set):
    """
    Initialize AppliedPermutations object.

    After filling this object's class attributes, check to ensure that
    `permutation_object.items` is a valid subset of `self.operand_set`.
    """
    self.permutation_object = permutation_object
    self.items = permutation_object.items
    self.operand_set = tuple(operand_set)
    if not all(item in self.operand_set for item in self.items):
      raise Exception("{:s} is not a subset of {:s}".format(
                      str(self.items), str(self.operand_set)))

  def iter_signed_permutations(self):
    """
    Iterate over signed permutations.

    Iterate over permutations in `self.permutation_object`, applying them to
    `self.operand_set`.

    Yields:
      tuple: A pair, in which the second element is a `tuple` containing the
        permuted `operand_set` and the first element is the permutation
        signature, an `int` with value `+1` or `-1`.
    """
    for sgn, per in self.permutation_object.iter_signed_permutations():
      yield sgn, self._make_permuted_operand_set(per)

  def _make_permuted_operand_set(self, permuted_items):
    """
    Apply a permutation to `self.operand_set` and return the result.
    """
    return tuple(permuted_items[self.items.index(item)] if item in self.items
                 else item for item in self.operand_set)



if __name__ == "__main__":
  block_perms = BlockPermutations(('a', 'b', 'c', 'd'), composition=(1, 3))
  for sgn, per in block_perms.iter_signed_permutations():
    print(sgn, per)

  block_perms = BlockPermutations(('b', 'c', 'd'), composition = (1, 1, 1))
  applied_perms = AppliedPermutations(block_perms, operand_set =
                                      ('a', 'b', 'c', 'd', 'e'))
  for sgn, per in applied_perms.iter_signed_permutations():
    print(sgn, per)

