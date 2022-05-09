import nltk
from nltk.book import *
from nltk.corpus import udhr, wordnet as wn
from nltk.corpus import words


def chapter2_24():
    def generate_random_text_on_n_most_likely_words(text, n):
        fdist = FreqDist(text)
        fdist = fdist.most_common(n)
        for i in range(n):
            print(random.choice(fdist)[0], end=' ')

    print()
    generate_random_text_on_n_most_likely_words(text1, 200)
    # print()
    # print()
    # generate_random_text_on_n_most_likely_words(brown.words(categories='news'), 200)
    # print()
    # print()
    # generate_random_text_on_n_most_likely_words(brown.words(categories=['news', 'romance']), 200)
    # print()
    # print()


def chapter2_25():
    def find_language(s):
        langs = []
        for lang in udhr.fileids():
            if lang.endswith('Latin1') and s in udhr.words(lang):
                langs.append(lang)
        return langs

    print(find_language('in'))


def chapter2_26():
    cnt = 0
    hypos = 0
    for synset in wn.all_synsets('n'):
        if synset.hyponyms():
            hypos += len(synset.hyponyms())
            cnt += 1
    print(hypos / cnt)


def chapter3_40():
    def ari(raw):
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = sent_tokenizer.tokenize(raw)
        words = nltk.word_tokenize(raw)
        av_wordlength = sum(len(w) for w in words) / len(words)
        av_sentlength = sum(len(s) for s in sents) / len(sents)
        return (4.71 * av_wordlength) + (0.5 * av_sentlength) - 21.43

    print(ari(nltk.corpus.abc.raw("rural.txt")))
    print(ari(nltk.corpus.abc.raw("science.txt")))


def chapter3_41():
    words = ['attribution', 'confabulation', 'elocution', 'sequoia', 'tenacious', 'unidirectional']
    vsequences = set([''.join([char for char in word if char in 'aeiou']) for word in words])
    sorted(vsequences)


def chapter4_32():
    def summarize(text_sents, n):
        from operator import itemgetter
        freqDist = nltk.FreqDist([w.lower() for sent in text_sents for w in sent])
        scoresSents = [(sum(freqDist[word] for word in sent), index, sent) for (index, sent) in enumerate(text_sents)]
        sortByFreq = sorted(scoresSents, key=itemgetter(0), reverse=True)[:n]
        sortByIndex = sorted(sortByFreq, key=itemgetter(1))
        for (freq, index, sent) in sortByIndex:
            print(index, ': ', sent, '\n')

    from nltk.corpus import brown
    summarize(brown.sents(categories='religion'), 10)


def chapter4_35(n):
    current_words, word_squares, unused = [word.upper() for word in filter(lambda w: len(w) == n, words.words())], [], [[] for i in range(n)]

    def check(word):
        if word in word_squares:
            return False
        else:
            for (index, square_word) in enumerate(word_squares):
                if word[index] != square_word[len(word_squares)]:
                    return False
            return True

    def add():
        if len(word_squares) == n:
            return True
        else:
            for word in current_words:
                if len(word_squares) == n:
                    return True
                if (word not in unused[len(word_squares)]) and check(word):
                    word_squares.append(word)
                    add()
            if len(word_squares) not in [n, 0]:
                unused[len(word_squares) - 1].append(word_squares.pop())
                for i in range(len(word_squares) + 1, n):
                    unused[i] = []
                add()
            return False
    if add():
        for word in word_squares:
            print(word)
    else:
        print('No Square')


import re, textwrap, random


def get_length(items):
    return sum([len(i) for i in items])


def distribute_paragraph(text, width):
    splitted = textwrap.wrap(' '.join([text]), width)

    for line in splitted:

        items = line.split()

        # evenly add spaces to each item (except the last item)
        # until the difference between the new length of the line
        # and the width is zero, or less than the number of items
        for j in range((width - get_length(items)) // len(items)):
            for i in range(len(items) - 1):
                items[i] += ' '

        # add spaces to random items until width is reached
        for si in random.sample(range(0, len(items) - 1),
                                width - get_length(items)):
            items[si] = items[si] + ' '

        print(''.join(items))


# text = """This story happened a long time ago in a galaxy far, far away. It is already over. Nothing can be done to change it.
# It is a story of love and loss, brotherhood and betrayal, courage and sacrifice and the death of dreams. It is a story of the blurred line between our best and our worst. It is the story of the end of an age.
# A strange thing about stories -- Though this all happened so long ago and so far away that words cannot describe the time or the distance, it is also happening right now. Right here.
# It is happening as you read these words. This is how twenty-five millennia come to a close. Corruption and treachery have crushed a thousand years of peace. This is not just the end of a republic; night is falling on civilization itself.
# This is the twilight of the Jedi. The end starts now.
# """
# text = re.sub(r'\n', ' ', text)
# text = re.sub(r' +', ' ', text)
# text = re.sub(r'’', "'", text)
#
# distribute_paragraph(text, width=60)

# chapter4_35()

def chapter5_34():
    import nltk
    from nltk.corpus import brown
    from tabulate import tabulate

    tags = brown.tagged_words()
    cfd = nltk.ConditionalFreqDist(tags)

    num_tags = []
    for condition in cfd.conditions():
        num_tags.append((condition, len(cfd[condition])))

    tags_by_num = []

    for i in range(11):
        this_num = 0
        for (word, num) in num_tags:
            if num == i:
                this_num += 1
        tags_by_num.append((i, this_num))

    # prints a table of the integers 1-10 and the numbers of distinct words in the corpus that have those numbers of distinct tags

    print(tabulate(tags_by_num))

    # "that" is the word with the most distinct tags.
    distinct_tags = [tag for tag in cfd['that']]

    tagged_sents = brown.tagged_sents()

    # go through each sentence in the corpus.
    # go through each tag in the sentence

    for sent in tagged_sents:
        for (word, tag) in sent:
            for distinct_tag in distinct_tags:
                if distinct_tag == tag and (word == 'That' or word == 'that'):
                    print(sent)
                    distinct_tags.remove(distinct_tag)
                    print("************")
                    break
def chapter5_35():
    import nltk
    from nltk.corpus import brown

    tagged_words = brown.tagged_words()
    cfd = nltk.ConditionalFreqDist(tagged_words)
    tagged_sents = brown.tagged_sents()

    bigram_tags = list(nltk.bigrams(tagged_words))

    words_following_must = []
    for bigram in bigram_tags:
        # returns a list of the form [['of', 'years'], ['IN', 'NNS']]
        zipped_tag = [list(t) for t in zip(*bigram)]
        if zipped_tag[0][0] == 'must' or zipped_tag[0][0] == 'Must':
            words_following_must.append((zipped_tag[0][1], zipped_tag[1][1]))

    tags_following_must = set([tag for (__, tag) in words_following_must])

    for bigram in bigram_tags:
        zipped_tag = [list(t) for t in zip(*bigram)]
        if zipped_tag[0][0] == 'must' or zipped_tag[0][0] == 'Must':
            print(zipped_tag[0][0] + " " + zipped_tag[0][1])
            if zipped_tag[1][1] in ['BE', 'BE-HL', 'NN', 'NNS', 'NP-HL']:
                print("Context is likely epistemic")
            elif zipped_tag[1][1] in ['HV', 'HV-TL', 'DO', 'RB', 'RB-HL', 'VB', 'VB-HL', 'VB-TL', 'VBZ']:
                print("Context is likely deontic")
            else:
                print("Context is unclear")
chapter5_35()
