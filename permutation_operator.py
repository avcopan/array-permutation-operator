import permutation as per

class P(object):

  def __init__(self, axis_string, **kwargs):
    """
    Permutation object constructor
    :param axis_string: a string of the form "0,1/2,3|4,5,6/7|..." defining a permutation of axes
           according to Bartlett and Shavitt
    """
    self.weight = 1.0 if not 'weight' in kwargs else kwargs['weight']
    self.axis_strings = axis_string.split('|')

  def iter_permutations(self, ndim):
    print "HELLO WORLD"

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

