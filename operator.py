import numpy as np
from .permutations import BlockPermutations, AppliedPermutations

class PermutationOperator(object):
  """Operator for applying antisymmetrizing operations to numpy arrays.

  Attributes:
    axis_string: A string of integers separated by commas and forward slashes,
      defining an antisymmetrizing operation of the axes for a numpy- array-like
      object using the notation of `Shavitt and Bartlett`_.  The operand must
      have `ndim` as an attribute and must implement the method `transpose()`_.
    _permutation_object: A `tensorshuffle.permutations.BlockPermutations` object
      which iterates over the permutations needed to achieve the anti-
      symmetrization operation defined by `axis_string`.
    _weight: After antisymmetrization, the array will be scaled by this value.
    _left_operator: Another instance of the PermutationOperator class, to be
      applied after this one.

  Examples:
    >>> import numpy as np
    >>> 
    >>> P = PermutationOperator
    >>> array1 = np.random.rand(15,15,15)
    >>> array2 = P("0/1") * array1 # antisymmetrizes array1 w.r.t. axes 0 and 1
    >>> array3 = P("0,1/2") * array2 # antisymmetrizes array2, assuming it is
    >>>                              # already antisymmetric in the first two
    >>>                              # axes
    >>> 
    >>> array4 = P("0/1/2") * array1 # totally antisymmetrize array1
    >>> np.allclose(array3, array4) # array3 and array4 are now equal
    True

  .. _Shavitt and Bartlett
     I. Shavitt and R. J. Bartlett, `Many-Body Methods in Chemistry and Physics`
    (Cambridge University Press, Cambridge, UK, 2009).
  .. _transpose():
     https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.transpose.html
  """

  def __init__(self, axis_string, _weight = 1.0, _left_operator = None):
    """Initialize PermutationOperator object.

    After defining this object's class attributes, build a BlockPermutations
    object to achieve the antisymmetrization defined by `axis_string`.  For
    example if `axis_string` is "0/1,2/3" then `self._permutation_object` will
    be BlockPermutations(range(4), composition = (1, 2, 1)).

    Args:
      axis_string: String of comma/forward-slash separated integers defining the
        antisymmetrizing operation.
      _weight: After antisymmetrization, the array will be scaled by this value.
      _left_operator: After antisymmetrization, this `PermutationOperator` will
        be applied to the result.
    """
    self.axis_string = axis_string
    self._weight = _weight
    self._left_operator = _left_operator
    try:
      eq_classes = [tuple(int(item) for item in eq_class.split(','))
                    for eq_class in axis_string.split('/')]
      composition = tuple(len(eq_class) for eq_class in eq_classes)
      items = sum(eq_classes, ())
      self._permutation_object = BlockPermutations(items, composition)
    except:
      raise Exception("{:s} is not a valid axis_string.".format(axis_string))

  def __mul__(self, other):
    """Left-multiply `other` by `self`.

    Return the appropriate value of (`self * other`).
    If `other` is a scalar value, pass it to `self.__rmul__()`.
    If `other` is a `PermutationOperator`, return a copy of `other` in which
    `other._left_operator` has been replaced with `self` or
    `self * other._left_operator`, depending on whether or not its initial value
    was `None`.
    If `other` is array-like (having a `tranpose()` method and an attribute
    `ndim`), antisymmetrize it by summing over all signed axis permutations in
    `self._permutation_object` and multiply the result by `self._weight`.  If
    `self._left_operator` is `None`, return it.  Otherwise, return
    `self._left_operator.__mul__(result_array)`.
    Note that the second and third cases have a recursive component, since
    `self._left_operator` has its own `_left_operator` attribute.  The upshot is
    that `P1 * P2 * P3 * array` gets evaluted as `P1 * (P2 * (P3 * array))`.

    Args:
      other: The operand, which must be an array-like object, a scalar, or
        another PermutationOperator.
    """
    if isinstance(other, (float, int)):
      return self.__rmul__(other)
    elif isinstance(other, self.__class__):
      left_operator = (self if other._left_operator is None else
                       self.__mul__(other._left_operator))
      return PermutationOperator(other.axis_string, _weight = other._weight,
                                 _left_operator = left_operator)
    elif hasattr(other, "transpose") and hasattr(other, "ndim"):
      ax_perm_object = AppliedPermutations(self._permutation_object,
                                           operand_set = range(other.ndim))
      result_array = (self._weight *
                      sum(sgn * other.transpose(ax_perm) for sgn, ax_perm
                          in ax_perm_object.iter_signed_permutations()))
      return (result_array if self._left_operator is None
              else self._left_operator.__mul__(result_array))
    else:
      raise Exception("PermutationOperator cannot be left-multiplied with {:s}"
                      .format(type(other).__name__))

  def __rmul__(self, other):
    """Right-multiply `other` by `self`.

    Return the appropriate value of (`other * self`).  If `other` is a scalar
    value, return a copy of `self` with `self._weight` scaled by `other`.  If
    `other` is a PermutationOperator, call `other.__mul__()` instead.
    """
    if isinstance(other, (float, int)):
      return PermutationOperator(self.axis_string,
                                 _weight = self._weight * other,
                                 _left_operator = self._left_operator)
    elif isinstance(other, self.__class__):
      return other.__mul__(self)
    else:
      raise Exception("PermutationOperator cannot be right-multiplied with {:s}"
                      .format(type(other).__name__))

if __name__ == "__main__":
  P = PermutationOperator
  array1 = np.random.rand(15,15,15)
  array2 = P("0/1") * array1 # antisymmetrizes array1 w.r.t. axes 0 and 1
  array3 = P("0,1/2") * array2 # antisymmetrizes array2, assuming it is
                               # already antisymmetric in the first two
                               # axes
  
  array4 = P("0/1/2") * array1 # totally antisymmetrize array1
  print(np.allclose(array3, array4)) # array3 and array4 are now equal

  
