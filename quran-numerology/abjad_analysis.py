"""Letter, word and abjad analysis of a surah, from the Quranic Arabic Corpus morphology file.

Usage:
    curl -sSLO https://raw.githubusercontent.com/mustafa0x/quran-morphology/master/quran-morphology.txt
    python3 abjad_analysis.py quran-morphology.txt 113

Conventions: Uthmani rasm as written (dagger alif not counted), each written letter counted
once (shadda not doubled), hamza forms and alif wasla = alif (1), alif maqsura = ya (10),
ta marbuta = ha (5). Mashriqi (eastern) abjad values.
"""
import collections
import re
import sys

ABJAD = dict(zip('ابجدهوزحطيكلمنسعفصقرشتثخذضظغ',
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                  200, 300, 400, 500, 600, 700, 800, 900, 1000]))
NORM = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ء': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'}
DIACRITICS = re.compile(r'[ً-ٰٟۖ-ۭـ]')


def letters(text):
    return [c for c in (NORM.get(c, c) for c in DIACRITICS.sub('', text)) if c in ABJAD]


def value(text):
    return sum(ABJAD[c] for c in letters(text))


def load(path):
    words = collections.OrderedDict()
    roots = collections.defaultdict(list)
    for line in open(path, encoding='utf-8'):
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 4:
            continue
        s, v, w, _ = map(int, parts[0].split(':'))
        words.setdefault((s, v, w), []).append(parts[1])
        root = re.search(r'ROOT:([^|]+)', parts[3])
        if root:
            roots[root.group(1)].append(f'{s}:{v}')
    return words, roots


def main(path, surah):
    words, roots = load(path)
    verse_counts = collections.Counter()
    for s, v, _ in words:
        verse_counts[s] = max(verse_counts[s], v)
    first = sum(verse_counts[s] for s in range(1, surah)) + 1
    print(f'Surah {surah}: {verse_counts[surah]} verses, global verses {first}-{first + verse_counts[surah] - 1} '
          f'of {sum(verse_counts.values())}')

    total_words = total_letters = total_value = 0
    freq = collections.Counter()
    surah_roots = collections.OrderedDict()
    for v in range(1, verse_counts[surah] + 1):
        verse = [''.join(words[k]) for k in words if k[:2] == (surah, v)]
        cells = [f'{DIACRITICS.sub("", w)}={value(w)}' for w in verse]
        n_letters = sum(len(letters(w)) for w in verse)
        v_value = sum(value(w) for w in verse)
        print(f'  v{v}: {len(verse)} words, {n_letters} letters, abjad {v_value}  ::  ' + ' | '.join(cells))
        total_words += len(verse)
        total_letters += n_letters
        total_value += v_value
        for w in verse:
            freq.update(letters(w))
    for root, refs in roots.items():
        if any(r.startswith(f'{surah}:') for r in refs):
            surah_roots[root] = refs

    print(f'Total: {total_words} words, {total_letters} letters, abjad {total_value}')
    print(f'Distinct letters: {len(freq)}; absent: {" ".join(c for c in ABJAD if c not in freq)}')
    print('Frequency: ' + ' '.join(f'{c}:{n}' for c, n in freq.most_common()))
    print('Root occurrences across the whole Quran:')
    for root, refs in surah_roots.items():
        print(f'  {root}: {len(refs)}' + (f'  {refs}' if len(refs) <= 12 else ''))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
