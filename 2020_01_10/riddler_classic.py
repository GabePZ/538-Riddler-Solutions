import collections
import string

import tqdm
import pandas as pd
import matplotlib.pyplot as plt


class Scorer:
    def __init__(self):
        self.bases = collections.OrderedDict(
            {1_000_000_000_000: 'trillion',
             1_000_000_000: 'billion',
             1_000_000: 'million',
             1_000: 'thousand',
             100: 'hundred',
             90: 'ninety',
             80: 'eighty',
             70: 'seventy',
             60: 'sixty',
             50: 'fifty',
             40: 'forty',
             30: 'thirty',
             20: 'twenty',
             19: 'nineteen',
             18: 'eighteen',
             17: 'seventeen',
             16: 'sixteen',
             15: 'fifteen',
             14: 'fourteen',
             13: 'thirteen',
             12: 'twelve',
             11: 'eleven',
             10: 'ten',
             9: 'nine',
             8: 'eight',
             7: 'seven',
             6: 'six',
             5: 'five',
             4: 'four',
             3: 'three',
             2: 'two',
             1: 'one'}
        )
        self.listed_bases = list(self.bases)
        self.zero = 'zero'
        self.cache = {}

    def int_to_str(self,
                   n: int) -> str:
        def _int_to_str(n: int,
                        base: int
                        ) -> str:
            word = []
            if n in self.bases:
                return self.bases[n]
            base_num = self.listed_bases[base]
            base_word = self.bases[base_num]
            if n // base_num > 0:
                # Only need to specify the number of bases for numbers above 100
                if n >= 100:
                    word.append(_int_to_str(n // base_num, base + 1))
                word.append(base_word)

            if n != 0:
                word.append(_int_to_str(n % base_num, base + 1))

            word_str = ' '.join(word)
            self.cache[n] = word_str
            return word_str.strip()
        word = []
        # We cant handle anything larger than 1 trillion
        if n >= 1_000_000_000_000_000:
            raise ValueError('Number is too big')

        # If n equals zero then we just need to return 0
        if n == 0:
            return self.zero

        # If n is negative then we just need to add negative to the
        # front of the word
        if n < 1:
            word.append('negative')
            n = abs(n)

        final_word = _int_to_str(n, 0)
        self.cache[n] = final_word

        return final_word.strip()

    @staticmethod
    def score_word(word: str) -> int:
        def _score_leter(l: str) -> int:
            l = l.upper()
            score = string.ascii_uppercase.find(l)
            # Score starts at 1 not 0
            # (spaces will have a score of -1 which is normalized to 0)
            score += 1
            return score

        return sum(map(_score_leter, list(word)))

    def score_int(self, n: int) -> int:
        word = self.int_to_str(n)
        score = self.score_word(word)
        return score

    def run_tests(self) -> None:
        print('Testing score_word...', end='')
        assert self.score_word('rIDdLER') == 70
        assert self.score_word('OnE') == 34
        assert self.score_word('TWO') == 58
        assert self.score_word('ONe THOUSAND FOUR HUNDRED SEVENTEEN') == 379
        print("pass")
        print('Testing int_to_str...', end='')
        assert self.int_to_str(0) == 'zero'
        assert self.int_to_str(150) == 'one hundred fifty'
        assert self.int_to_str(1_593_152) == 'one million five hundred ninety three thousand one hundred fifty two'
        print('pass')
        print('Testing score_int...', end='')
        assert self.score_int(1) == 34
        assert self.score_int(2) == 58
        assert self.score_int(1417) == 379
        print('pass')


scorer = Scorer()

def write_range(start: int, stop: int, io) -> None:
    for i in tqdm.tqdm(range(start, stop)):
        score = scorer.score_int(i)
        if score > i:
            print('i:', i, ' score: ', score)

        io.write(f'{i},{score}\n')

if __name__ == '__main__':
	with open('./history.csv', 'w') as csvfile:
	    csvfile.write('i,score\n')
	    write_range(1, 100_000, csvfile)

	df = pd.read_csv('./history.csv')

	plt.plot(df.i, df.score)
	plt.plot(df.i, df.i)
	plt.yscale('log')

	plt.show()


