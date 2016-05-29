class BlockPermutations(object):
  """
  Given a list of elements, iterate over all unique permutations, treating subsets of the elements as equivalent.
  This is done by mapping equivalent elements into a single element, applying all unique permutations to that,
  and applying the same changes to the original set.
  Uses Algorithm L from Knuth 'The Art of Computer Programming: Volume 4A: Pre-Fascicle 2B: Draft of
  Section 7.1.1.2 - Generating All Permutations' which can be found at http://www.cs.utsa.edu/~wagner/knuth/
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
    self.indices = sum((block_size * [ block_index ] for block_index, block_size in enumerate(composition)), [])

  def iter_permutations_with_signature(self):
    elements = list(self.elements)
    indices  = list(self.indices)
    sgn = 1
    p0 = 0
    while p0 >= 0:
      yield sgn, tuple(elements)
      p0 = next((p for p in reversed(range(self.nelem-1)) if indices[p ] < indices[p+1]), -1)
      p1 = next((p for p in reversed(range(self.nelem))   if indices[p0] < indices[p  ]),  0)
      indices [p0], indices [p1] = indices [p1], indices [p0]
      elements[p0], elements[p1] = elements[p1], elements[p0]
      sgn *= -1
      indices [p0+1:] = indices [p0+1:][::-1]
      elements[p0+1:] = elements[p0+1:][::-1]
      sgn *= (-1) ** ( (self.nelem-p0-1)/2 )

