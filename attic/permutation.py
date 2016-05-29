import itertools as it
import numpy     as np

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

  def iter_index_permutations(self):
    elements = list(self.elements)
    indices  = range(self.nelem)
    p0 = 0
    while p0 >= 0:
      yield tuple(indices.index(p) for p in range(self.nelem)) # return the permutation that was applied to 'indices'
      p0 = next((p for p in reversed(range(self.nelem-1)) if elements[p ] < elements[p+1]), -1)
      p1 = next((p for p in reversed(range(self.nelem))   if elements[p0] < elements[p  ]),  0)
      elements[p0], elements[p1] = elements[p1], elements[p0]
      indices [p0], indices [p1] = indices [p1], indices [p0]
      elements[p0+1:] = elements[p0+1:][::-1]
      indices [p0+1:] = indices [p0+1:][::-1]

  def iter_permutations(self):
    for index_permutation in self.iter_index_permutations():
      yield tuple(self.elements[index] for index in index_permutation)


if __name__ == "__main__":
  import math
  unique_permutations = UniquePermutations([0,1,1,1,2,3,3])
  for count, permutation in enumerate(unique_permutations.iter_permutations()):
    print permutation
  print("this should say {:d}".format(math.factorial(7)/(math.factorial(3)*math.factorial(2))))
  print(count + 1)
