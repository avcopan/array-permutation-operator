import pytest
import numpy as np

def test__axis_permutations_exception():
  from tensorshuffle.permutations import BlockPermutations
  from tensorshuffle.operator     import AxisPermutations

  with pytest.raises(Exception):
    pobject = BlockPermutations(('a', 'b'), composition = (1,1))
    perms = list(AxisPermutations(pobject, ndim=5).iter_signed_permutations())

def test__axis_permutations_composition_1_1():
  from tensorshuffle.permutations import BlockPermutations
  from tensorshuffle.operator     import AxisPermutations

  pobject = BlockPermutations((1, 3), composition = (1,1))
  perms = list(AxisPermutations(pobject, ndim=5).iter_signed_permutations())
  assert(
    perms == [
      ( 1, (0, 1, 2, 3, 4)),
      (-1, (0, 3, 2, 1, 4))
    ]
  )

def test__permutation_operator_composition_1_1():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load("test/random_arrays/15x15.npy")
  array2 = np.load("test/random_arrays/15x15.npy")

  #print( P("0/1") * array1 )
  #print(array1)
  #print( (P("0/1") * array1) == array1 )

if __name__ == "__main__":
  test__axis_permutations_exception()
  test__axis_permutations_composition_1_1()
  test__permutation_operator_composition_1_1()
