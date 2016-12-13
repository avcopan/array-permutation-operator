import numpy     as np
import itertools as it
from ..permutations import BlockPermutations

class PermutationOperator(object):

  def __init__(self, axis_strings_with_bars, **kwargs):
    """
    Permutation object constructor
    :param axis_string: a string of the form "0,1/2,3|4,5,6/7|..." defining a permutation of axes
           according to Bartlett and Shavitt
    """
    self.axis_strings_with_bars = axis_strings_with_bars
    self.weight = 1.0 if not 'weight' in kwargs else kwargs['weight']
    axis_strings = axis_strings_with_bars.split('|')
    element_sets, compositions = zip(*(PermutationOperator.process_axis_string(axis_string) for axis_string in axis_strings))
    self.block_permutations = [BlockPermutations(element_set, composition) for element_set, composition in zip(element_sets, compositions)]
    self.items = sum(element_sets, ())

  def iter_signed_permutations(self, ndim):
    axes = tuple(range(ndim))
    pools = tuple(block_permutation.iter_signed_permutations() for block_permutation in self.block_permutations)
    for prod in it.product(*pools):
      signs, permuted_subsets = zip(*prod)
      sign = np.product(signs)
      permuted_items = sum(permuted_subsets, ())
      permuted_axes = self.permute(permuted_items)(axes)
      yield sign, permuted_axes

  def __mul__(self, other):
    if hasattr(other, "transpose") and hasattr(other, "ndim"):
      return self.weight * sum(sgn * other.transpose(per) for sgn, per in self.iter_signed_permutations(other.ndim))
    elif isinstance(other, (float, int)):
      return PermutationOperator(*self.axis_strings_with_bars, weight = self.weight * other)
    else:
      raise Exception("Cannot left-multiply PermutationOperator object with {:s}".format(type(other).__name__))

  def __rmul__(self, other):
    if isinstance(other, (float, int)):
      return PermutationOperator(*self.axis_strings_with_bars, weight = self.weight * other)
    else:
      raise Exception("Cannot right-multiply PermutationOperator object with {:s}".format(type(other).__name__))

  def permute(self, permuted_items):
    return lambda x: tuple(permuted_items[self.items.index(item)] if item in self.items else item for item in x)

  @staticmethod
  def process_axis_string(axis_string):
    try:
      axis_equivalent_sets = [[int(axis) for axis in substring.split(',')] for substring in axis_string.split('/')]
      items = tuple(sum(axis_equivalent_sets, []))
      composition = tuple(len(axis_equivalent_set) for axis_equivalent_set in axis_equivalent_sets)
      return items, composition
    except:
      raise Exception("Invalid string {:s} passed as constructor argument.".format(axis_string))


if __name__ == "__main__":
  for sgn, per in PermutationOperator("0,1/2,3").iter_signed_permutations(4):
    print(sgn, per)

  P = PermutationOperator
  array1 = np.random.rand(4,4,4)
  #array2 = P("0/1") * array1
  #array3 = P("0,1/2") * array2
  #array4 = P("0/1/2") * array1
  #print(array2)
  #print(array4.round(8))
  #print(array4.round(8))
  #print(np.allclose(array3, array4))
  array2 = P("0") * array1
  print(array2)
  print(np.allclose(array1, array2))
