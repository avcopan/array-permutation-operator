import itertools   as it
import numpy       as np
import permutation as perm

class P(object):

  def __init__(self, axis_strings_with_bars, **kwargs):
    """
    Permutation object constructor
    :param axis_string: a string of the form "0,1/2,3|4,5,6/7|..." defining a permutation of axes
           according to Bartlett and Shavitt
    """
    self.weight = 1.0 if not 'weight' in kwargs else kwargs['weight']
    axis_strings = axis_strings_with_bars.split('|')
    self.nblocks = len(axis_strings)
    element_sets, compositions = zip(*[P.process_axis_string(axis_string) for axis_string in axis_strings])
    self.block_permutations = [perm.BlockPermutations(element_set, composition) for element_set, composition in zip(element_sets, compositions)]
    self.elements = sum((element_set for element_set in element_sets), ())

  def iter_permutations(self, ndim):
    axes = tuple(range(ndim))
    pools = tuple(block_permutation.iter_permutations_with_signature() for block_permutation in self.block_permutations)
    for prod in it.product(*pools):
      signs, permuted_subsets = zip(*prod)
      sign = np.product(signs)
      permuted_elements = sum(permuted_subsets, ())
      permuted_axes = P.apply_permutation(axes, self.elements, permuted_elements)
      yield sign, permuted_axes

  def __mul__(self, other):
    if hasattr(other, "transpose") and hasattr(other, "ndim"):
      return self.weight * sum(sgn * other.transpose(per) for sgn, per in self.iter_permutations(other.ndim))
    elif isinstance(other, (float, int)):
      return P(*self.axis_tuples, weight = self.weight * other)
    else:
      raise Exception("Cannot left-multiply P permutation object with {:s}".format(type(other).__name__))

  def __rmul__(self, other):
    if isinstance(other, (float, int)):
      return P(*self.axis_tuples, weight = self.weight * other)
    else:
      raise Exception("Cannot right-multiply P permutation object with {:s}".format(type(other).__name__))

  @staticmethod
  def process_axis_string(axis_string):
    try:
      axis_equivalent_sets = [[int(axis) for axis in substring.split(',')] for substring in axis_string.split('/')]
      elements = tuple(sum(axis_equivalent_sets, []))
      composition = tuple(len(axis_equivalent_set) for axis_equivalent_set in axis_equivalent_sets)
      return elements, composition
    except:
      raise Exception("Invalid string {:s} passed as constructor argument.".format(axis_string))

  @staticmethod
  def apply_permutation(operand, elements, permuted_elements):
    permuted_operand = [None] * len(operand)
    for index, item in enumerate(operand):
      if not item in elements:
        permuted_operand[index] = item
      elif item in elements:
        permuted_operand[index] = permuted_elements[elements.index(item)]
    return tuple(permuted_operand)


if __name__ == "__main__":
  print P.process_axis_string("0/1,2/3")
  per1 = P("0,1/2,3|4/5")
  for sgn, p in per1.iter_permutations(7):
    print('{:>2d} {:s}'.format(sgn, str(p)))

  # test it on a matrix
  import numpy as np
  M = np.arange(3*3).reshape((3, 3))
  print P("0/1") * M

  # test it on a 3d array for all permutations
  T = np.random.rand(3, 3, 3)
  A = P("0/1/2") * T
  from parity import signature
  print("these should all be true:")
  ref = tuple(range(3))
  for per in it.permutations(ref):
    print np.all(A.transpose(per).round(10) == signature(ref,per)*A.round(10))

  # test it on a 4d array for subset permutations
  # 1. first antisymmetrize with respect to axes (0, 1) and (2, 3)
  print("'0/1|2/3' permutations:")
  per2 = P("0/1|2/3")
  for sgn, p in per2.iter_permutations(4):
    print('{:>2d} {:s}'.format(sgn, str(p)))
  T = np.random.rand(3, 3, 3, 3)
  A = P("0/1|2/3") * T # make T antisymmetric in the first and second pair of indices
  print("these should all be true:")
  for sgn, p in per2.iter_permutations(4):
    print np.all(A.transpose(p).round(10) == sgn*A.round(10))
  print("these should all be false:")
  print np.all(A.transpose((2,1,0,3)).round(10) == -A.round(10))
  print np.all(A.transpose((3,1,2,0)).round(10) == -A.round(10))
  print np.all(A.transpose((0,2,1,3)).round(10) == -A.round(10))
  print np.all(A.transpose((0,3,2,1)).round(10) == -A.round(10))
  print np.all(A.transpose((2,3,0,1)).round(10) == -A.round(10))

  # 2. now apply '0,1/2,3' permutation, which should make it totally antisymmetric
  print("'0,1/2,3' permutations:")
  per3 = P("0,1/2,3")
  for sgn, p in per3.iter_permutations(4):
    print('{:>2d} {:s}'.format(sgn, str(p)))

  B = sum( sgn * A.transpose(p) for sgn, p in per3.iter_permutations(4) )
  print("these should all be true:")
  for sgn, p in per3.iter_permutations(4):
    print sgn, p
    print np.all(B.transpose(p).round(10) == sgn*B.round(10))
