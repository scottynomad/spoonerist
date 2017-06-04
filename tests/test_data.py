import pronouncing
import pytest


from spoonerist.data import (
    alliterates,
    pairs,
    split,
    rhymes
)


# [u'P ER0 M IH1 T', u'P ER1 M IH2 T']
@pytest.mark.parametrize('test_input, expected', [
    ('permit', [(7046, 'P', 'ER0 M IH1 T', 'permit'),
                (7046, 'P', 'ER1 M IH2 T', 'permit')]),
    ('breeze', [(0, 'B R', 'IY1 Z', 'breeze')])
])
def test_split(test_input, expected):
    assert split(test_input) == expected


@pytest.mark.parametrize('test_input, expected, absent', [
    ('cheese', ['peas'], ['cheese', 'fleece'])
])
def test_rhymes(test_input, expected, absent):
    res = [t[3] for t in rhymes(test_input)]
    for e in expected:
        assert e in res
    for e in absent:
        assert e not in res


@pytest.mark.parametrize('test_input, expected, absent', [
    ('cheese', ['chancellor', 'chess'], ['cheese', 'christ']),
    ('breeze', [], ['b'])
])
def test_alliterates(test_input, expected, absent):
    res = [t[3] for t in alliterates(test_input)]
    for e in expected:
        assert e in res
    for e in absent:
        assert e not in res


@pytest.mark.parametrize('test_word, limit_letter,  expected, absent', [
    ('cheese', 'b', [('cheese', 'baack', 'beas', 'chalk')], []),
    ('balls', 'b', [('balls', 'bra', 'brawls', 'bah')], []),
    ('stork', 'b', [('stork', 'bumbling', 'bork', 'stumbling')], [])
])
def test_pairs(test_word, limit_letter, expected, absent):
    res = list(pairs(test_word, limit_letter))
    for e in expected:
        assert e in res
    for e in absent:
        assert e not in res


def test_pair_order_stability():
    g = pairs('stork')
    assert g.__next__() == ("stork", "cologne", "cork", "stallone")
