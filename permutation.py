import itertools as it

class BlockPermutations(object):
  """
  Given a list of elements, iterate over all unique permutations, treating subsets of the elements as equivalent.
  The algorithm works by mapping the list of elements into a list of integers [0,0,0,1,1,3,4,4,4,...], identifying
  which equivalence block they belong to, and using that to generate the unique permutations.
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
    self.ncomp = len(composition)
    block_indices = sum(( block_size * [block_index] for block_index, block_size in enumerate(composition)),[])
    # for composition [2,3,1,4] this will equal [0,0,1,1,1,2,3,3,3,3]
    self.unique_permutations = UniquePermutations(block_indices)

  def iter_permutations_with_signature(self):
    for sgn, index_permutation in self.unique_permutations.iter_index_permutations_with_signature():
      yield sgn, tuple(self.elements[index] for index in index_permutation)
    

class UniquePermutations(object):
  """
  Given an ordered list of elements, possibly containing repeats, iterate over unique permutations.
  Uses Algorithm L from Knuth 'The Art of Computer Programming: Volume 4A: Pre-Fascicle 2B: Draft of
  Section 7.1.1.2 - Generating All Permutations' which can be found at http://www.cs.utsa.edu/~wagner/knuth/
  """
  def __init__(self, elements):
    """
    :param elements: an iterable, which is **assumed to be in sorted order**
    """
    self.nelem = len(elements)
    self.elements = tuple(sorted(elements))

  def iter_index_permutations_with_signature(self):
    elements = list(self.elements)
    indices  = range(self.nelem)
    sgn = 1
    p0 = 0
    while p0 >= 0:
      yield sgn, tuple(indices.index(p) for p in range(self.nelem)) # return the permutation that was applied to 'indices'
      p0 = next((p for p in reversed(range(self.nelem-1)) if elements[p ] < elements[p+1]), -1)
      p1 = next((p for p in reversed(range(self.nelem))   if elements[p0] < elements[p  ]),  0)
      elements[p0], elements[p1] = elements[p1], elements[p0]
      indices [p0], indices [p1] = indices [p1], indices [p0]
      sgn *= -1
      elements[p0+1:] = elements[p0+1:][::-1]
      indices [p0+1:] = indices [p0+1:][::-1]
      sgn *= (-1) ** ( (self.nelem-p0-1)/2 ) # number of transpositions for a reversal

  def iter_permutations_with_signature(self):
    for sgn, index_permutation in self.iter_index_permutations_with_signature():
      yield sgn, tuple(self.elements[index] for index in index_permutation)


if __name__ == "__main__":
  perms = BlockPermutations('abcd', [1,2,1])
  for sgn, per in perms.iter_permutations_with_signature():
    print('{:s} {:>2d}'.format(''.join(per), sgn))
    print parity('abcd', per)
