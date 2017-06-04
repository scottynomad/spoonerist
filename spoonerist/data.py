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
corpus_re = re.compile("(.+)\W+(\d+)")

WORD_FREQ = {}


def build_word_freq(corpus=None):
    if corpus is None:
        corpus = open('resources/words.txt', 'r')
    for line in corpus:
        match = corpus_re.match(line)
        word = match.groups()[0]
        freq = match.groups()[1]
        WORD_FREQ[word.strip()] = int(freq)


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
        if word not in WORD_FREQ:
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
    """Return a list of tuples of (rank, 1st consonants, subsequent phones, word.
    
    Rank of 0 indicates that the word is not in the word frequency list.
    """
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
    l1_splits = split(word)

    combinations = []
    for l1 in l1_splits:
        for r1 in rhymes(l1[-1]):
            if limit_to_letter and not r1[-1].startswith(limit_to_letter):
                continue
            if l1[1] == r1[1]:
                continue
            for l2 in alliterates(r1[-1]):
                target_phones = '{} {}'.format(l1[1], l2[2])
                r2 = BY_PHONES.get(target_phones)
                #for r2 in BY_PHONES.get(target_phones, ()):
                if r2:
                    r2 = sorted(r2, key=lambda r: r[0])
                    combinations.append((l1, l2, r1, r2[0]))

    sorted_combinations = sorted(combinations, key=lambda p: p[2][0] + p[1][0] + p[3][0], reverse=True)
    # TODO Unique
    return [[w[-1] for w in c] for c in sorted_combinations]