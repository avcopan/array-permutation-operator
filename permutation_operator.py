import numpy     as np
import itertools as it
from block_permutations import BlockPermutations

class P(object):

  def __init__(self, axis_strings_with_bars, **kwargs):
    """
    Permutation object constructor
    :param axis_string: a string of the form "0,1/2,3|4,5,6/7|..." defining a permutation of axes
           according to Bartlett and Shavitt
    """
    self.axis_strings_with_bars = axis_strings_with_bars
    self.weight = 1.0 if not 'weight' in kwargs else kwargs['weight']
    axis_strings = axis_strings_with_bars.split('|')
    element_sets, compositions = zip(*(P.process_axis_string(axis_string) for axis_string in axis_strings))
    self.block_permutations = [BlockPermutations(element_set, composition) for element_set, composition in zip(element_sets, compositions)]
    self.elements = sum(element_sets, ())

  def iter_permutations_with_signature(self, ndim):
    axes = tuple(range(ndim))
    pools = tuple(block_permutation.iter_permutations_with_signature() for block_permutation in self.block_permutations)
    for prod in it.product(*pools):
      signs, permuted_subsets = zip(*prod)
      sign = np.product(signs)
      permuted_elements = sum(permuted_subsets, ())
      permuted_axes = self.permute(permuted_elements)(axes)
      yield sign, permuted_axes

  def __mul__(self, other):
    if hasattr(other, "transpose") and hasattr(other, "ndim"):
      return self.weight * sum(sgn * other.transpose(per) for sgn, per in self.iter_permutations_with_signature(other.ndim))
    elif isinstance(other, (float, int)):
      return P(*self.axis_strings_with_bars, weight = self.weight * other)
    else:
      raise Exception("Cannot left-multiply P permutation object with {:s}".format(type(other).__name__))

  def __rmul__(self, other):
    if isinstance(other, (float, int)):
      return P(*self.axis_strings_with_bars, weight = self.weight * other)
    else:
      raise Exception("Cannot right-multiply P permutation object with {:s}".format(type(other).__name__))

  def permute(self, permuted_elements):
    return lambda x: tuple(permuted_elements[self.elements.index(item)] if item in self.elements else item for item in x)

  @staticmethod
  def process_axis_string(axis_string):
    try:
      axis_equivalent_sets = [[int(axis) for axis in substring.split(',')] for substring in axis_string.split('/')]
      elements = tuple(sum(axis_equivalent_sets, []))
      composition = tuple(len(axis_equivalent_set) for axis_equivalent_set in axis_equivalent_sets)
      return elements, composition
    except:
      raise Exception("Invalid string {:s} passed as constructor argument.".format(axis_string))


### SIMPLE TEST CASES ###
if __name__ == "__main__":
  import numpy as np
  from permutation_signature import signature
  import itertools as it
  # 0,1/2,3 case
  T = np.random.rand(20,20,20,20)
  axes = tuple(range(4))
  T = P("0/1|2/3") * T
  print("these should all be true:")
  for sgn, per in P("0/1|2/3").iter_permutations_with_signature(4):
    print np.all(T.transpose(per).round(10) == sgn * T.round(10))
  print("some of these should be false:")
  for per in it.permutations(axes):
    print np.all(T.transpose(per).round(10) == signature(axes,per) * T.round(10))
  print np.linalg.norm(T)
  T = P("0,1/2,3") * T
  print("now these should all be true:")
  for per in it.permutations(axes):
    print np.all(T.transpose(per).round(10) == signature(axes,per) * T.round(10))
  print np.linalg.norm(T)


  # 0/1,2/3 case
  T = np.random.rand(20,20,20,20)
  axes = tuple(range(4))
  T = P("1/2") * T
  print("these should all be true:")
  for sgn, per in P("1/2").iter_permutations_with_signature(4):
    print np.all(T.transpose(per).round(10) == sgn * T.round(10))
  print("some of these should be false:")
  for per in it.permutations(axes):
    print np.all(T.transpose(per).round(10) == signature(axes,per) * T.round(10))
  print np.linalg.norm(T)
  T = P("0/1,2/3") * T
  print("now these should all be true:")
  for per in it.permutations(axes):
    print np.all(T.transpose(per).round(10) == signature(axes,per) * T.round(10))
  print np.linalg.norm(T)
