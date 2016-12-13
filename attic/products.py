import itertools as it
import numpy     as np

class PermutationProducts(object):
  """
  Given a series of permutation objects, iterate over their Cartesian product.
  """

  def __init__(self, *permutation_objects):
    """
    Construct a permutation object
    :param permutation_objects: a tuple of permutation objects which implement the method iter_signed_permutations
    """
    self.pobjects = permutation_objects
    self.items    = sum((pobject.items for pobject in self.pobjects), ())
    self.nelem    = sum((pobject.nelem for pobject in self.pobjects))

  def iter_signed_permutations(self):
    """
    Iterate over signed permutations.
    """
    for product in it.product(*(pobject.iter_signed_permutations() for pobject in self.pobjects)):
      signs, permutations = zip(*product)
      sign = np.product(signs)
      permutation = sum(permutations, ())
      yield sign, permutation


if __name__ == "__main__":
  from ..permutations import BlockPermutations
  pobject = PermutationProducts(
    BlockPermutations(('a','b'), composition=(1,1)),
    BlockPermutations(('c','d'), composition=(1,1))
  )
  for sgn, per in pobject.iter_signed_permutations():
    print(sgn, per)
