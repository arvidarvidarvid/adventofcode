import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.readlines()


def test_phrase(phrase, anagrams=False):
    words = phrase.split()
    if anagrams:
        words = [''.join(sorted(word)) for word in words]
    return len(words) == len(set(words))


def test():
    assert test_phrase('aa bb cc dd ee') is True
    assert test_phrase('aa bb cc dd aa') is False
    assert test_phrase('aa bb cc dd aaa') is True
    assert test_phrase('abcde fghij', anagrams=True) is True
    assert test_phrase('abcde xyz ecdab', anagrams=True) is False
    assert test_phrase('a ab abc abd abf abj', anagrams=True) is True
    assert test_phrase('iiii oiii ooii oooi oooo', anagrams=True) is True
    assert test_phrase('oiii ioii iioi iiio', anagrams=True) is False
    return True


def main():
    input = get_input()
    valid_phrases = sum([1 for p in input if test_phrase(p)])
    valid_anagram_phrases = sum([1 for p in input if test_phrase(p, True)])
    logger.info('Result 1: %s' % valid_phrases)
    logger.info('Result 2: %s' % valid_anagram_phrases)


if __name__ == '__main__':
    if test():
        main()
