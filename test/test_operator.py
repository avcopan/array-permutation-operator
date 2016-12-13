import pytest
import numpy as np

def test__permutation_operator_composition_1():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load("test/random_arrays/15x15.npy")

  array2 = P("0") * array1

  assert(np.allclose(array1, array2))

def test__permutation_operator_composition_1_1():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load("test/random_arrays/15x15.npy")

  array2 = P("0/1") * array1
  array3 = array1 - array1.transpose()

  assert(np.allclose(array2, array3))

def test__permutation_operator_composition_1_2():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load("test/random_arrays/15x15x15.npy")

  array2 = P("1/2") * array1

  array3 = P("0/1,2") * array2
  array4 = array2 - array2.transpose((1, 0, 2)) - array2.transpose((2, 1, 0))
  assert(np.allclose(array3, array4))

def test__permutation_operator_composition_1_1_1():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load("test/random_arrays/15x15x15.npy")

  array2 = P("0/1/2") * array1
  array3 = (array1
            - array1.transpose(0, 2, 1)
            - array1.transpose(1, 0, 2)
            + array1.transpose(1, 2, 0)
            + array1.transpose(2, 0, 1)
            - array1.transpose(2, 1, 0))
  assert(np.allclose(array2, array3))

def test__permutation_operator_composition_2_1():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load("test/random_arrays/15x15x15.npy")

  array2 = P("0/1") * array1

  array3 = P("0,1/2") * array2
  array4 = array2 - array2.transpose((2, 1, 0)) - array2.transpose((0, 2, 1))
  assert(np.allclose(array3, array4))

if __name__ == "__main__":
  test__permutation_operator_composition_1()
  test__permutation_operator_composition_1_1()
  test__permutation_operator_composition_1_2()
  test__permutation_operator_composition_1_1_1()
  test__permutation_operator_composition_2_1()
