def decompose_permutation(elements, permuted_elements):
  elements = tuple(elements)
  permuted_elements = list(permuted_elements)
  transpositions = []
  for p0, element in enumerate(elements):
    p1 = permuted_elements.index(element)
    if not p0 == p1:
      permuted_elements[p0], permuted_elements[p1] = permuted_elements[p1], permuted_elements[p0]
      transpositions.append((p0, p1))
  assert elements == tuple(permuted_elements)
  return transpositions


if __name__ == "__main__":
  import itertools as it
  print decompose_permutation('abcd', 'cadb')

