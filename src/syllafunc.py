import re
import pyphen
from regex_funcs import LETTERS_REGEX, PUNCTUATION_REGEX, fix_re_escape

s = pyphen.Pyphen(lang='en')


REGEX = PUNCTUATION_REGEX + r"|" + LETTERS_REGEX + r"+"


def syllables_split(sentence: str):
    words = sentence.split()
    syllable_list = []
    for word in words:
        # Make sure dashes in words don't just disappear
        word.replace("-"," ")
        syllables = s.inserted(word).split('-')
        word.replace(" ", "-")
        if word == '\U000e0000' or all(len(ele) == 0 for ele in syllables):
            continue

        # Separate punctuation to be separate grammatically
        syllables_punctuation = []
        for syllable in syllables:
            # Make sure syllable isn't empty
            if syllables == '':
                continue

            # Splits words and punctuation
            split = re.findall(REGEX, re.escape(syllable))
            # Fixes the \\ being messed up from re.escape
            for i, e in enumerate(split):
                split[i] = fix_re_escape(e)
            # Adds the split array to the syllables and punctuation array
            syllables_punctuation = syllables_punctuation + split

        syllable_list.append(syllables_punctuation)
    return syllable_list


def syllables_to_sentence(syllable_lists):
    # Join each list of syllables back into words
    words = [''.join(syllables) for syllables in syllable_lists]
    sentence = ' '.join(words)  # Join words into a complete sentence
    return sentence
