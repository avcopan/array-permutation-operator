def test__sloppy_shuffles_composition_1_1_1():
    from permutils.shuffle import sloppy_shuffles

    it = ('a', 'b', 'c')
    cmp = (1, 1, 1)
    unsigned_shuffles = list(sloppy_shuffles(it, cmp))
    signed_shuffle = list(sloppy_shuffles(it, cmp, yield_signature=True))
    assert (
        unsigned_shuffles == [
            ('a', 'b', 'c'),
            ('a', 'c', 'b'),
            ('b', 'a', 'c'),
            ('b', 'c', 'a'),
            ('c', 'a', 'b'),
            ('c', 'b', 'a')
        ]
    )
    assert (
        signed_shuffle == [
            (('a', 'b', 'c'), +1),
            (('a', 'c', 'b'), -1),
            (('b', 'a', 'c'), -1),
            (('b', 'c', 'a'), +1),
            (('c', 'a', 'b'), +1),
            (('c', 'b', 'a'), -1)
        ]
    )


def test__sloppy_shuffles_composition_1_2():
    from permutils.shuffle import sloppy_shuffles

    it = ('a', 'b', 'c')
    cmp = (1, 2)
    unsigned_shuffles = list(sloppy_shuffles(it, cmp))
    signed_shuffle = list(sloppy_shuffles(it, cmp, yield_signature=True))
    assert (
        unsigned_shuffles == [
            ('a', 'b', 'c'),
            ('c', 'a', 'b'),
            ('c', 'b', 'a')
        ]
    )
    assert (
        signed_shuffle == [
            (('a', 'b', 'c'), +1),
            (('c', 'a', 'b'), +1),
            (('c', 'b', 'a'), -1)
        ]
    )


def test__sloppy_shuffles_composition_1_3():
    from permutils.shuffle import sloppy_shuffles

    it = ('a', 'b', 'c', 'd')
    cmp = (1, 3)
    unsigned_shuffles = list(sloppy_shuffles(it, cmp))
    signed_shuffle = list(sloppy_shuffles(it, cmp, yield_signature=True))
    assert (
        unsigned_shuffles == [
            ('a', 'b', 'c', 'd'),
            ('d', 'a', 'c', 'b'),
            ('d', 'b', 'a', 'c'),
            ('d', 'b', 'c', 'a')
        ]
    )
    assert (
        signed_shuffle == [
            (('a', 'b', 'c', 'd'), +1),
            (('d', 'a', 'c', 'b'), +1),
            (('d', 'b', 'a', 'c'), +1),
            (('d', 'b', 'c', 'a'), -1)
        ]
    )


def test__sloppy_shuffles_composition_2_2():
    from permutils.shuffle import sloppy_shuffles

    it = ('a', 'b', 'c', 'd')
    cmp = (2, 2)
    unsigned_shuffles = list(sloppy_shuffles(it, cmp))
    signed_shuffle = list(sloppy_shuffles(it, cmp, yield_signature=True))
    assert (
        unsigned_shuffles == [
            ('a', 'b', 'c', 'd'),
            ('a', 'd', 'b', 'c'),
            ('a', 'd', 'c', 'b'),
            ('c', 'b', 'a', 'd'),
            ('c', 'b', 'd', 'a'),
            ('c', 'd', 'a', 'b')
        ]
    )
    assert (
        signed_shuffle == [
            (('a', 'b', 'c', 'd'), +1),
            (('a', 'd', 'b', 'c'), +1),
            (('a', 'd', 'c', 'b'), -1),
            (('c', 'b', 'a', 'd'), -1),
            (('c', 'b', 'd', 'a'), +1),
            (('c', 'd', 'a', 'b'), +1)
        ]
    )


def test__sloppy_shuffles_composition_1_2_1():
    from permutils.shuffle import sloppy_shuffles

    it = ('a', 'b', 'c', 'd')
    cmp = (1, 2, 1)
    unsigned_shuffles = list(sloppy_shuffles(it, cmp))
    signed_shuffle = list(sloppy_shuffles(it, cmp, yield_signature=True))
    assert (
        unsigned_shuffles == [
            ('a', 'b', 'c', 'd'),
            ('a', 'b', 'd', 'c'),
            ('a', 'd', 'c', 'b'),
            ('b', 'a', 'c', 'd'),
            ('b', 'a', 'd', 'c'),
            ('b', 'c', 'a', 'd'),
            ('b', 'c', 'd', 'a'),
            ('b', 'd', 'a', 'c'),
            ('b', 'd', 'c', 'a'),
            ('d', 'a', 'c', 'b'),
            ('d', 'b', 'a', 'c'),
            ('d', 'b', 'c', 'a')
        ]
    )
    assert (
        signed_shuffle == [
            (('a', 'b', 'c', 'd'), +1),
            (('a', 'b', 'd', 'c'), -1),
            (('a', 'd', 'c', 'b'), -1),
            (('b', 'a', 'c', 'd'), -1),
            (('b', 'a', 'd', 'c'), +1),
            (('b', 'c', 'a', 'd'), +1),
            (('b', 'c', 'd', 'a'), -1),
            (('b', 'd', 'a', 'c'), -1),
            (('b', 'd', 'c', 'a'), +1),
            (('d', 'a', 'c', 'b'), +1),
            (('d', 'b', 'a', 'c'), +1),
            (('d', 'b', 'c', 'a'), -1)
        ]
    )


if __name__ == "__main__":
    test__sloppy_shuffles_composition_1_1_1()
    test__sloppy_shuffles_composition_1_2()
    test__sloppy_shuffles_composition_1_3()
    test__sloppy_shuffles_composition_2_2()
    test__sloppy_shuffles_composition_1_2_1()
