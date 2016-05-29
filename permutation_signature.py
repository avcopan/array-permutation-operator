def signature(ref, per):
  """
  Given a reference iterable and a permuted iterable, return the parity of the permutation.
  :param ref: reference iterable
  :param per: permuted iterabl
  """
  sgn, per = +1, list(per)
  for elem in ref:
    i, j = ref.index(elem), per.index(elem)
    sgn *= -1 if not i is j else +1
    per[i], per[j] = per[j], per[i]
  return sgn

