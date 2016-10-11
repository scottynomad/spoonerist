from collections import defaultdict
import pronouncing
import re
from sortedcontainers import SortedList


# https://en.wikipedia.org/wiki/Arpabet

CONSONANT_PHONES = {
    'P', 'B', 'T', 'D', 'K', 'G',
    'CH', 'JH',
    'F', 'V', 'TH', 'DH', 'S', 'Z', 'SH', 'ZH', 'HH',
    'M', 'EM', 'N', 'EN', 'NG', 'ENG',
    'L', 'EL', 'R', 'DX', 'NX',
    'Y', 'W', 'Q'}


cons = '(?:' + '|'.join(CONSONANT_PHONES) + ')'
first_consonants = '(?:{}(?: {})*)'.format(cons, cons)
splitter_re = '^(?P<start>{}) (?P<rest>.+)$'.format(first_consonants)
splitter = re.compile(splitter_re)
filter_re = re.compile("['\.]")


WORD_FREQ = {}


def build_word_freq(corpus=None):
    if corpus is None:
        corpus = open('google-10000-english/google-10000-english-usa.txt', 'r')
    count = 10000 
    for word in corpus:
        WORD_FREQ[word.strip()] = count
        count -= 1


BY_END = defaultdict(SortedList)
BY_START = defaultdict(SortedList)
BY_PHONES = defaultdict(SortedList)


# TODO: Serialize this and reload it must be faster
def build_db():
    pronouncing.init_cmu()
    build_word_freq()
    for word, phones in pronouncing.pronunciations:
        if len(word) < 3:
            continue
        if filter_re.search(word):
            continue
        match = splitter.match(phones)
        if not match:
            continue
        start, end = match.groups()
        rank = WORD_FREQ.get(word, 10000)
        t = (rank, start, end, word)
        BY_END[end].add(t)
        BY_START[start].add(t)
        BY_PHONES[phones].add(t)


build_db()


def split(word):
    """Return a list of tuples of (1st consonnts, subsequents phones, word)"""
    word = word.lower()
    phones = pronouncing.phones_for_word(word)
    res = []
    for p in phones:
        match = splitter.match(p)
        if match:
            rank = WORD_FREQ.get(word, 0)
            res.append((rank, *match.groups(), word))
    return res


def rhymes(word):
    """Return all the words sharing everything after the first sound."""
    _, start, rest, _ = split(word)[0]
    return (t for t in BY_END[rest] if t[3] != word)


def alliterates(word):
    """Return all the words sharing the same first sound."""
    _, start, _, _ = split(word)[0]
    return (t for t in BY_START[start] if t[3] != word)


def pairs(word, limit_to_letter=None):
    """Returns a generator of valid spoonerism pairs for the input word."""
    for score, first, rest, _ in split(word):
        for r_score, r_first, r_rest, rhyme in rhymes(word):
            if limit_to_letter and not rhyme.startswith(limit_to_letter):
                continue
            if r_first == first:
                continue
            for a_score, a_r_first, a_r_rest, a_r in alliterates(rhyme):
                target_phones = '{} {}'.format(first, a_r_rest)
                for m_score, _, _, match in BY_PHONES.get(target_phones, ()):
                    score_all = score + r_score + a_score + m_score
                    yield (word, a_r, rhyme, match)
