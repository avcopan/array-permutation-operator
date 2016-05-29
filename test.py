import numpy as np
import itertools as it
from permutation_signature import signature

def test__4d_01_slash_23():
  from permutation_operator import P
  T = np.random.rand(20,20,20,20)
  axes = tuple(range(4))
  T = P("0/1|2/3") * T
  assert     all( np.all(T.transpose(per).round(10) == sgn                  * T.round(10)) for sgn, per in P("0/1|2/3").iter_permutations_with_signature(4) )
  assert not all( np.all(T.transpose(per).round(10) == signature(axes, per) * T.round(10)) for per      in it.permutations(axes) )
  assert np.linalg.norm(T) != 0
  T = P("0,1/2,3") * T
  assert     all( np.all(T.transpose(per).round(10) == signature(axes, per) * T.round(10)) for per      in it.permutations(axes) )
  assert np.linalg.norm(T) != 0


def test__4d_0_slash_12_slash_3():
  from permutation_operator import P
  T = np.random.rand(20,20,20,20)
  axes = tuple(range(4))
  T = P("1/2") * T
  assert     all( np.all(T.transpose(per).round(10) == sgn                  * T.round(10)) for sgn, per in P("1/2").iter_permutations_with_signature(4) )
  assert not all( np.all(T.transpose(per).round(10) == signature(axes, per) * T.round(10)) for per      in it.permutations(axes) )
  assert np.linalg.norm(T) != 0
  T = P("0/1,2/3") * T
  assert     all( np.all(T.transpose(per).round(10) == signature(axes, per) * T.round(10)) for per      in it.permutations(axes) )
  assert np.linalg.norm(T) != 0


def test__5d_0_slash_12_slash_34():
  from permutation_operator import P
  T = np.random.rand(15,15,15,15,15)
  axes = tuple(range(5))
  T = P("1/2|3/4") * T
  assert     all( np.all(T.transpose(per).round(10) == sgn                  * T.round(10)) for sgn, per in P("1/2|3/4").iter_permutations_with_signature(5) )
  assert not all( np.all(T.transpose(per).round(10) == signature(axes, per) * T.round(10)) for per      in it.permutations(axes) )
  assert np.linalg.norm(T) != 0
  T = P("0/1,2/3,4") * T
  assert     all( np.all(T.transpose(per).round(10) == signature(axes, per) * T.round(10)) for per      in it.permutations(axes) )
  assert np.linalg.norm(T) != 0

