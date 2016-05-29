import itertools as it
from permutation_signature import signature

class BlockPermutations(object):
  """
  Given a list of elements, iterate over all unique permutations, treating subsets of the elements as equivalent.
  """
  def __init__(self, elements, composition):
    """
    :param elements: an iterable; for example ('a','b','c','d')
    :param composition: an integer composition of the number of elements, indicating which subsets of elements
           should be treated as equivalent; with the above example, (2,2) would indicate that ('a','b') and
           ('c','d') should be treated as equivalent.
    """
    self.elements = tuple(elements)
    self.nelem = len(elements)
    ncomp = len(composition)
    block_slices = [slice(sum(composition[:start]), sum(composition[:end])) for start, end in zip(range(0, ncomp), range(1, ncomp+1))]
    blocks = [self.elements[slc] for slc in block_slices]
    self.symmetries = [sum(permuted_blocks,()) for permuted_blocks in it.product(*(it.permutations(block) for block in blocks))]

  def iter_permutations(self):
    unique_permutations = []
    for permuted_elements in it.permutations(self.elements):
      if not any(self.permute(sym)(permuted_elements) in unique_permutations for sym in self.symmetries):
        unique_permutations.append(permuted_elements)
        yield permuted_elements

  def iter_permutations_with_signature(self):
    for permutation in self.iter_permutations():
      yield signature(self.elements, permutation), permutation

  def permute(self, permuted_elements):
    return lambda x: tuple(permuted_elements[self.elements.index(item)] if item in self.elements else item for item in x)


