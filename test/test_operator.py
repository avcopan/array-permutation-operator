import pytest
import numpy as np
import os 
test_dir_path = os.path.dirname(os.path.realpath(__file__))
array_path_template = os.path.join(test_dir_path, "random_arrays", "{:s}.npy")

def test__permutation_operator_composition_1():
  """
  Make sure P("0") acts as the identity.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15"))
  array2 = P("0") * array1

  assert(np.allclose(array1, array2))

def test__permutation_operator_composition_1_1():
  """
  Make sure P("0/1") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15"))

  array2 = P("0/1") * array1
  array3 = array1 - array1.transpose()

  assert(np.allclose(array2, array3))

def test__permutation_operator_composition_1_2():
  """
  Build an array which is antisymmetrized with respect to axes 1 and 2, then
  check to make sure P("0/1,2") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15"))
  array2 = P("1/2") * array1
  
  array3 = P("0/1,2") * array2
  array4 = array2 - array2.transpose((1, 0, 2)) - array2.transpose((2, 1, 0))
  assert(np.allclose(array3, array4))

def test__permutation_operator_composition_2_1():
  """
  Build an array which is antisymmetrized with respect to axes 0 and 1, then
  check to make sure P("0,1/2") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15"))
  array2 = P("0/1") * array1

  array3 = P("0,1/2") * array2
  array4 = array2 - array2.transpose((2, 1, 0)) - array2.transpose((0, 2, 1))
  assert(np.allclose(array3, array4))

def test__permutation_operator_composition_1_1_1():
  """
  Make sure P("0/1/2") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15"))

  array2 = P("0/1/2") * array1
  array3 = (array1
            - array1.transpose((0, 2, 1))
            - array1.transpose((1, 0, 2))
            + array1.transpose((1, 2, 0))
            + array1.transpose((2, 0, 1))
            - array1.transpose((2, 1, 0)))
  assert(np.allclose(array2, array3))

def test__permutation_operator_composition_1_3():
  """
  Build an array which is antisymmetrized with respect to axes 1, 2, and 3, then
  check to make sure P("0/1,2,3") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))
  array2 = P("1/2/3") * array1

  array3 = P("0/1,2,3") * array2
  array4 = (array2
            - array2.transpose((1, 0, 2, 3))
            - array2.transpose((2, 1, 0, 3))
            - array2.transpose((3, 1, 2, 0)))
  assert(np.allclose(array3, array4))

def test__permutation_operator_composition_2_2():
  """
  Build an array in which axes (0, 1) and axes (2, 3) are separately anti-
  symmetrized, then check to make sure P("0,1/2,3") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))
  array2 = P("0/1") * P("2/3") * array1

  array3 = P("0,1/2,3") * array2
  array4 = (array2
            - array2.transpose((2, 1, 0, 3))
            - array2.transpose((3, 1, 2, 0))
            - array2.transpose((0, 2, 1, 3))
            - array2.transpose((0, 3, 2, 1))
            + array2.transpose((2, 3, 0, 1)))
  assert(np.allclose(array3, array4))

def test__permutation_operator_composition_3_1():
  """
  Build an array which is antisymmetrized with respect to axes 0, 1, and 2, then
  check to make sure P("0,1,2/3") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))
  array2 = P("0/1/2") * array1

  array3 = P("0,1,2/3") * array2
  array4 = (array2
            - array2.transpose((3, 1, 2, 0))
            - array2.transpose((0, 3, 2, 1))
            - array2.transpose((0, 1, 3, 2)))

  assert(np.allclose(array3, array4))

def test__permutation_operator_composition_1_2_1():
  """
  Build an array which is antisymmetrized with respect to axes 1 and 2, then
  check to make sure P("0/1,2/3") does the right thing.
  """
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))
  array2 = P("1/2") * array1

  array3 = P("0/1,2/3") * array2
  array4 = (array2
            - array2.transpose((1, 0, 2, 3))
            - array2.transpose((2, 1, 0, 3))
            - array2.transpose((3, 1, 2, 0))
            - array2.transpose((0, 3, 2, 1))
            - array2.transpose((0, 1, 3, 2))
            + array2.transpose((1, 0, 3, 2))
            + array2.transpose((2, 3, 0, 1))
            + array2.transpose((1, 3, 2, 0))
            + array2.transpose((2, 1, 3, 0))
            + array2.transpose((3, 0, 2, 1))
            + array2.transpose((3, 1, 0, 2)))
  assert(np.allclose(array3, array4))

def test__permutation_operator_expression_01():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))

  array2 = 0.25 * P("0/1") * P("2/3") * array1

  array3 = 0.25 * (array1
                   - array1.transpose((1, 0, 2, 3))
                   - array1.transpose((0, 1, 3, 2))
                   + array1.transpose((1, 0, 3, 2)))

  assert(np.allclose(array2, array3))

def test__permutation_operator_expression_02():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))

  array2 = (0.25 * P("0/1")) * P("2/3") * array1

  array3 = 0.25 * (array1
                   - array1.transpose((1, 0, 2, 3))
                   - array1.transpose((0, 1, 3, 2))
                   + array1.transpose((1, 0, 3, 2)))

  assert(np.allclose(array2, array3))

def test__permutation_operator_expression_03():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))

  array2 = P("0/1") * (P("2/3") * 0.25) * array1

  array3 = 0.25 * (array1
                   - array1.transpose((1, 0, 2, 3))
                   - array1.transpose((0, 1, 3, 2))
                   + array1.transpose((1, 0, 3, 2)))

  assert(np.allclose(array2, array3))

def test__permutation_operator_expression_04():
  from tensorshuffle.operator import PermutationOperator as P

  array1 = np.load(array_path_template.format("15x15x15x15"))

  array2 = P("2/3").__rmul__(P("0/1")).__mul__(0.25) * array1

  array3 = 0.25 * (array1
                   - array1.transpose((1, 0, 2, 3))
                   - array1.transpose((0, 1, 3, 2))
                   + array1.transpose((1, 0, 3, 2)))

  assert(np.allclose(array2, array3))

def test__permutation_operator_expression_05():
  from tensorshuffle.operator import PermutationOperator as P

  with pytest.raises(Exception):
    array1 = np.load(array_path_template.format("15x15x15x15"))

    array2 = 0.25 * P("0/1") * P("2/3").__rmul__(array1)



if __name__ == "__main__":
  test__permutation_operator_composition_1()
  test__permutation_operator_composition_1_1()
  test__permutation_operator_composition_1_2()
  test__permutation_operator_composition_2_1()
  test__permutation_operator_composition_1_1_1()
  test__permutation_operator_composition_1_3()
  test__permutation_operator_composition_2_2()
  test__permutation_operator_composition_3_1()
  test__permutation_operator_composition_1_2_1()
  test__permutation_operator_expression_01()
  test__permutation_operator_expression_02()
  test__permutation_operator_expression_03()
  test__permutation_operator_expression_04()
  test__permutation_operator_expression_05()
