import numpy as np

def test__block_permutations_composition_1_1_1():
  from tensorshuffle.permutations import BlockPermutations

  perms = list(BlockPermutations(('a', 'b', 'c'), composition=(1,1,1)).iter_signed_permutations())
  assert(
    perms == [
      ( 1, ('a', 'b', 'c')),
      (-1, ('a', 'c', 'b')),
      (-1, ('b', 'a', 'c')),
      ( 1, ('b', 'c', 'a')),
      ( 1, ('c', 'a', 'b')),
      (-1, ('c', 'b', 'a'))
    ]
  )

def test__block_permutations_composition_1_2():
  from tensorshuffle.permutations import BlockPermutations

  perms = list(BlockPermutations(('a', 'b', 'c'), composition=(1,2)).iter_signed_permutations())
  assert(
    perms == [
      ( 1, ('a', 'b', 'c')),
      ( 1, ('c', 'a', 'b')),
      (-1, ('c', 'b', 'a'))
    ]
  )

def test__block_permutations_composition_1_3():
  from tensorshuffle.permutations import BlockPermutations

  perms = list(BlockPermutations(('a', 'b', 'c', 'd'), composition=(1,3)).iter_signed_permutations())
  assert(
    perms == [
      ( 1, ('a', 'b', 'c', 'd')),
      ( 1, ('d', 'a', 'c', 'b')),
      ( 1, ('d', 'b', 'a', 'c')),
      (-1, ('d', 'b', 'c', 'a'))
    ]
  )

def test__block_permutations_composition_2_2():
  from tensorshuffle.permutations import BlockPermutations

  perms = list(BlockPermutations(('a', 'b', 'c', 'd'), composition=(2,2)).iter_signed_permutations())
  assert(
    perms == [
      ( 1, ('a', 'b', 'c', 'd')),
      ( 1, ('a', 'd', 'b', 'c')),
      (-1, ('a', 'd', 'c', 'b')),
      (-1, ('c', 'b', 'a', 'd')),
      ( 1, ('c', 'b', 'd', 'a')), 
      ( 1, ('c', 'd', 'a', 'b'))
    ]
  )

def test__block_permutations_composition_1_2_1():
  from tensorshuffle.permutations import BlockPermutations

  perms = list(BlockPermutations(('a', 'b', 'c', 'd'), composition=(1,2,1)).iter_signed_permutations())
  assert(
    perms == [
      ( 1, ('a', 'b', 'c', 'd')),
      (-1, ('a', 'b', 'd', 'c')),
      (-1, ('a', 'd', 'c', 'b')),
      (-1, ('b', 'a', 'c', 'd')),
      ( 1, ('b', 'a', 'd', 'c')),
      ( 1, ('b', 'c', 'a', 'd')),
      (-1, ('b', 'c', 'd', 'a')),
      (-1, ('b', 'd', 'a', 'c')),
      ( 1, ('b', 'd', 'c', 'a')),
      ( 1, ('d', 'a', 'c', 'b')),
      ( 1, ('d', 'b', 'a', 'c')),
      (-1, ('d', 'b', 'c', 'a'))
    ]
  )

if __name__ == "__main__":
  test__block_permutations_composition_1_1_1()
  test__block_permutations_composition_1_2()
  test__block_permutations_composition_1_3()
  test__block_permutations_composition_2_2()
  test__block_permutations_composition_1_2_1()
