def disjoint_cycles_to_permutation(elements, cycles):
  if cycles == [()]: return tuple(elements)
  elements = list(elements)
  for cycle in cycles:
    for elem1, elem2 in reversed(zip(cycle,cycle[1:])):
      i, j = elements.index(elem1), elements.index(elem2)
      elements[i], elements[j] = elements[j], elements[i]
  return tuple(elements)

if __name__ == "__main__":
  import itertools as it
  from parity import signature
  perms = list(it.permutations(range(4)))
  unique_perms = []
  for i, p1 in enumerate(perms):
    p2 = disjoint_cycles_to_permutation(p1, [(1,2)])
    if not p2 in unique_perms:
      unique_perms.append(p1)
  print unique_perms

  import itertools as it
  from parity import signature
  perms = list(it.permutations(range(4)))
  unique_perms = []
  has_symmetries = [[(0,1)],[(2,3)],[(0,1),(2,3)]]
  for i, p1 in enumerate(perms):
    if not any(disjoint_cycles_to_permutation(p1, sym) in unique_perms for sym in has_symmetries):
      unique_perms.append(p1)
  print len(unique_perms)
  print unique_perms
